# ICSSIM-main/src/Configs.py

class SimulationConfig:
    # Constants
    EXECUTION_MODE_LOCAL = 'local'
    EXECUTION_MODE_DOCKER = 'docker'
    EXECUTION_MODE_GNS3 = 'gns3'

    # configurable
    EXECUTION_MODE = EXECUTION_MODE_DOCKER


class PHYSICS:
    # Gas Pipeline Physical Parameters
    PIPE_LENGTH = 1000  # meters
    PIPE_DIAMETER = 0.5 # meters
    PRESSURE_ATM = 101.3 # kPa (kilopascal)
    GAS_CONSTANT = 8.314 # J/(mol*K)

    # Sensors and Actuators
    PRESSURE_SENSOR_COUNT = 10
    VALVE_COUNT = 10

    # Leak Simulation
    LEAK_RATE_NORMAL = 0.0 # m^3/s
    LEAK_RATE_MINOR = 0.05 # m^3/s
    LEAK_RATE_MAJOR = 0.2 # m^3/s


class TAG:
    # Tags for the gas pipeline simulation
    TAG_PIPELINE_STATUS = 'pipeline_status'
    TAG_GLOBAL_PRESSURE = 'global_pressure'
    TAG_GLOBAL_FLOW_RATE = 'global_flow_rate'
    TAG_LEAK_RATE = 'leak_rate'

    # Dynamically generated tags for each pressure sensor and valve
    TAG_LIST = {
        TAG_PIPELINE_STATUS: {'id': 0, 'plc': 1, 'type': 'output', 'fault': 0.0, 'default': 1},
        TAG_GLOBAL_PRESSURE: {'id': 1, 'plc': 1, 'type': 'input', 'fault': 0.0, 'default': 101.3},
        TAG_GLOBAL_FLOW_RATE: {'id': 2, 'plc': 1, 'type': 'input', 'fault': 0.0, 'default': 0},
        TAG_LEAK_RATE: {'id': 3, 'plc': 1, 'type': 'output', 'fault': 0.0, 'default': 0}
    }

    # Add tags for each sensor and valve
    for i in range(1, PHYSICS.PRESSURE_SENSOR_COUNT + 1):
        tag_name = f'pressure_sensor_{i}_value'
        TAG_LIST[tag_name] = {'id': 100 + i, 'plc': 1, 'type': 'input', 'fault': 0.0, 'default': 101.3}

    for i in range(1, PHYSICS.VALVE_COUNT + 1):
        tag_name = f'valve_{i}_status'
        TAG_LIST[tag_name] = {'id': 200 + i, 'plc': 1, 'type': 'output', 'fault': 0.0, 'default': 1}
        tag_name_mode = f'valve_{i}_mode'
        TAG_LIST[tag_name_mode] = {'id': 300 + i, 'plc': 1, 'type': 'output', 'fault': 0.0, 'default': 3}


class Controllers:
    PLC_CONFIG = {
        SimulationConfig.EXECUTION_MODE_DOCKER: {
            1: {
                'name': 'PLC_MASTER',
                'ip': '192.168.0.11',
                'port': 502,
                'protocol': 'ModbusWriteRequest-TCP'
             }
        }
    }

    PLCs = PLC_CONFIG[SimulationConfig.EXECUTION_MODE]


class Connection:
    SQLITE_CONNECTION = {
        'type': 'sqlite',
        'path': 'storage/PhysicalSimulation1.sqlite',
        'name': 'fp_table',
    }
    MEMCACHE_DOCKER_CONNECTION = {
        'type': 'memcache',
        'path': '192.168.1.31:11211',
        'name': 'fp_table',
    }
    File_CONNECTION = {
        'type': 'file',
        'path': 'storage/sensors_actuators.json',
        'name': 'fake_name',
    }

    CONNECTION_CONFIG = {
        SimulationConfig.EXECUTION_MODE_GNS3: MEMCACHE_DOCKER_CONNECTION,
        SimulationConfig.EXECUTION_MODE_DOCKER: SQLITE_CONNECTION,
        SimulationConfig.EXECUTION_MODE_LOCAL: SQLITE_CONNECTION
    }
    CONNECTION = CONNECTION_CONFIG[SimulationConfig.EXECUTION_MODE]
