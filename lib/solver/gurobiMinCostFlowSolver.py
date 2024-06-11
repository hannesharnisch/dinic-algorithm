from datetime import datetime

from loguru import logger
from lib.network.capacitatedArc import CapacitatedArc
from lib.solver.solver import Solver
from lib.solver.solverState import SolverState, SolverSolution
import gurobipy as gp
from gurobipy import GRB


class GurobiMinCostFlowSolver(Solver):

    def __init__(self, use_initial_solution: bool = True):
        self.use_initial_solution = use_initial_solution

    def solve(self, state: SolverState) -> SolverSolution:
        """
        Gets a SolverResult which contains a min-cost-flow problem network and an optinal initial solution.
        This function tries to optimally solve the problem.
        """

        network = state.network

        # Create a new model
        with gp.Env(empty=True) as env:
            env.setParam('OutputFlag', 0)
            env.start()
            with gp.Model('min-cost-flow', env=env) as min_cost_model:
                # Add model varibables for flows on arcs
                variables: dict[CapacitatedArc, gp.Var] = {}
                for arc in network.arcs:
                    arc_key = (arc.from_node, arc.to_node)
                    variables[arc_key] = min_cost_model.addVar(
                        lb=arc.capacity.lb,
                        ub=arc.capacity.ub,
                        obj=arc.cost,
                        vtype=GRB.CONTINUOUS,
                        name=f"x_{arc.from_node}_{arc.to_node}"
                    )

                    # Add initial solution
                    if state.solution == None:
                        continue

                    if self.use_initial_solution:
                        if arc_key in state.solution.flow.keys():
                            variables[arc_key].start = state.solution.flow[arc_key]

                # Add flow conservation constraints for each node
                inflow_vars = {node.id: [] for node in network.nodes}
                outflow_vars = {node.id: [] for node in network.nodes}

                for arc in network.arcs:
                    outflow_vars[arc.from_node].append(
                        variables[(arc.from_node, arc.to_node)])

                    inflow_vars[arc.to_node].append(
                        variables[(arc.from_node, arc.to_node)])

                for node in network.nodes:
                    demand = node.demand
                    inflow = gp.quicksum(inflow_vars[node.id])
                    outflow = gp.quicksum(outflow_vars[node.id])
                    min_cost_model.addConstr(inflow - outflow == demand,
                                             name=f"flow_maintenance_{node.id}")

                # Set objective to minimize the total cost
                min_cost_model.ModelSense = GRB.MINIMIZE

                # Set the method to network simplex
                min_cost_model.setParam(GRB.Param.Method, 1)

                start = datetime.now()

                # Optimize the model
                min_cost_model.optimize()

                # Output the results
                if min_cost_model.status != GRB.OPTIMAL:
                    return None

                solution_flow = {}
                for arc, modelVar in variables.items():
                    if (modelVar.x > 0):
                        solution_flow[arc] = int(modelVar.x)

                end = datetime.now()

                logger.success(
                    f"Gurobi Min - Calculation duration: {end-start}")

                return SolverState(
                    network=network,
                    solution=SolverSolution(
                        flow=solution_flow,
                        target_value=min_cost_model.ObjVal,
                        calc_duration=end-start
                    )
                )
