import requests

class WaterQuality:
    """Implement GET queries in Drinking Water Quality API.

    Attributes
    ----------
    timeout : float, optional
        Timeout for requests, in seconds
    """
    BASE_URI = "https://api.euskadi.eus/water-quality"
    HEADERS = {"accept": "application/json"}

    def __init__(self, timeout=None):
        self.timeout = timeout

    def _get_complete_url(self, path):
        return f"{WaterQuality.BASE_URI}/{path}"

    def _request(self, path, params=None):
        url = self._get_complete_url(path)

        response = requests.get(url,
                                params=params,
                                headers=WaterQuality.HEADERS,
                                timeout=self.timeout
                                )
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.json()

    def find_sampling_points(self, county_id, municipality_id, **kwargs):
        """Find sampling points by province id and municipality id.

        Parameters
        ----------
        county_id: str
            The identifier of the province
        municipality_id: str
            The identifier of the municipality
        **kwargs
            currentPage: int, number of current page. Default value "1"
            itemsOfPage: int, the number of items to be displayed on the page. Default value "10"
            format: {"json", "geojson"}
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        list of dict
            Representation of the JSON returned from the API.
        """
        path = f"sampling-points/counties/{county_id}/municipalities/{municipality_id}"
        return self._request(path, kwargs)

    def get_measurements(self, point, **kwargs):
        """Get all measurements by sampling point.

        Parameters
        ----------
        point : str
            The identifier of the sampling point
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"sampling-points/{point}/measurements"
        return self._request(path, kwargs)
        
    def get_analytical_data(self, point, measurement, **kwargs):
        """Get analytical data by sampling point and measurement.

        Parameters
        ----------
        point : str
            The identifier of the sampling point
        measurement : str
            The date of the measurement
        **kwargs
            lang: {"SPANISH", "BASQUE"}

        Returns
        -------
        dict
            Representation of the JSON returned from the API.
        """
        path = f"sampling-points/{point}/measurements/{measurement}/analytical-data"
        return self._request(path, kwargs)