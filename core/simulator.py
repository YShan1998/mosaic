from typing import Any, Dict, Optional

import requests
import streamlit

from core.config import SM_BASE_1, SM_BASE_2, TC_BASE_1, TC_BASE_2
from ui.simulation_preparation import SimulationPreparationUI


class Simulator:

    def __init__(self, simulation_preparation_ui: SimulationPreparationUI):
        self.simulation_preparation_ui = simulation_preparation_ui
        self._set_server()

    def run(self):
        steps = [
            ("Reset Layout", self._reset_layout),
            ("Initialise Setup", self._initialise_setup),
            ("Configure SM Obstacles", self._configure_SM_obstacles),
            ("Configure Layout", self._configure_layout),
            ("Configure Skycar Setup", self._configure_skycar_setup),
            ("Configure TC Obstacles", self._configure_TC_obstacles),
            ("Start Cube", self._start_cube),
            ("Send Jobs", self._send_jobs),
        ]

        progress_bar = streamlit.progress(0)
        status_text = streamlit.empty()

        for i, (step_name, step_func) in enumerate(steps):
            status_text.text(f"Running: {step_name}")
            _ = step_func()
            progress_bar.progress((i + 1) / len(steps))

        status_text.text("Simulation setup complete!")

    def _set_server(self):
        if self.simulation_preparation_ui.server_number == 1:
            self.SM_BASE = SM_BASE_1
            self.TC_BASE = TC_BASE_1
        else:
            self.SM_BASE = SM_BASE_2
            self.TC_BASE = TC_BASE_2

    def _reset_layout(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.SM_BASE}/v3/initialize/reset",
            method="POST",
        )
        return response

    def _initialise_setup(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.SM_BASE}/v3/initialize",
            method="POST",
            data=self.simulation_preparation_ui.input_zones_and_stations.to_json(
                type="dict"
            ),
        )
        return response

    def _configure_SM_obstacles(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.SM_BASE}/v3/obstacles",
            method="POST",
            data=self.simulation_preparation_ui.input_sm_obstacles.to_json(type="dict"),
        )
        return response

    def _configure_layout(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.SM_BASE}/v3/initialize/storage",
            method="POST",
            data=self.simulation_preparation_ui.input_buffer.to_json(type="dict"),
        )
        return response

    def _configure_skycar_setup(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.TC_BASE}/simulation/seed-skycars",
            method="POST",
            data=self.simulation_preparation_ui.input_skycar_setup.to_json(type="dict"),
        )
        return response

    def _configure_TC_obstacles(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.TC_BASE}/wcs/obstacle",
            method="POST",
            data=self.simulation_preparation_ui.input_tc_obstacles.to_json(type="dict"),
        )
        return response

    def _start_cube(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.TC_BASE}/operation/cube?start=true&bypass=true",
            method="POST",
        )
        return response

    def _send_jobs(self) -> requests.Response:
        response = self._send_request(
            url=f"{self.SM_BASE}/v3/dry-runs",
            method="POST",
            data=self.simulation_preparation_ui.input_jobs.to_json(type="dict"),
        )
        return response

    def _send_request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Send an HTTP request to the specified endpoint.

        Parameters
        ----------
        endpoint : str
            The API endpoint to send the request to
        method : str, optional
            The HTTP method to use (GET, POST, PUT, DELETE, etc.)
        data : Dict[str, Any], optional
            The data to send in the request body
        params : Dict[str, Any], optional
            The URL parameters to include
        headers : Dict[str, Any], optional
            The headers to include in the request

        Returns
        -------
        requests.Response
            The response from the server

        Raises
        ------
        requests.exceptions.RequestException
            If the request fails
        """

        if headers is None:
            headers = {"Content-Type": "application/json"}

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
