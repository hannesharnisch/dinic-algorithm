import subprocess
import json
import os
from functools import reduce

"""
    This file is a benchmark test. You can specify the problem to be tested and the times it should run.
"""


def run_pipeline(method, data_path):
    update_env_file('.env', 'RUN_BENCHMARK', "False")
    if method == "Dinic" or method == "Gurobi":
        update_env_file('.env', 'DATA_PATH', data_path)
        update_env_file('.env', 'SOLVER_METHOD', method)
    else:
        update_env_file('.env', 'DATA_PATH', data_path)
        update_env_file('.env', 'USE_INITIAL_SOLUTION', "False")

    run_command("python main.py")

    return read_output_and_get_runtime(method)


def get_json_value(file_path, key):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Retrieve the value for the given key
    value = data.get(key, None)

    return value


def read_output_and_get_runtime(method):
    if method == "Dinic" or method == "Gurobi":
        maxFlowPath = os.path.dirname(
            __file__) + f"/../Output/{method}/MaxFlow.json"
        maxFlowTime = get_json_value(maxFlowPath, "calc_duration")
    else:
        maxFlowTime = 0

    minFlowPath = os.path.dirname(
        __file__) + f"/../Output/Gurobi/MinCostFlow.json"
    minFlowTime = get_json_value(minFlowPath, "calc_duration")

    return {
        "maxFlowTime": maxFlowTime,
        "minFlowTime": minFlowTime,
        "totalTime": maxFlowTime + minFlowTime
    }


def update_env_file(file_path, variable_name, new_value):
    # Read the current content of the .env file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the DATA_PATH variable if it exists, otherwise add it
    variable_found = False
    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith(variable_name + '='):
                file.write(f"{variable_name}={new_value}\n")
                variable_found = True
            else:
                file.write(line)
        if not variable_found:
            file.write(f"{variable_name}={new_value}\n")


def run_command(command):
    try:
        # Execute the command
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the standard output and error
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')

        # Print the outputs
        if stderr:
            raise Exception("Error occurred while solving one pipeline")

        return stdout, stderr
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command:", e)
        return None, str(e)


def calcAverages(timeResultList):
    def sumTotalTimeFunc(a, b):
        return {"totalTime": a["totalTime"] + b["totalTime"]}

    def sumMaxFlowTime(a, b):
        return {"maxFlowTime": a["maxFlowTime"] + b["maxFlowTime"]}

    def sumMinFlowTime(a, b):
        return {"minFlowTime": a["minFlowTime"] + b["minFlowTime"]}

    sumTotalTime = reduce(sumTotalTimeFunc, timeResultList)
    sumMaxFlowTime = reduce(sumMaxFlowTime, timeResultList)
    sumMinFlowTime = reduce(sumMinFlowTime, timeResultList)

    return {
        "averageMaxFlowTime": sumMaxFlowTime["maxFlowTime"]/len(timeResultList),
        "averageMinFlowTime": sumMinFlowTime["minFlowTime"]/len(timeResultList),
        "averageTotalTime": sumTotalTime["totalTime"]/len(timeResultList)
    }


def convert_to_milliseconds(time_dict):
    return {key: f"{value * 1000} ms" for key, value in time_dict.items()}


if __name__ == "__main__":
    data_path = "Data/MinCost/chvatal_small.json"
    times_to_test = 10

    dinicResults = []
    for i in range(times_to_test):
        dinicResults.append(run_pipeline("Dinic", data_path))

    dinicResult = convert_to_milliseconds(calcAverages(dinicResults))
    print("DINIC RESULT")
    print(dinicResult)

    gurobiResults = []
    for i in range(times_to_test):
        gurobiResults.append(run_pipeline("Gurobi", data_path))
    gurobiResult = convert_to_milliseconds(calcAverages(gurobiResults))
    print("Gurobi RESULT")
    print(gurobiResult)

    withoutInitalSoultionResults = []
    for i in range(times_to_test):
        withoutInitalSoultionResults.append(
            run_pipeline("NoInitial", data_path))

    withoutInitalSoultionResult = convert_to_milliseconds(
        calcAverages(withoutInitalSoultionResults))
    print("WithoutInitialSoultion RESULT")
    print(withoutInitalSoultionResult)
