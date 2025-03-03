# Using the FPGA Script

This script enables communication with an FPGA via a serial (UART) port. It provides several functionalities to write and read memory values, as well as to display data on LEDs.

## Prerequisites

- Python 3 installed
- `pyserial` library installed (if needed, install with `pip install pyserial`)
- An FPGA connected to a serial port on the computer

## Installation

1. Clone this repository or copy the file to your machine.
2. Ensure `pyserial` is installed by running:
   ```sh
   pip install pyserial
   ```

## Usage

### 1. Initialization

Create an instance of the `FPGA` class, specifying the COM port, baud rate, and timeout:
```python
fpga = FPGA("COM10", 115200, timeout=None)
```

### 2. Open Connection
Before any communication, open the connection with:
```python
fpga.open_instrument()
```

### 3. Writing to Memory
Set a memory address and write a value to it:
```python
fpga.set_memory_addr("00")  # Memory address
fpga.write_val_mem("FF")    # Value to write
```

### 4. Display Values on LEDs

```python
fpga.display_mem_vals_leds()
```

### 5. Reading a Memory Value
```python
mem_val = fpga.read_mem_val()
print("Read value:", mem_val)
```

### 6. Close Connection
At the end of the program, close the serial connection:
```python
fpga.close_instrument()
```

## Complete Example

```python
if __name__ == '__main__':
    fpga = FPGA("COM10", 115200, timeout=None)
    fpga.open_instrument()
    fpga.set_memory_addr("00")
    fpga.write_val_mem("FF")
    fpga.display_mem_vals_leds()
    mem_val = fpga.read_mem_val()
    print("Read value:", mem_val)
    fpga.close_instrument()
```

## Notes
- Ensure that the correct serial port is used (`COM10` in this example, adjust as needed for your setup).
- The FPGA must be properly configured to interpret the sent commands.

## Troubleshooting
- **Error opening the port**: Ensure no other program is using the serial port.
- **No response received**: Check the connection and proper functioning of the FPGA.




