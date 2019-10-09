import json
import pandas as pd
from influxable import attributes, serializers
from influxable.db import RawQuery
from influxable.measurement import Measurement
from influxable.response import InfluxDBResponse


class TestSerializer:
    def create_measurement_class(self):
        class MySampleMeasurement(Measurement):
            measurement_name = 'mysamplemeasurement'
            time = attributes.TimestampFieldAttribute(precision="s")
            value = attributes.IntegerFieldAttribute()
        measurement_cls = MySampleMeasurement
        return measurement_cls

    def execute_query(self, query):
        response = RawQuery(query).execute()
        influx_response = InfluxDBResponse(response)
        return influx_response

    def execute_sample_query(self):
        query = 'SHOW DATABASES'
        influx_response = self.execute_query(query)
        return influx_response

    def test_base_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.BaseSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, dict)
        assert 'results' in data

    def test_json_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.JsonSerializer(influx_response)
        data = serializer.convert()
        json_data = json.loads(data)
        assert isinstance(data, str)
        assert json_data is not None

    def test_formatted_serie_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.FormattedSerieSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, list)
        assert len(data) == 1
        assert 'databases' in data[0]

