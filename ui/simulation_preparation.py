import json
import streamlit

from input_creation import (
    InputBuffer,
    InputSkyCarSetup,
    InputSMObstacles,
    InputTCObstacles,
    InputZonesAndStations,
    InputJobs,
)
from core.parameters import Parameters
from ui.grid_designer import GridDesignerUI
from ui.simulation_input import SimulationInputUI


class SimulationPreparationUI:
    def __init__(
        self, grid_designer_ui: GridDesignerUI, simulation_input_ui: SimulationInputUI
    ):
        self.grid_designer_ui = grid_designer_ui
        self.simulation_input_ui = simulation_input_ui

    def show(self) -> bool:
        streamlit.write("## Simulation Preparation")

        input_zones_and_stations = InputZonesAndStations(
            grid_designer_ui=self.grid_designer_ui
        )
        with streamlit.expander("reset-2.json: Zones and Stations"):
            json_data = input_zones_and_stations.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-2.json"
            )

        input_sm_obstacles = InputSMObstacles(grid_designer_ui=self.grid_designer_ui)
        with streamlit.expander("reset-3.json: SM Obstacles"):
            json_data = input_sm_obstacles.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-3.json"
            )

        input_buffer = InputBuffer(buffer_ratio=self.grid_designer_ui.buffer_ratio)
        with streamlit.expander("reset-4.json: Buffer"):
            json_data = input_buffer.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-4.json"
            )

        input_skycar_setup = InputSkyCarSetup(
            number_of_skycars=self.simulation_input_ui.number_of_skycars,
            model=Parameters.ZONE_NAME,
        )
        with streamlit.expander("reset-5.json: Skycar Setup"):
            json_data = input_skycar_setup.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-5.json"
            )

        input_tc_obstacles = InputTCObstacles(grid_designer_ui=self.grid_designer_ui)
        with streamlit.expander("reset-6.json: TC Obstacles"):
            json_data = input_tc_obstacles.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-6.json"
            )

        input_jobs = InputJobs(
            grid_designer_ui=self.grid_designer_ui,
            simulation_input_ui=self.simulation_input_ui,
            input_zones_and_stations=input_zones_and_stations,
        )
        with streamlit.expander("reset-job.json: Job Parameters"):
            json_data = input_jobs.to_json()
            self._show_individual_json_file(
                json_data=json_data, file_name="reset-job.json"
            )

        server_number = streamlit.selectbox(
            "Choose a server to run the simulation on.",
            [1, 2],
            index=None,
            placeholder="Select server...",
        )
        if server_number is None:
            return False

        self.input_zones_and_stations = input_zones_and_stations
        self.input_sm_obstacles = input_sm_obstacles
        self.input_buffer = input_buffer
        self.input_skycar_setup = input_skycar_setup
        self.input_tc_obstacles = input_tc_obstacles
        self.input_jobs = input_jobs
        self.server_number = server_number

        return True

    def _show_individual_json_file(self, json_data: str, file_name: str):
        streamlit.download_button(
            label="Download",
            data=json_data,
            file_name=file_name,
            mime="application/json",
            type="primary",
        )
        streamlit.json(json_data)
