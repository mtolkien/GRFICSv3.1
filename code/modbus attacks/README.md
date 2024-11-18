## Overview

This folder contains two scripts that utilize the Modbus protocol to interact with the Modbus server. The scripts demonstrate how to write values to registers and coils using the pymodbus library.

## Script Descriptions

### Script 1: Writing Random Values to Registers

This script connects to a Modbus server and continuously generates a list of random values to write to a set of registers.

**Key Features:**
- Connects to a Modbus TCP server at the specified IP address and port.
- Generates random values in the range of 0 to 65535.
- Writes the generated values to the registers.
- Handles errors during the write operation and prints success messages.

**Usage:**
1. Ensure the Modbus server is running and reachable at the specified IP address (`192.168.95.2`) and port (`502`).
2. Run the script in a Python environment where pymodbus is installed.

### Script 2: Writing Values to a Coil

This script connects to a Modbus server and alternates writing `True` and `False` values to a specified coil address.

**Key Features:**
- Connects to a Modbus TCP server at the specified IP address and port.
- Writes `True` to the given coil address, followed by `False`.
- Handles errors during the write operation and prints success messages.
- Loops indefinitely until interrupted.

**Usage:**
1. Ensure the Modbus server is running and reachable at the specified IP address (`192.168.95.2`) and port (`502`).
2. Specify the coil address in the script (default is `40`).
3. Run the script in a Python environment where pymodbus is installed.
