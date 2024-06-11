from datetime import datetime

from loguru import logger
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
            with gp.Model('max_flow', env=env) as max_flow_model:

                # Create variables
                variables: dict[CapacitatedArc, gp.Var] = {}
                for arc in network.arcs:
                    variables[(arc.from_node, arc.to_node)] = max_flow_model.addVar(
                        lb=0, ub=arc.capacity.ub, name=f"x_{arc.from_node}_{arc.to_node}")

                # Objective function
                max_flow_model.setObjective(gp.quicksum(variables[(arc.from_node, arc.to_node)]
                                                        for arc in network.arcs if arc.from_node == source.id), gp.GRB.MAXIMIZE)

                # Flow conservation constraints
                inflow_vars = {node.id: []
                               for node in network.nodes if node != source and node != sink}
                outflow_vars = {node.id: []
                                for node in network.nodes if node != source and node != sink}

                for arc in network.arcs:
                    if arc.from_node != source.id:
                        outflow_vars[arc.from_node].append(
                            variables[(arc.from_node, arc.to_node)])

                    if arc.to_node != sink.id:
                        inflow_vars[arc.to_node].append(
                            variables[(arc.from_node, arc.to_node)])

                for node in inflow_vars:
                    inflow = gp.quicksum(inflow_vars[node])
                    outflow = gp.quicksum(outflow_vars[node])
                    max_flow_model.addConstr(inflow - outflow == 0,
                                             name=f"flow_maintenance_{node}")

                start = datetime.now()
                # Solve the model
                max_flow_model.optimize()

                if max_flow_model.status != gp.GRB.OPTIMAL:
                    return None

                solution_flow = {}
                for arc, modelVar in variables.items():
                    if (modelVar.x > 0):
                        solution_flow[arc] = int(modelVar.x)

                end = datetime.now()

                logger.success(
                    f"Gurobi Max - Calculation duration: {end-start}")

                return SolverState(
                    network=state.network,
                    solution=SolverSolution(
                        flow=solution_flow,
                        target_value=max_flow_model.ObjVal,
                        calc_duration=end-start
                    )
                )
