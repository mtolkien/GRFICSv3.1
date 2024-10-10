from pymodbus.client import ModbusTcpClient
import random
import time

client = ModbusTcpClient('192.168.95.2', port=502)

try:
    while True:
        # Generates a list of random values
        values = [random.randint(0, 65535) for _ in range(13)]

        response = client.write_registers(0, values)

        if response.isError():
            print(f"Error when writing registers: {response}")
        else:
            print("Corrupt registers with success")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Operation terminated")

finally:
    client.close()