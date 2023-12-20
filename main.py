import serial
import requests
import time
import json
import traceback

# Define the serial port (you might need to change this)
# serial_port = '/dev/ttyUSB0'  # On Linux
serial_port = 'COM11'  # On Windows (change to your port)

# Define the baud rate (must match Arduino's baud rate)
baud_rate = 9600

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    data_collection_duration = config.get("data_collection_duration_seconds", 5)

def collect_data():
    data_list = []  # List to store received data
    start_time = time.time()  # Get the current time
    while (time.time() - start_time) < data_collection_duration:
        line = ser.readline().decode().strip()
        data_list.append(line)  # Add received data to the list
        print(line)  # Print received data
    return data_list

# Establish serial communication
ser = serial.Serial(serial_port, baud_rate)

while True:
    try:
        collected_data = collect_data()

        # Send data via HTTP API
        api_endpoint = 'https://your-api-endpoint-here.com/data'  # Replace with your API endpoint
        payload = {'data': collected_data}

        response = requests.post(api_endpoint, json=payload)
        if response.status_code == 200:
            print("Data sent successfully!")
            break  # Exit the loop if data sent successfully

    except KeyboardInterrupt:
        print("Program stopped by the user.")
        break  # Exit the loop if stopped by the user

    except Exception as e:
        with open('error.log', 'a') as error_log:
            error_log.write(f"An error occurred: {str(e)}\n")
            error_log.write(f"Traceback: {traceback.format_exc()}\n")
        print("An error occurred. Retrying in 1 minute...")
        time.sleep(60)  # Wait for 5 seconds before retrying

# Close the serial connection when done
ser.close()
