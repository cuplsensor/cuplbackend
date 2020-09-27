from . import ConsumerApiWrapper
import requests


class SampleWrapper(ConsumerApiWrapper):
    """Wraps samples endpoint of the Consumer API."""

    def get_samples(self,
                    serial: str,
                    starttime: str,
                    endtime: str,
                    page: int = 1,
                    per_page: int = 10000) -> list:
        """Get a list of temperature/humidity samples collected by a tag.

        A time window can be specified so that only samples that fall between starttime and endtime are returned.

        Makes a GET request to the :ref:`Samples <SamplesConsumerAPI>` endpoint.

        Args:
            serial (str): Base64 string. Identifies a tag to return samples from.
            starttime (str): Start datetime as an ISO-8601 string.
            endtime (str): End datetime as an ISO-8601 string.
            offset (int): Start list at the nth sample for pagination.
            limit (int): Limit the list length for pagination.

        Returns:
            list: A list of samples. Each is a dictionary.

        """
        samplesurl = "{apiurl}/tag/{serial}/samples".format(apiurl=self.apiurl,
                                                            serial=serial)

        payload = {
            'starttimestr': starttime,
            'endtimestr': endtime,
            'page': page,
            'per_page': per_page
        }

        # Using urlencode is important to remove the '+' and convert it to %2B. Date decode does
        # not work without it.
        r = requests.get(samplesurl, params=payload)
        r.raise_for_status()
        ConsumerApiWrapper.process_status(r.status_code)
        sample_response = r.json()
        return sample_response
