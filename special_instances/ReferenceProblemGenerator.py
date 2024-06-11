import json

class ReferenceProblemGenerator:
    def create_reference_problem(self, n):
        if (n % 2 == 1):
            raise Exception("n must be even")

        initial_data = {
            "nodes": {},
            "arcs": []
        }

        initial_data["nodes"]["s"] = {"demand": 0}
        initial_data["nodes"]["t"] = {"demand": 0}

        level_node_count = int(n/2 - 1)

        for i in range(level_node_count):
            initial_data["nodes"][str(i)] = {"demand": 0}
            initial_data["nodes"][str(i+level_node_count)] = {"demand": 0}
            initial_data["arcs"].append(
                {
                    "from": str(i),
                    "to": str(i+level_node_count),
                    "cost": 0,
                    "lower_bound": 0,
                    "upper_bound": 1
                }
            )
            initial_data["arcs"].append(
                {
                    "from": "s",
                    "to": str(i),
                    "cost": 0,
                    "lower_bound": 0,
                    "upper_bound": n
                }
            )
            initial_data["arcs"].append(
                {
                    "from": str(i+level_node_count),
                    "to": "t",
                    "cost": 0,
                    "lower_bound": 0,
                    "upper_bound": n
                }
            )

        # Add additional nodes
        for i in range(int(n/2)):
            initial_data["arcs"].append(
                {
                    "from": str(i),
                    "to": str(int((i+level_node_count+1) % n-2)),
                    "cost": 0,
                    "lower_bound": 0,
                    "upper_bound": 1
                }
            )

        print(f"Number of nodes: {len(initial_data['nodes'].keys())}")
        print(f"Number of arcs: {len(initial_data['arcs'])}")

        with open("../Data/MaxFlow/reference_problem.json", 'w') as json_file:
            json.dump(initial_data, json_file, indent=4)
        print("JSON-file was successfully saved.")

if __name__ == "__main__":
    generator = ReferenceProblemGenerator()
    generator.create_reference_problem(256)