import random

from MinCostFlowProblemGenerator import MinCostFlowProblemGenerator


class TwoLayerNetworkGenerator(MinCostFlowProblemGenerator):
    def create_network(self, json_path: str, supplier_node_count: int, target_node_count: int):
        initial_data = {
            "nodes": {},
            "arcs": []
        }
        positive_list, negative_list = self.generate_balanced_lists(supplier_node_count, target_node_count)

        for i in range(supplier_node_count):
            initial_data["nodes"][str(i)] = {"demand": negative_list[i]}

        for i in range(target_node_count):
            initial_data["nodes"][str(i + supplier_node_count)] = {"demand": positive_list[i]}

        n = supplier_node_count + target_node_count

        for i in range(2*n-3):
            initial_data["arcs"].append(
                {
                    "from": str(random.randint(0, supplier_node_count-1)),
                    "to": str(random.randint(supplier_node_count, supplier_node_count+target_node_count-1)),
                    "cost": random.randint(1, 10),
                    "lower_bound": 0,
                    "upper_bound": random.randint(1, 10)
                }
            )

        self.save_json(json_path, initial_data)

if __name__ == "__main__":
    generator = TwoLayerNetworkGenerator()
    generator.create_network("../Data/sample_2_layer.json", 128,128)