import pytest
from random import randint
import app

class MockWMI:
    def __init__(self,namespace):
        self.namespace = namespace

    def __repr__(self):
        return f'<MockWMI {self.namespace}>'
    
    @staticmethod
    def MSAcpi_ThermalZoneTemperature():
        return [MockTempResponse()]

class MockTempResponse:
    def __init__(self):
        values = {'ActiveTripPoint': 2732 + 500,
                'PassiveTripPoint': 2732 + 1000,
                'CriticalTripPoint': 2732 + 1500,
                'CurrentTemperature': randint(2732, 2732 + 2000)}
        for property,property_value in values.items():
            setattr(self,property,property_value)

@pytest.fixture(autouse=True)
def patch_WMI(monkeypatch):
    monkeypatch.setattr(app,"w",MockWMI(namespace = 'whatever'))
    print('app.w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature')
    print(app.w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature)