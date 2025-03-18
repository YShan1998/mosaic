import json
from typing import Any, Dict, Optional

import requests
import streamlit


class MosaicRequest:
    @staticmethod
    def health_check(TC_base: str) -> bool | None:
        try:
            response = MosaicRequest.send_request(
                url=f"{TC_base}/operation/healthcheck", method="GET", timeout=1
            )
            real_response = json.loads(response.text)
            return real_response["model"]["cycle_stop"]["status"]

        except requests.exceptions.RequestException as _:
            streamlit.warning("Server is unavailable.")
            return None

    @staticmethod
    def stop(TC_base: str) -> requests.Response | None:
        try:
            response = MosaicRequest.send_request(
                url=f"{TC_base}/operation/cyclestop",
                data={
                    "status": "Enabled",
                    "reason": "Matrix simulation has stopped the simulation.",
                },
            )
            streamlit.success("Simulation stopped successfully.", icon="✅")
            return response
        except requests.exceptions.RequestException as _:
            streamlit.warning(
                "Failed to stop simulation, or there is no simulation to be stopped.",
                icon="⚠️",
            )
            return None

    @staticmethod
    def send_request(
        url: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int | None = None,
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
        timeout : int, optional
            The timeout for the request

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
                timeout=timeout,
            )
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
