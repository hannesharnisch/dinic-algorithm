import time
from lib.exporter.plotExporter import PlotExporter
from lib.exporter.textExporter import TextExporter
from lib.settings import  SolverMethod, settings
from lib.networkInput import NetworkInput
from lib.network.network import Network
from lib.solver.dinicSolver import DinicSolver
from lib.solver.gurobiMaxFlowSolver import GurobiMaxFlowSolver
from lib.solver.gurobiMinCostFlowSolver import GurobiMinCostFlowSolver
from lib.solvingPipeline import SolvingPipeline
from lib.transformer.maxFlowTransformer import MaxFlowTransformer


def export(pipeline: SolvingPipeline, file_name: str) -> None:
    pipeline.export_to_file(TextExporter(), file_name)
    if settings.plot_output:
        pipeline.export_to_file(PlotExporter(), file_name)

def create_pipeline():

    print('---------------------------------------------')
    print('Loading Inputdata...')
    network_input = NetworkInput()
    network_input.load_data_from_txt_file(settings.data_path)
    print('---------------------------------------------')

    print('Start creating Network...')
    network = Network(network_input)
    print('---------------------------------------------')


    print('Start solving MinCostFlow...')
    pipeline = SolvingPipeline(network)
    pipeline.transform_network(MaxFlowTransformer())
    
    if settings.solver_method ==  SolverMethod.Dinic:
        print('Selected solver method: ' + settings.solver_method)
        pipeline.apply_solver(DinicSolver())
        export(pipeline, '/Dinic/MaxFlow')

    elif settings.solver_method == SolverMethod.Gurobi:
        print('Selected solver method:' + settings.solver_method)
        pipeline.apply_solver(GurobiMaxFlowSolver())
        export(pipeline, '/Gurobi/MaxFlow')

    else:
        raise ValueError('Invalid solver method:' + settings.solver_method)


    pipeline.use_initial_network()
    pipeline.apply_solver(GurobiMinCostFlowSolver(settings.use_initial_solution))
    export(pipeline, '/Gurobi/MinCostFlow')
    print('...')

    return pipeline

if __name__ == '__main__':

    start_time = time.time()

    pipeline = create_pipeline()
    pipeline.run(debug=False)


    print('Total time: ' + str(time.time() - start_time) + ' seconds')
