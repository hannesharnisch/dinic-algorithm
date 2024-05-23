class Settings:
  def __init__(self):
    self.__data_path = ''
    self.__solver_method = ''

  def get_data_path(self):
    return self.__data_path
  
  def get_solver_method(self):
    return self.__solver_method
  
  def import_settings_from_txt_file(self, settings_extension = ""):
    print('Importing settings...')
    settings_file_name = "settings" + settings_extension + ".txt"
    settings_file = open(settings_file_name, 'r')
    settings_dict = {'data_path' : ''
                     ,'solver_method' : ''
                    }       
    for line in settings_file:
      key = line.partition(' ')[0]
      if key in settings_dict:
        if type(settings_dict[key]) is int:
          settings_dict[key] = int(line.partition('[')[-1].partition(']')[0])
        elif type(settings_dict[key]) is bool:
          settings_dict[key] = line.partition('[')[-1].partition(']')[0] == 'True'
        elif type(settings_dict[key]) is float:
          settings_dict[key] = float(line.partition('[')[-1].partition(']')[0])
        else:
          settings_dict[key] = line.partition('[')[-1].partition(']')[0]
          
    self.__data_path = settings_dict['data_path']
    self.__solver_method = settings_dict['solver_method']