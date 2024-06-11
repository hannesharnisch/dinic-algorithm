import json
import random

from MinCostFlowProblemGenerator import MinCostFlowProblemGenerator


class TwoLayerCoherentNetworkGenerator(MinCostFlowProblemGenerator):
    def create_network(self, json_path, supplier_node_count, target_node_count):
        initial_data = {
            "nodes": {},
            "arcs": []
        }
        positive_list, negative_list = self.generate_balanced_lists(
            supplier_node_count, target_node_count)

        for i in range(supplier_node_count):
            initial_data["nodes"][str(i)] = {"demand": negative_list[i]}

        for i in range(target_node_count):
            initial_data["nodes"][str(
                i + supplier_node_count)] = {"demand": positive_list[i]}

        for i in range(supplier_node_count):
            for j in range(target_node_count):
                initial_data["arcs"].append(
                    {
                        "from": str(i),
                        "to": str(j + supplier_node_count),
                        "cost": random.randint(1, 10),
                        "lower_bound": 0,
                        "upper_bound": random.randint(1, 10)
                    }
                )
        self.save_json(json_path, initial_data)


if __name__ == "__main__":
    creator = TwoLayerCoherentNetworkGenerator()
    creator.create_network(
        "../Data/MinCost/sample_2_layer_coherent.json", 128, 128)
