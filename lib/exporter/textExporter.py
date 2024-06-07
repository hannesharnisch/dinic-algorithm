
import os
from typing import Tuple

from loguru import logger
from lib.exporter.exporter import Exporter
from lib.network.graph.identifiable import NodeID
from lib.solver.solverState import SolverState
import json

class TextExporter(Exporter):

    def __init__(self):
        pass

    def export(self, state: SolverState, file_name: str="result") -> str:
        
        logger.info("writing to file...")

        res = {
            "target_value": state.solution.target_value,
            "calc_duration": state.solution.calc_duration.total_seconds(),
            "flow": self.remap_keys(state.solution.flow),
        }

        file_path = f'./Output/{file_name}.json'

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)

        return state
    
    def remap_keys(self, mapping: dict[Tuple[NodeID, NodeID], int] ) -> dict:
        return [{'arc':k, 'flow': v} for k, v in mapping.items()]
    