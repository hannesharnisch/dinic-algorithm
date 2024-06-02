from lib.solver.solver import Solver
from lib.solver.solverState import SolverState, SolverSolution
import gurobipy as gp
from gurobipy import GRB


class GurobiMinCostFlowSolver(Solver):

    def solve(self, state: SolverState) -> SolverSolution:
        """
        Gets a SolverResult which contains a min-cost-flow problem network and an optinal initial solution.
        This function tries to optimally solve the problem.
        """
        # Create a new model
        model = gp.Model('min-cost-flow')
        
        # Add model varibables for flows on arcs
        flow = {}
        for arc in state.network.arcs:
            arc_key = (arc.from_node, arc.to_node)
            flow[arc_key] = model.addVar(
                lb=arc.capacity.lb,
                ub=arc.capacity.ub,
                obj=arc.cost,
                vtype=GRB.CONTINUOUS,
                name=f"x_{arc.from_node}_{arc.to_node}"
            )

            #Add initial solution
            if state.solution == None:
                continue

            if arc_key in state.solution.flow.keys():
                flow[arc_key].start = state.solution.flow[arc_key]



        # Add flow conservation constraints for each node
        for node in state.network.nodes:
            demand = node.demand
            inflow = gp.quicksum(flow[i, j] for i, j in flow.keys() if j == node.id)
            outflow = gp.quicksum(flow[i, j] for i, j in flow.keys() if i == node.id)
            model.addConstr(inflow - outflow == demand, name=f"flow_maintenance_{node.id}")

        # Set objective to minimize the total cost
        model.ModelSense = GRB.MINIMIZE

        # Set the method to network simplex
        model.setParam(GRB.Param.Method, 1)

        # Optimize the model
        model.optimize()

        # Output the results
        if model.status != GRB.OPTIMAL:
            return None
        
        solution_flow = {}
        for arc, modelVar in flow.items():
            if(modelVar.x > 0):
                solution_flow[arc] = int(modelVar.x)

        return SolverState(
            network = state.network,
            solution = SolverSolution(
                flow=solution_flow, 
                target_value=model.ObjVal
            )
        )
        