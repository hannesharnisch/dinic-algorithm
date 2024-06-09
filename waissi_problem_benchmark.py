import sys
from lib.network.capacitatedArc import CapacitatedArc, Capacity
from lib.network.network import Network
from lib.network.node import Node
from lib.networkInput import NetworkInput
from lib.solver.dinicSolver import DinicSolver
from lib.solver.gurobiMaxFlowSolver import GurobiMaxFlowSolver
from lib.solver.solverState import SolverState
"""
    This file is a benchmark test for the problem proposed by Waissi 1991.
"""

def generate_problem_network(n):

    # Add the initial source and target nodes and the start arc
    network = Network(NetworkInput())
    network.add_node(Node("s", demand=-999999999999999))
    network.add_node(Node("t", demand=9999999999999))
    network.add_arc(CapacitatedArc(from_node="s", to_node="t", capacity=Capacity(1, 0), cost=0))

    # Add all other nodes depending on how big the Waissi network should be
    for i in range(2, n):
        network.add_node(Node(str(i)))
        if i == 2:
            network.add_arc(CapacitatedArc(from_node="s", to_node=network.get_node(str(i)).id, capacity=Capacity(n, 0), cost=0))
        else:
            network.add_arc(CapacitatedArc(from_node=str(i-1), to_node=network.get_node(str(i)).id, capacity=Capacity(n, 0), cost=0))
        network.add_arc(CapacitatedArc(from_node=str(i), to_node="t", capacity=Capacity(1, 0), cost=0))

    return network

def solve_problem_network(network, solver):
    state = SolverState(network=network)

    if solver == "Gurobi":
        solver = GurobiMaxFlowSolver()
    else:
        solver = DinicSolver()

    return solver.solve(state=state)

def execute_n_times_and_get_avg(n, network, solver):
    solutionStates = []
    for i in range(n):
        tempSolution = solve_problem_network(network, solver)
        solutionStates.append(tempSolution)

    mappedSolutionStates = map(lambda x: x.solution.calc_duration.total_seconds() * 1000, solutionStates)
    return sum(mappedSolutionStates) / n

if __name__ == "__main__":
    n = 256

    network = generate_problem_network(n)

    print("*** GUROBI RESULT: ***")
    print("Average solution time:")
    print(f"{execute_n_times_and_get_avg(10, network, "Gurobi")} ms")


    print("\n")
    print("*** DINIC RESULT: ***")
    print("Average solution time:")
    print(f"{execute_n_times_and_get_avg(10, network, "Dinic")} ms")
