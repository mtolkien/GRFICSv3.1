import subprocess
import time

# Numero di esecuzioni al minuto
EXECUTIONS_PER_MINUTE = 2  # Ad esempio, 2 significa ogni 30 secondi
INTERVAL = 60 / EXECUTIONS_PER_MINUTE

rc_file = "modbus_commands.rc"

while True:
    # Esegui Metasploit con il file .rc utilizzando subprocess
    process = subprocess.run(["msfconsole", "-q", "-r", rc_file])

    # Controlla l'output di ritorno per eventuali errori
    if process.returncode != 0:
        print(f"Errore durante l'esecuzione di Metasploit: codice di uscita {process.returncode}")

    time.sleep(INTERVAL)
