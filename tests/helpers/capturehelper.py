#  A web application that stores samples from a collection of NFC sensors.
#
#  https://github.com/cuplsensor/cuplbackend
#
#  Original Author: Malcolm Mackay
#  Email: malcolm@plotsensor.com
#  Website: https://cupl.co.uk
#
#  Copyright (c) 2021. Plotsensor Ltd.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the
#  GNU Affero General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from datetime import timedelta
import pytz
import random
from string import ascii_lowercase
from tests.apiwrapper.admin.capture import CaptureWrapper
from tests.apiwrapper.consumer.capture import CaptureWrapper as ConsumerCaptureWrapper

tz = pytz.timezone("Europe/London")


class CaptureHelper:
    def makesamples(self, starttime, timeintmins, nsamples):
        temp = 0
        smpltime = starttime
        samplelist = []
        for x in range(0, nsamples):
            samplelist.append({
                "temp": temp,
                "timestamp": smpltime.astimezone(tz).isoformat()
            })
            temp += 1
            smpltime += timedelta(minutes=timeintmins)
        return samplelist

    def makecapture(self, samples, timeintmins, tag_id):
        capture = {
            "batvoltagemv": 3000,
            "tag_id": tag_id,
            "cursorpos": 10,
            "loopcount": 20,
            "hash": ''.join(random.choice(ascii_lowercase) for i in range(8)),
            "samples": samples,
            "status": {
                "brownout": False,
                "clockfail": False,
                "lpm5wakeup": False,
                "misc": False,
                "resetsalltime": 120,
                "supervisor": False,
                "watchdog": False
            },
            "timeintmins": timeintmins,
            "timestamp": samples[-1]['timestamp'],
            "format": "TempRH_URL"
        }
        return capture



    def make_capture_with_samples(self, starttime, tag_id, timeintmins=12, nsamples=4):
        samples = self.makesamples(starttime, timeintmins, nsamples)
        return self.makecapture(samples, timeintmins, tag_id)

    def __init__(self):
        super().__init__()


class CaptureListHelper(CaptureHelper):
    def __init__(self, baseurl, adminapi_token, capturespeclist, tagid, timeintmins=12):
        super().__init__()
        self.capturelist = []
        self.writtencaptures = []
        alltimestamps = []
        capturewrapper = CaptureWrapper(baseurl, adminapi_token)
        consumercapturewrapper = ConsumerCaptureWrapper(baseurl)


        for capturespec in capturespeclist:
            capture = self.make_capture_with_samples(starttime=capturespec['starttime'],
                                                     tag_id=tagid,
                                                     timeintmins=timeintmins,
                                                     nsamples=capturespec['nsamples'])

            writtencapture = capturewrapper.post(capture)

            samples = consumercapturewrapper.get_samples(capture_id=writtencapture['id'])

            # Make a list of all timestamps to find the maximum and minimum
            timestamps = [sample['timestamp'] for sample in samples]
            alltimestamps.extend(timestamps)

            self.capturelist.append(capture)
            self.writtencaptures.append(writtencapture)

        self.mints = min(alltimestamps)
        self.maxts = max(alltimestamps)

