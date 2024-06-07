from datetime import datetime
from lib.network.capacitatedArc import CapacitatedArc
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverSolution, SolverState
import gurobipy as gp


class GurobiMaxFlowSolver(Solver):
    def solve(self, state: SolverState) -> SolverState:

       

        network = state.network
        source = network.get_node("s")
        sink = network.get_node("t")

        # Create a new model
        with gp.Env(empty=True) as env:
            env.setParam('OutputFlag', 0)
            env.start()
            with gp.Model('max_flow',env=env) as max_flow:

                # Create variables
                variables: dict[CapacitatedArc, gp.Var] = {}
                for arc in network.arcs:
                    variables[(arc.from_node, arc.to_node)] = max_flow.addVar(
                        lb=0, ub=arc.capacity.ub, name=f"x_{arc.from_node}_{arc.to_node}")
        
                # Objective function
                max_flow.setObjective(gp.quicksum(variables[(arc.from_node, arc.to_node)]
                                      for arc in network.arcs if arc.from_node == source.id), gp.GRB.MAXIMIZE)
        
                # Flow conservation constraints
                for node in network.nodes:
                    if node == source or node == sink:
                        continue
                    inflow = gp.quicksum(variables[(arc.from_node, arc.to_node)]
                                         for arc in network.arcs if arc.to_node == node.id)
                    outflow = gp.quicksum(variables[(arc.from_node, arc.to_node)]
                                          for arc in network.arcs if arc.from_node == node.id)
                    max_flow.addConstr(inflow - outflow == 0,
                                       name=f"flow_maintenance_{node.id}")
        
                start = datetime.now()
                # Solve the model
                max_flow.optimize()
        
                if max_flow.status != gp.GRB.OPTIMAL:
                    return None
        
                solution_flow = {}
                for arc, modelVar in variables.items():
                    if (modelVar.x > 0):
                        solution_flow[arc] = int(modelVar.x)
        
                end = datetime.now()
        
                print(f"Gurobi Max - Calculation duration: {end-start}")
        
                return SolverState(
                    network=state.network,
                    solution=SolverSolution(
                        flow=solution_flow,
                        target_value=max_flow.ObjVal,
                        calc_duration=end-start
                    )
                )
