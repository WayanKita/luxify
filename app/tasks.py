import os, csv, glob
from django.conf import settings
from celery import task
from django.utils import timezone
from app.models.room import Desk, SensorLog, Sensor

path = settings.SYNC_PATH  # the path where the synced files are located

def is_float(value):

    """
    Checks whether the given value is of the type float
    """

    try:
        float(value)
        return True
    except ValueError:
        return False

def is_int(value):

    """
    Checks whether the given value is of the type int
    """

    try:
        int(value)
        return True
    except ValueError:
        return False

@task
def parse_cvs():

    """
    Parses csv files and updates each desk's illuminance value
    """

    desks = Desk.objects.exclude(illuminance_sensor__isnull=True).exclude(occupancy_sensor__isnull=True)
    glob_pattern = os.path.join(path, '*.csv')  # filter out non-csv files
    file = max(glob.iglob(glob_pattern), key=os.path.getctime)  # only parse the newest file
    
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            if "Timestamp" in row:  # this indicates that the row is a header
                for idx, field in enumerate(row):
                    if Sensor.objects.filter(name=field).exists():
                        """ if a sensor with this name exists, update its column value """
                        Sensor.objects.filter(name=field).update(column=idx)
                    else:
                        """ if a sensor with this name doesn't exist, create one """
                        Sensor.objects.create(column=idx, name=field)
            if "Timestamp" not in row:  # this indicates that the row is not a header
                for desk in desks:
                    illuminance_column = desk.illuminance_sensor.column  # get the illuminance
                    occupancy = row[desk.occupancy_sensor.column]
                    if not is_int(row[desk.occupancy_sensor.column]):
                        occupancy = 0
                    if is_float(row[desk.illuminance_sensor.column_number]):
                        desk.illuminance = float(row[desk.illuminance_sensor.column_number])
                    desk.save()

                    """ convert occupancy to boolean """
                    occupied  = False
                    if occupancy == 1:
                        occupied = True

                    if is_float(row[desk.illuminance_sensor.column_number]):
                        """ if the illuminance value type is valid, log this """
                        SensorLog.objects.create(
                            desk=desk, 
                            timestamp=timezone.now(), 
                            illuminance=float(row[illuminance_column]), 
                            occupied=occupied
                        )
