import json


class WaissiProblemGenerator:
    def create_waissi(self, n: int):
        initial_data = {
            "nodes": {},
            "arcs": []
        }

        initial_data["nodes"]["s"] = {"demand": 0}
        initial_data["nodes"]["t"] = {"demand": 0}

        initial_data["arcs"].append(
            {
                "from": "s",
                "to": "t",
                "cost": 0,
                "lower_bound": 0,
                "upper_bound": 1
            }
        )

        for i in range(2, n):
            initial_data["nodes"][str(i)] = {"demand": 0}
            if i == 2:
                initial_data["arcs"].append(
                    {
                        "from": "s",
                        "to": str(i),
                        "cost": 0,
                        "lower_bound": 0,
                        "upper_bound": n
                    }
                )
            else:
                initial_data["arcs"].append(
                    {
                        "from": str(i - 1),
                        "to": str(i),
                        "cost": 0,
                        "lower_bound": 0,
                        "upper_bound": n
                    }
                )
            initial_data["arcs"].append(
                {
                    "from": str(i),
                    "to": "t",
                    "cost": 0,
                    "lower_bound": 0,
                    "upper_bound": 1
                }
            )

        print(f"Number of nodes: {len(initial_data['nodes'].keys())}")
        print(f"Number of arcs: {len(initial_data['arcs'])}")

        with open("../Data/MaxFlow/waissi.json", 'w') as json_file:
            json.dump(initial_data, json_file, indent=4)
        print("JSON-file was successfully saved.")


if __name__ == "__main__":
    generator = WaissiProblemGenerator()
    generator.create_waissi(256)
