import json
import random
from abc import abstractmethod


class MinCostFlowProblemGenerator:
    def __init__(self):
        pass

    @abstractmethod
    def create_network(self, json_path: str, supplier_node_count: int, target_node_count: int):
        pass

    def generate_balanced_lists(self, an: int, bn: int):
        if an == 0 or bn == 0:
            raise ValueError("Both list lengths must be greater than zero.")

        # Generate random positive integers for the positive list
        pos_list = [random.randint(1, 100) for _ in range(bn)]
        sum_pos = sum(pos_list)

        # Generate random negative integers for the negative list
        neg_list = []
        remaining_sum = sum_pos

        for i in range(an - 1):
            neg_value = random.randint(1, remaining_sum // (an - i))
            neg_list.append(-neg_value)
            remaining_sum -= neg_value

        # Adjust the last element to ensure the sum is exactly -sum_pos
        neg_list.append(-remaining_sum)

        return pos_list, neg_list

    def save_json(self, path: str, json_to_be_saved: dict[str, list | dict]):
        with open(path, 'w') as json_file:
            json.dump(json_to_be_saved, json_file, indent=4)
        print("JSON-file was successfully saved.")
