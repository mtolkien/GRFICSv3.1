import time
from pymodbus.client import ModbusTcpClient

# Configure IP Address and Port of the server Modbus
client = ModbusTcpClient('192.168.95.2', port=502)
print("Connection...")
client.connect()

# Coil address
address = 40

try:
    while True:
        current_value = True
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Error when writing coil {address} with value {current_value}")
        else:
            print(f"Coil {address} successfully written with value {int(current_value)}")

        time.sleep(0.01)

        current_value = False
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Error when writing coil {address} with value {current_value}")
        else:
            print(f"Coil {address} successfully written with value {int(current_value)}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Operation terminated")

finally:
    client.close()