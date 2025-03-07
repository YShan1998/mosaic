import json
from typing import List

from input_creation.input_zones import InputZonesAndStations
from core.parameters import Parameters
from ui.grid_designer import GridDesignerUI
from ui.simulation_input import SimulationInputUI

SIMULATION_DURATION_IN_HOURS: int = 5


class InputJobs:
    def __init__(
        self,
        grid_designer_ui: GridDesignerUI,
        simulation_input_ui: SimulationInputUI,
        input_zones_and_stations: InputZonesAndStations,
    ):
        self.mode = "CONTINUOUS"
        self.allowCrossZoneGroup = False
        self.enableAutoStore = False
        self.pickFromZoneGroups = [Parameters.ZONE_NAME]
        self.minLayer = 0
        self.maxLayer = grid_designer_ui.z_size
        self.stations = self._get_list_of_stations(
            input_zones_and_stations=input_zones_and_stations
        )
        self.qty = (
            len(self.stations)
            * simulation_input_ui.goods_in_throughput
            * SIMULATION_DURATION_IN_HOURS
        )

    def _get_list_of_stations(
        self, input_zones_and_stations: InputZonesAndStations
    ) -> List[int]:
        return [station.code for station in input_zones_and_stations.stations]

    def to_json(
        self, save: bool = False, filename: str = "reset-job.json", type: str = "str"
    ) -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        if type == "str":
            return json_str
        elif type == "dict":
            return json.loads(json_str)
