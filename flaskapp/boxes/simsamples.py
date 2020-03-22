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


def simsamples(tm=datetime.utcnow(), smplintervalmins: int=10, nsamples: int=144, valmax: float=110, valmin: float=-10):
    """Produces a list of simulated samples prior to a given time (now by default).
    These vary in a sine wave scaled between valmax and valmin, according to the time of day.

    The purpose of this function is to produce a virtual sensor. Data for previous timestamps will not change each time
     the function is run.

    Args:
        tm: time of the most recent sensor sample
        smplintervalmins: time difference between sensor samples in minutes
        nsamples: number of samples to output including the most recent
        valmax: maximum value of the sine wave
        valmin: minimum value of the sine wave

    Returns:
        A list of samples. If the product of smplintervalmins and nsamples is 24 hours, these will range between
        valmax and valmin.

    """
    # First get the time rounded down to the closest time interval minutes
    # e.g. if time interval is 10 minutes and the time is 1652,
    # tm_modinterval = 2 minutes
    tm_modinterval = timedelta(minutes=tm.minute % smplintervalmins,
                               seconds=tm.second,
                               microseconds=tm.microsecond)

    tm_firstinterval = tm - tm_modinterval

    td_smplinterval = timedelta(minutes=smplintervalmins)

    # Make an array of times previous to it.
    for i in range(0, nsamples):
        tm_smpl = tm_firstinterval - i*td_smplinterval
        time_smpl = tm_smpl.time()
        rad_smpl = time_to_radians(time_smpl)
        valrange = valmax - valmin
        zsin_smpl = 0.5*sin(rad_smpl) + 0.5 # Scale sine function so it is between 0 and 1.
        val_smpl = valrange*zsin_smpl + valmin # Scale again
        print("time = {}, radians = {}, value = {}".format(time_smpl, rad_smpl, val_smpl))


if __name__ == "__main__":
    now = datetime.utcnow()
    midnight = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    simsamples(tm=midnight)
