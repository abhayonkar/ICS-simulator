# ICSSIM-main/src/FactorySimulation.py
import logging
from ics_sim.Device import HIL
from Configs import TAG, PHYSICS, Connection
import math


class FactorySimulation(HIL):
    def __init__(self):
        super().__init__('Factory', Connection.CONNECTION, 100)
        self.init()
        # Initial pipeline state
        self.pipeline_pressure = [PHYSICS.PRESSURE_ATM] * PHYSICS.PRESSURE_SENSOR_COUNT
        self.pipeline_flow = [0.0] * PHYSICS.PRESSURE_SENSOR_COUNT


    def _logic(self):
        elapsed_time = (self._current_loop_time - self._last_loop_time) / 1000.0  # seconds

        # Read valve statuses from PLCs
        valve_statuses = []
        for i in range(1, PHYSICS.VALVE_COUNT + 1):
            tag_name = f'valve_{i}_status'
            status = self._get(tag_name)
            valve_statuses.append(status)

        # Simulate gas flow and pressure changes
        for i in range(PHYSICS.PRESSURE_SENSOR_COUNT):
            # A very simplified gas dynamics model
            # Pressure changes based on flow from previous section and valve status
            # For simplicity, we assume an initial pressure source and a single sink
            
            # Simplified flow calculation:
            # Flow is proportional to pressure difference and valve opening
            
            # Start of the pipeline (assuming external pressure source)
            if i == 0:
                pressure_diff = self.pipeline_pressure[0] - PHYSICS.PRESSURE_ATM
                flow_rate_in = pressure_diff / 100 * valve_statuses[0]
                
            else:
                pressure_diff = self.pipeline_pressure[i] - self.pipeline_pressure[i-1]
                flow_rate_in = pressure_diff / 100 * valve_statuses[i]
                
            # Flow out of the section
            flow_rate_out = self.pipeline_flow[i]

            # Gas leak simulation (controlled by a PLC tag)
            leak_rate = self._get(TAG.TAG_LEAK_RATE)
            flow_rate_out += leak_rate

            # Update pressure based on flow rates
            pressure_change = (flow_rate_in - flow_rate_out) * 10 
            self.pipeline_pressure[i] += pressure_change * elapsed_time
            self.pipeline_flow[i] = flow_rate_in

            # Update database with new sensor values
            self._set(f'pressure_sensor_{i+1}_value', self.pipeline_pressure[i])


        # update global tags (averages for the dashboard)
        avg_pressure = sum(self.pipeline_pressure) / len(self.pipeline_pressure)
        avg_flow = sum(self.pipeline_flow) / len(self.pipeline_flow)
        
        self._set(TAG.TAG_GLOBAL_PRESSURE, avg_pressure)
        self._set(TAG.TAG_GLOBAL_FLOW_RATE, avg_flow)
        self.report(f"Pressure: {avg_pressure:.2f} kPa, Flow: {avg_flow:.2f} m^3/s")


    def init(self):
        initial_list = []
        for tag in TAG.TAG_LIST:
            initial_list.append((tag, TAG.TAG_LIST[tag]['default']))

        self._connector.initialize(initial_list)


    @staticmethod
    def recreate_connection():
        return True


if __name__ == '__main__':
    factory = FactorySimulation()
    factory.start()

