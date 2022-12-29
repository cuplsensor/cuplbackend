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

from datetime import datetime, timedelta, time
from math import pi, sin


def time_to_radians(timeofday: time) -> float:
    """Maps from time to radians.

    00:00 -> 0 rad
    06:00 -> pi/2 rad
    12:00 -> pi rad
    18:00 -> 3*pi/2 rad

    Args:
        timeofday: Time of day in the range of 00:00 to 23:59

    Returns: Radians from 0 to 2*pi radians

    """
    secondsperday = timedelta(days=1).total_seconds()
    radianspersecond = 2*pi / secondsperday
    td_timeofday = timedelta(hours=timeofday.hour,
                             minutes=timeofday.minute,
                             seconds=timeofday.second)
    secondsofday = td_timeofday.total_seconds()

    return secondsofday * radianspersecond


def simsamples(tm=None,
               smplintervalmins: int = 10,
               nsamples: int = 144,
               valmax: float = 110,
               valmin: float = -10) -> (list, int):
    """
    Produce a list of samples, to simulate the output from a temperature or humidity sensor.

    These vary in a sine wave that ranges between valmax and valmin, according to the time of day. The function
    can be called at different times (tm) to see the effect of adding new samples and removing old ones.

    With all other parameters equal, a sample at a given point in time will not change,
    regardless of the number before or after. This mimics the behaviour of a cuplTag, which stores samples
    one-at-a-time on a circular buffer.

    :rtype: list, int
    :param tm: Time closest to the most recent sample. Defaults to now.
    :param smplintervalmins: Time difference between samples in minutes.
    :param nsamples: The number of samples to return.
    :param valmax: Maximum value of the sine wave.
    :param valmin: Minimum value of the sine wave.

    :return: A list of timestamped samples, with one value per sample. Sorted oldest first.
             timeoffset_mins is offset in minutes to the most recent sample.

    """
    tm = tm or datetime.utcnow()
    # First get the time rounded down to the closest time interval minutes
    # e.g. if time interval is 10 minutes and the time is 1652,
    # timeoffset_mins = 2 minutes
    timeoffset_mins = tm.minute % smplintervalmins
    tm_modinterval = timedelta(minutes=timeoffset_mins,
                               seconds=tm.second,
                               microseconds=tm.microsecond)

    tm_firstinterval = tm - tm_modinterval

    td_smplinterval = timedelta(minutes=smplintervalmins)

    smpl_list = list()

    # Make an array of times previous to it.
    for i in range(0, nsamples):
        tm_smpl = tm_firstinterval - i*td_smplinterval
        time_smpl = tm_smpl.time()
        rad_smpl = time_to_radians(time_smpl)
        valrange = valmax - valmin
        zsin_smpl = 0.5*sin(rad_smpl) + 0.5 # Scale sine function so it is between 0 and 1.
        val_smpl = valrange*zsin_smpl + valmin # Scale again
        smpl_list.insert(0, {"time": time_smpl, "rad": rad_smpl, "val": val_smpl})

    return smpl_list, timeoffset_mins


def trhsamples(tm=None,
               smplintervalmins: int = 10,
               nsamples: int = 144,
               tempmax: float = 110,
               tempmin: float = -10,
               rhmax: float = 100,
               rhmin: float = 0):
    """

    :rtype: list, int
    :param tm: Time closest to the most recent sample. Defaults to now.
    :param smplintervalmins: Time difference between samples in minutes.
    :param nsamples: The number of samples to return.
    :param tempmax: Maximum value of the temperature sine wave.
    :param tempmin: Minimum value of the temperature sine wave.
    :param rhmax: Maximum value of the relative humidity sine wave.
    :param rhmin: Minimum value of the relative humidity sine wave.
    :return: A list of timestamped samples, each containing temperature and humidity readings. Sorted oldest first.
             timeoffset_mins is the offset in minutes to the most recent sample.
    """
    tm = tm or datetime.utcnow()
    tempsim, _ = simsamples(tm=tm, smplintervalmins=smplintervalmins, nsamples=nsamples, valmax=tempmax, valmin=tempmin)
    rhsim, timeoffset_mins = simsamples(tm=tm, smplintervalmins=smplintervalmins, nsamples=nsamples, valmax=rhmax, valmin=rhmin)
    templist = [temp['val'] for temp in tempsim]
    rhlist = [rh['val'] for rh in rhsim]
    trhlist = [{'temp': temp, 'rh': rh} for temp, rh in zip(templist, rhlist)]
    return trhlist, timeoffset_mins


if __name__ == "__main__":
    now = datetime.now()
    time1610 = datetime(year=now.year, month=now.month, day=now.day, hour=16, minute=10, second=0)
    time1501 = datetime(year=now.year, month=now.month, day=now.day, hour=15, minute=1, second=0)
    trhlist, timeoffsetmins = trhsamples(tm=time1501)
    print(trhlist)
    print(timeoffsetmins)
    trhlist, timeoffsetmins = trhsamples(tm=time1610)
    print(trhlist)