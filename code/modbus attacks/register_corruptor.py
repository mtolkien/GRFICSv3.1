import random
import time
from pymodbus.client import ModbusTcpClient

# Configura l'indirizzo IP e la porta del server Modbus
client = ModbusTcpClient('192.168.95.2', port=502)

client.connect()

# Indirizzo di partenza dei registri
start_address = 0
num_registers = 13  # Numero di registri da sovrascrivere

try:
    while True:
        # Genera una lista di valori casuali (UINT16, tra 0 e 65535) per i registri
        values = [random.randint(0, 65535) for _ in range(num_registers)]

        result = client.write_registers(start_address, values)

        if result.isError():
            print(f"Errore durante la scrittura dei registri a partire dall'indirizzo {start_address}")
        else:
            print(f"Registri sovrascritti con successo con i valori casuali")

        time.sleep(0.0005)

except KeyboardInterrupt:
    print("Esecuzione interrotta manualmente.")

finally:
    client.close()
