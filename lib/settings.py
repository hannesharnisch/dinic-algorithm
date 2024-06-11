from enum import Enum
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = Path.joinpath(Path(__file__).parent.parent.resolve(), ".env")


class SolverMethod(str, Enum):
    Dinic = "Dinic"
    Gurobi = "Gurobi"


class Settings(BaseSettings):
    data_path: str = Field("Data/chvatal_small.json", env="DATA_PATH")
    solver_method: SolverMethod = Field(
        SolverMethod.Dinic, env="SOLVER_METHOD")
    plot_dinic_steps: bool = Field(False, env="PLOT_DINIC_STEPS")
    plot_output: bool = Field(False, env="PLOT_OUTPUT")
    use_initial_solution: bool = Field(False, env="USE_INITIAL_SOLUTION")
    grb_license_file: str = Field("", env="GRB_LICENSE_FILE")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    run_benchmark: bool = Field(False, env="RUN_BENCHMARK")
    benchmark_path: str = Field(env="BENCHMARK_PATH")

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
