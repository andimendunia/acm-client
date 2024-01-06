import serial
import requests
import time
import json
import traceback
import datetime

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

    api_url             = config.get("api_url", "http://localhost/api/ins-acm-metrics")
    baud_rate           = config.get("baud_rate", 9600)
    line                = config.get('line', 0)
    duration_seconds    = config.get("duration_seconds", 60)
    serial_port         = config.get('serial_port', 'COM1')


def collect_data():
    data = []  # List to store received data
    start_time = time.time()  # Get the current time
    while (time.time() - start_time) < duration_seconds:
        now = datetime.datetime.now()
        data_line = ser.readline().decode().strip()
        data_list = data_line.split(",")
        data_dict = {
            "line": line,
            "dt_client": now.strftime("%Y-%m-%d %H:%M:%S"),
            "rate_min": int(data_list[0]),
            "rate_max": int(data_list[1]),
            "rate_act": int(data_list[2]),
        }
        data.append(data_dict)  # Add received data to the list
        print(data_dict)  # Print received data
    return data

# Establish serial communication
ser = serial.Serial(serial_port, baud_rate)

while True:
    try:
        collected_data = collect_data()

        # Send data via HTTP API
        payload = {'data': collected_data}

        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print("Data terikirim")
            print(response.content)
            # break  # Exit the loop if data sent successfully

    except KeyboardInterrupt:
        print("Program dihentikan oleh user.")
        break  # Exit the loop if stopped by the user

    except Exception as e:
        with open('error.log', 'a') as error_log:
            error_log.write(f"Terjadi error: {str(e)}\n")
            error_log.write(f"Traceback: {traceback.format_exc()}\n")
        print("Terjadi error. Mencoba lagi dalam 1 menit...")
        time.sleep(60)  # Wait for 60 seconds before retrying

# Close the serial connection when done
ser.close()
