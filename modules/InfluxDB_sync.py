# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import datetime



"""Tutorial on using the InfluxDB client."""


def sendToInfluxDB(traffic_station,date_class,time_class,full_string, host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'homeassistant'
    password = 'homeassistant'
    dbname = 'vegvesen'
    query = 'select Float_value from cpu_load_short;'
    query_where = 'select Int_value from cpu_load_short where host=$host;'
    bind_params = {'host': 'server01'}
    json_body = [
        {
            "measurement": "kjoretimer",
            "tags": {
                "traffic_station": traffic_station
            },
            "time": date_class,
            "fields": {
                "timen": date_class,
                "sted": traffic_station,

            }   
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)


    print("Write points: {0}".format(json_body))
    client.write_points(json_body,time_precision='ms')

