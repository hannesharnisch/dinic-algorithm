# Dinic Algorithm

## Requirements

- Docker running
- Devcontainer VSCode extension installed

[Don't know how to use devcontainer?](https://microsoft.github.io/vscode-essentials/en/09-dev-containers.html)

### If used without Devcontainer

- Install requirements

  `pip3 install --user -r requirements.txt`
- Set GRB_LICENSE_FILE env variable

  `"GRB_LICENSE_FILE": "/workspaces/dinic/gurobi.lic"`

## Quickstart

- run main.py

  `python3 ./main.py`
- run benchmarks

  `python3 ./benchmarks/max_flow_benchmark.py`

  `python3 ./benchmarks/min_cost_flow_benchmark.py`
  >Note: Select data path `data_path` and iterations `times_to_test` at the end of the file
## .env file

```
DATA_PATH: Data path of instance to solve
SOLVER_METHOD: Dinic | Gurob
PLOT_DINIC_STEPS: Plot every dinic iteration
PLOT_OUTPUT: Plot the final flow after solving max and min flow
USE_INITIAL_SOLUTION: Should Gurobi Min Cost use the initial sulution
LOG_LEVEL: DEBUG | INFO | WARNING | ERROR | CRITICAL
RUN_BENCHMARK: The max flow problem is solved by both gurobi and dinic
BENCHMARK_PATH: Path to the max flow problem
```

## Output

### Structure:
- Benchmark
  - Dinic.json
  - Gurobi.json
- Dinic
  - Steps
    - iteration_x.png
  - MaxFlow.json
  - MaxFlow.png
- Gurobi
  - MaxFlow.json
  - MaxFlow.png
  - MinCostFlow.json
  - MinCostFlow.json
