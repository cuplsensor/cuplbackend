from . import ConsumerApiWrapper
import requests


class SampleWrapper(ConsumerApiWrapper):
    """Wraps samples endpoint of the Consumer API."""

    def get_samples(self,
                    serial: str,
                    starttime: str,
                    endtime: str,
                    offset: int = 0,
                    limit: int = None) -> list:
        """Get a list of temperature/humidity samples collected by a box.

        A time window can be specified so that only samples that fall between starttime and endtime are returned.

        Makes a GET request to the :ref:`Samples <SamplesConsumerAPI>` endpoint.

        Args:
            serial (str): Base64 string. Identifies a box to return samples from.
            starttime (str): Start datetime as an ISO-8601 string.
            endtime (str): End datetime as an ISO-8601 string.
            offset (int): Start list at the nth sample for pagination.
            limit (int): Limit the list length for pagination.

        Returns:
            list: A list of samples. Each is a dictionary.

        """
        samplesurl = "{apiurl}/samples".format(apiurl=self.apiurl)

        payload = {
            'serial': serial,
            'starttimestr': starttime,
            'endtimestr': endtime,
            'offset': offset
        }

        if limit is not None:
            payload['limit'] = limit

        # Using urlencode is important to remove the '+' and convert it to %2B. Date decode does
        # not work without it.
        r = requests.get(samplesurl, params=payload)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        sample_response = r.json()
        return sample_response
