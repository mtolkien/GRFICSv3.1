from pymodbus.client import ModbusTcpClient
import random
import time

client = ModbusTcpClient('192.168.95.2', port=502)

try:
    while True:
        # Genera una lista di valori casuali
        valori = [random.randint(0, 65535) for _ in range(13)]

        response = client.write_registers(0, valori)

        # Controlla se la scrittura ha avuto successo
        if response.isError():
            print(f"Errore nella scrittura dei registri: {response}")
        else:
            print("Registri corrotti con successo.")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Operazione interrotta")

finally:
    client.close()
