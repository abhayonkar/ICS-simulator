# ICSSIM-main/src/PLC1.py
from ics_sim.Device import PLC, SensorConnector, ActuatorConnector
from Configs import TAG, Controllers, Connection
import logging


class PLC1(PLC):
    def __init__(self):
        sensor_connector = SensorConnector(Connection.CONNECTION)
        actuator_connector = ActuatorConnector(Connection.CONNECTION)
        super().__init__(1, sensor_connector, actuator_connector, TAG.TAG_LIST, Controllers.PLCs)

    def _logic(self):
        # We'll use a simple control loop to maintain pressure
        # Read the global average pressure from the physical simulation
        global_pressure = self._get(TAG.TAG_GLOBAL_PRESSURE)
        
        # Simple pressure regulation logic
        # If pressure is too high, close all valves
        if global_pressure > 120:
            for i in range(1, PHYSICS.VALVE_COUNT + 1):
                self._set(f'valve_{i}_status', 0)
                self.report(f"Pressure too high ({global_pressure:.2f} kPa), closing valve {i}", logging.WARNING)

        # If pressure is too low, open all valves
        elif global_pressure < 90:
            for i in range(1, PHYSICS.VALVE_COUNT + 1):
                self._set(f'valve_{i}_status', 1)
                self.report(f"Pressure too low ({global_pressure:.2f} kPa), opening valve {i}", logging.INFO)

        # In a normal state, keep valves open
        else:
            for i in range(1, PHYSICS.VALVE_COUNT + 1):
                self._set(f'valve_{i}_status', 1)
