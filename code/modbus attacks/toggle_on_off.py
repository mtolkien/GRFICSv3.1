import time
from pymodbus.client import ModbusTcpClient

# Configura l'indirizzo IP e la porta del server Modbus
client = ModbusTcpClient('192.168.95.2', port=502)

print("Connessione in corso...")
client.connect()

# Indirizzo coil
address = 40

try:
    while True:
        current_value = True
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Errore durante la scrittura del coil {address} con valore {current_value}")
        else:
            print(f"Coil {address} scritto con successo con valore {int(current_value)}")

        time.sleep(0.01)

        current_value = False
        result = client.write_coil(address, current_value)

        if result.isError():
            print(f"Errore durante la scrittura del coil {address} con valore {current_value}")
        else:
            print(f"Coil {address} scritto con successo con valore {int(current_value)}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Operazione interrotta")

finally:
    client.close()
