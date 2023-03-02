'''
Author: Qi7
Date: 2023-03-02 11:28:10
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-03-02 11:29:46
Description: 
'''
#!/usr/bin/env python3
import time
# python API client for influx 2.x
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS


def write_influx2(influx, unit, table_name, data_name, data, start_timestamp, fs):
    bucket = influx['bucket']
    org = influx['org']
    token = influx['token']
    url = influx['ip'] + ":8086"
    start = start_timestamp
    
    max_size = 1
    count = 0
    total = len(data)
    
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    for value in data:
        count += 1
        if count >= max_size:
            print("Write to influx: ", table_name, data_name, count)
            p = influxdb_client.Point(table_name).tag("location", unit).field(data_name, value).time(start)
            write_api.write(bucket=bucket, org=org, record=p)
            total = total - count
            count = 0
        start += 1 / fs

def read_influx2(influx, unit, table_name, data_name, start_timestamp, pre_len, startEpoch):
    
    bucket = influx['bucket']
    org = influx['org']
    token = influx['token']
    url = influx['ip'] + ":8086"
    start = start_timestamp + 'Z' # correct format
    
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    
    if(start_timestamp==startEpoch):
        time.sleep(30)
    else:
        time.sleep(3)
            
    query_api = client.query_api()
    query = f' from(bucket:"{bucket}")\
    |> range(start: {start})\
    |> filter(fn:(r) => r._measurement == "{table_name}")\
    |> filter(fn:(r) => r._field == "{data_name}" )\
    |> limit(n:{pre_len})'
    
    print(query)
    
    result = query_api.query(org=org, query=query)
    data, times = [], []
    for table in result:
        for record in table.records:
            data.append(record.get_value())
            times.append(record.get_time())

    return data, times