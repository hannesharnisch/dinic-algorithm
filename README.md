# Dinic Algorithm

## Requirements

- Docker running
- Devcontainer VSCode extension installed

[Don't know how to use devcontainer?](https://microsoft.github.io/vscode-essentials/en/09-dev-containers.html)

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
