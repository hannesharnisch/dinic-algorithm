import os
import time
from lib.exporter.plotExporter import PlotExporter
from lib.exporter.textExporter import TextExporter
from lib.settings import Settings
from lib.networkInput import NetworkInput
from lib.network.network import Network
from lib import helper
from lib.solver.dinicSolver import DinicSolver
from lib.solver.gurobiMaxFlowSolver import GurobiMaxFlowSolver
from lib.solver.gurobiMinCostFlowSolver import GurobiMinCostFlowSolver
from lib.solvingPipeline import SolvingPipeline
from lib.transformer.maxFlowTransformer import MaxFlowTransformer
from lib.transformer.minCostFlowTransformer import MinCostFlowTransformer


if __name__ == '__main__':
    # Check if the Gurobi license file exists
    if os.path.isfile('/workspaces/dinic-algorithm/gurobi.lic'):
        # Set the environment variable for Gurobi
        os.environ['GRB_LICENSE_FILE'] = '/workspaces/dinic-algorithm/gurobi.lic'

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
    pipeline.transform_network(MaxFlowTransformer())
    if settings.get_solver_method() ==  'Dinic':
        print('Selected solver method: ' + settings.get_solver_method())
        pipeline.apply_solver(DinicSolver())
        pipeline.export_to_file(TextExporter(), '/Dinic/MaxFlow')
        pipeline.export_to_file(PlotExporter(), '/Dinic/MaxFlow')
    elif settings.get_solver_method() == 'Gurobi':
        print('Selected solver method:' + settings.get_solver_method())
        pipeline.apply_solver(GurobiMaxFlowSolver())
        pipeline.export_to_file(TextExporter(), '/Gurobi/MaxFlow')
        pipeline.export_to_file(PlotExporter(), '/Gurobi/MaxFlow')
    else:
        raise ValueError('Invalid solver method:' + settings.get_solver_method())
    pipeline.use_initial_network()
    pipeline.apply_solver(GurobiMinCostFlowSolver())
    pipeline.export_to_file(PlotExporter(), '/Gurobi/MinCostFlow')
    pipeline.export_to_file(TextExporter(), '/Gurobi/MinCostFlow')
    pipeline.run(debug=False)
    network_flow = pipeline.result
    print('Done')
    print('Generating output...')
    helper.save_network_flow(network_flow)
    print('Done')
    print('Total time: ' + str(time.time() - start_time) + ' seconds')
