import serial
import time

def simulate_serial_data(port, baudrate=9600, interval=1):
    try:
        ser = serial.Serial(port, baudrate)
        print(f"Simulating data on {port}. Press Ctrl+C to stop.")
        count = 0
        while True:
            data = f"Serial data {count}\n".encode('utf-8')
            ser.write(data)
            print(f"Sent: {data.decode('utf-8').strip()}")
            count += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped.")
        ser.close()

simulate_serial_data('COM10')  # Replace 'COMx' with your COM port
