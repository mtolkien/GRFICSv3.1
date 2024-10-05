import time
from pymodbus.client import ModbusTcpClient

# Configura l'indirizzo IP e la porta del server Modbus
client = ModbusTcpClient('192.168.95.2', port=502)

client.connect()

# Indirizzo della coil
address = 40

try:
    while True:
        current_value = True
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Errore durante la scrittura del coil {address} con valore {current_value}")
        else:
            print(f"Coil {address} scritto con successo con valore {int(current_value)}")

        time.sleep(0.1)

        current_value = False  # Secondo valore
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Errore durante la scrittura del coil {address} con valore {current_value}")
        else:
            print(f"Coil {address} scritto con successo con valore {int(current_value)}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interruzione manuale. Chiusura del client...")

finally:
    client.close()