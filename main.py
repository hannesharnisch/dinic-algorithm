import time
from lib.settings import Settings
from lib.networkInput import NetworkInput
from lib.network.network import Network
from lib import helper
from lib.solver.dinicSolver import DinicSolver
from lib.solver.gurobiInitialSolver import GurobiInitialSolver
from lib.solver.gurobiNetworkSimplexSolver import GurobiNetworkSimplexSolver
from lib.solvingPipeline import SolvingPipeline
from lib.transformer.maxFlowTransformer import MaxFlowTransformer
from lib.transformer.minCostFlowTransformer import MinCostFlowTransformer


if __name__ == '__main__':
    start_time = time.time()
    print('Loading settings...')
    settings = Settings()
    settings.import_settings_from_txt_file()
    print('Done')
    print('Loading Inputdata...')
    network_input = NetworkInput()
    network_input.load_data_from_txt_file(settings.get_data_path())
    print('Done')
    print('Start creating Network...')
    network = Network(network_input)
    print('Done')
    print('Start solving MinCostFlow...')
    pipeline = SolvingPipeline(network)
    pipeline.transformNetwork(MaxFlowTransformer())
    if settings.get_solver_method() ==  'Dinic':
        print('Selected solover method: ' + settings.get_solver_method())
        pipeline.applySolver(DinicSolver())
    elif settings.get_solver_method() == 'Gurobi':
        print('Selected solover method:' + settings.get_solver_method())
        pipeline.applySolver(GurobiInitialSolver())
    else:
        raise ValueError('Invalid solver method:' + settings.get_solver_method())
    pipeline.transformNetwork(MinCostFlowTransformer())
    pipeline.applySolver(GurobiNetworkSimplexSolver())
    pipeline.run()
    network_flow = pipeline.result
    print('Done')
    print('Generating output...')
    helper.save_network_flow(network_flow)
    print('Done')
    print('Total time: ' + str(time.time() - start_time) + ' seconds')
