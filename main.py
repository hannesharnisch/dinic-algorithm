import time
from lib.settings import Settings
from lib.networkInput import NetworkInput
from lib.network import Network
from lib import helper

#from lib.xxSolver import XXSolver
#from lib.yySolver import YYSolver


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
    if settings.get_solver_method() ==  'XX':
        print('Selected solover method:' + settings.get_solver_method())
        #network_flow = XXSolver.solve(network)
    elif settings.get_solver_method() == 'YY':
        print('Selected solover method:' + settings.get_solver_method())
        #network_flow = YYSolver.solve(network)
    else:
        raise ValueError('Invalid solver method:' + settings.get_solver_method())
    print('Done')
    print('Generating output...')
    #helper.save_network_flow(network_flow)
    print('Done')
    print('Total time: ' + str(time.time() - start_time) + ' seconds')
