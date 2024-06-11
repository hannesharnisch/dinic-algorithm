import time

from lib.settings import SolverMethod, settings
from loguru import logger
from lib.exporter.plotExporter import PlotExporter
from lib.exporter.textExporter import TextExporter
from lib.logger import init_logging
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


def create_default_pipeline():

    logger.info('---------------------------------------------')
    logger.info('Loading Inputdata...')
    network_input = NetworkInput()
    network_input.load_data_from_txt_file(settings.data_path)
    logger.info('---------------------------------------------')

    logger.info('Start creating Network...')
    network = Network(network_input)
    logger.info('---------------------------------------------')

    logger.info('Start solving MinCostFlow...')
    pipeline = SolvingPipeline(network)
    pipeline.transform_network(MaxFlowTransformer())

    if settings.solver_method == SolverMethod.Dinic:
        logger.info('Selected solver method: ' + settings.solver_method)
        pipeline.apply_solver(DinicSolver())
        export(pipeline, '/Dinic/MaxFlow')

    elif settings.solver_method == SolverMethod.Gurobi:
        logger.info('Selected solver method:' + settings.solver_method)
        pipeline.apply_solver(GurobiMaxFlowSolver())
        export(pipeline, '/Gurobi/MaxFlow')

    else:
        raise ValueError('Invalid solver method:' + settings.solver_method)

    pipeline.use_initial_network()
    pipeline.apply_solver(GurobiMinCostFlowSolver(
        settings.use_initial_solution))
    export(pipeline, '/Gurobi/MinCostFlow')

    return pipeline


def create_benchmark_pipeline():

    logger.info('---------------------------------------------')
    logger.info('Loading Inputdata...')
    network_input = NetworkInput()
    network_input.load_data_from_txt_file(settings.benchmark_path)
    logger.info('---------------------------------------------')

    logger.info('Start creating Network...')
    network = Network(network_input)
    logger.info('---------------------------------------------')

    pipeline = SolvingPipeline(network)

    pipeline.apply_solver(DinicSolver())
    export(pipeline, '/Benchmark/Dinic')

    pipeline.apply_solver(GurobiMaxFlowSolver())
    export(pipeline, '/Benchmark/Gurobi')

    return pipeline


if __name__ == '__main__':

    init_logging()
    start_time = time.time()

    if settings.run_benchmark:
        pipeline = create_benchmark_pipeline()
    else:
        pipeline = create_default_pipeline()

    pipeline.run()

    logger.success('Total time: ' + str(time.time() - start_time) + ' seconds')
