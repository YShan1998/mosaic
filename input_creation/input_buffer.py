import json
from core.parameters import Parameters


class InputBuffer:
    def __init__(self, buffer_ratio: float):
        self.percentage = round(buffer_ratio, 2)
        self.zoneGroup = Parameters.ZONE_NAME

    def to_json(self, save: bool = False, filename: str = "reset-4.json") -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        return json_str
