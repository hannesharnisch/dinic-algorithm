import subprocess
import json
import os


def run_pipeline(data_path):
    update_env_file('../.env', 'RUN_BENCHMARK', 'TRUE')
    update_env_file('../.env', 'BENCHMARK_PATH', data_path)

    run_command("python main.py")

    return {
        "Dinic": read_output_and_get_runtime("Dinic"),
        "Gurobi": read_output_and_get_runtime("Gurobi"),
    }


def read_output_and_get_runtime(method):
    maxFlowPath = os.path.dirname(__file__) + f"/Output/Benchmark/{method}.json"
    maxFlowTime = get_json_value(maxFlowPath, "calc_duration") * 1000
    return maxFlowTime


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
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    result_sum = sum(timeResultList)
    return result_sum / len(timeResultList)


def get_json_value(file_path, key):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Retrieve the value for the given key
    value = data.get(key, None)

    return value


def convert_to_milliseconds(time_dict):
    return {key: f"{value * 1000} ms" for key, value in time_dict.items()}


if __name__ == "__main__":
    data_path = "../Data/MaxFlow/reference_problem.json"
    times_to_test = 10

    results = []
    for i in range(times_to_test):
        results.append(run_pipeline(data_path))

    dinic_results = []
    gurobi_results = []

    for result in results:
        dinic_results.append(result["Dinic"])
        gurobi_results.append(result["Gurobi"])

    dinic_avg = calcAverages(dinic_results)
    gurobi_avg = calcAverages(gurobi_results)

    print("Dinic Average:")
    print(f"{dinic_avg} ms")

    print("Gurobi Average:")
    print(f"{gurobi_avg} ms")
