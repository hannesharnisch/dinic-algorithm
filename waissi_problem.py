import sys
from lib.network.capacitatedArc import CapacitatedArc, Capacity
from lib.network.network import Network
from lib.network.node import Node
from lib.networkInput import NetworkInput
from lib.solver.dinicSolver import DinicSolver
from lib.solver.solverState import SolverState

"""
    This file is a benchmark test for the problem proposed by Waissi 1991.
"""

def generate_problem_network_and_solve(n):

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

    state = SolverState(network=network)

    dinicSolver = DinicSolver()

    print("Starting solving...")

    solutionState = dinicSolver.solve(state=state)
    print("Solution time:")
    print(f"{solutionState.solution.calc_duration.total_seconds() * 1000} ms")
    sum = 0
    for arc in solutionState.solution.flow.keys():
        if (arc[1] == "t"):
            sum = sum + solutionState.solution.flow[arc]

    print("Solution Max Flow:")
    print(sum)

if __name__ == "__main__":
    n = 8192

    sys.setrecursionlimit(9000) # Recursion limit has to be enhanced for this
    generate_problem_network_and_solve(n)
