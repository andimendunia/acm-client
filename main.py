import serial
import requests
import time
import json
import traceback
import datetime

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

    api_url             = config.get('api_url', 'http://localhost/api/ins-acm-metrics')
    baud_rate           = config.get('baud_rate', 9600)
    line                = config.get('line', 'TEST')
    duration_seconds    = config.get('duration_seconds', 60)
    serial_port         = config.get('serial_port', 'COM1')

print('')
print('-----------------------------------')
print('Aplikasi main.py berjalan.')
print('-----------------------------------')
print('')
print('Berikut konfigurasi yang terbaca:')
print('')
print(' •  api_url          : ' + str(api_url))
print(' •  baud_rate        : ' + str(baud_rate))
print(' •  line             : ' + str(line))
print(' •  duration_seconds : ' + str(duration_seconds))
print(' •  serial_port      : ' + str(serial_port))
print('')

def collect_data():
    data = []  # List to store received data
    start_time = time.time()  # Get the current time
    while (time.time() - start_time) < duration_seconds:
        now = datetime.datetime.now()
        data_line = ser.readline().decode().strip()
        data_list = data_line.split(",")
        data_dict = {
            'line': line,
            'dt_client': now.strftime('%Y-%m-%d %H:%M:%S'),
            'rate_min': int(data_list[0]),
            'rate_max': int(data_list[1]),
            'rate_act': int(data_list[2]),
        }
        data.append(data_dict)  # Add received data to the list
        print(data_dict)  # Print received data
    return data

try:
    # Establish serial communication
    print('Membuka komunikasi serial...')
    ser = serial.Serial(serial_port, baud_rate)
except Exception as e:
    print('')
    print('Tidak dapat berkomunikasi dengan serial.')
    print(str(e))
    print('')
    print('Program dihentikan, sampai jumpa.')
    exit()


while True:
    try:
        print('Mendengar serial...')
        collected_data = collect_data()
        print('Data terkumpul: ' + str(len(collected_data)) )
        
        # Send data via HTTP API
        payload = {'data': collected_data}

        print('Mengirim ke server...')
        response = requests.post(api_url, json=payload)
        # 200 artinya OK
        if response.status_code == 200:
            print('Balasan dari server: ' + str(response.content))

        else:
            print('Terjadi kesalahan pada server:' + str(response.status_code))
            # break  # Exit the loop if data sent successfully

    except KeyboardInterrupt:
        print('Program dihentikan oleh user.')
        break  # Exit the loop if stopped by the user

    except Exception as e:
        with open('error.log', 'a') as error_log:
            error_log.write(f'Terjadi error: {str(e)}\n')
            error_log.write(f'Traceback: {traceback.format_exc()}\n')
        print('Terjadi error: ' + str(e))
        print('')
        print('Program tertidur selama satu menit...')
        time.sleep(60)  # Wait for 60 seconds before retrying

# Close the serial connection when done
ser.close()
