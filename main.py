import serial
import requests
import time
import json
import datetime

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

    api_url             = config.get('api_url', 'http://localhost/api/ins-acm-metrics')
    baud_rate           = config.get('baud_rate', 9600)
    line                = config.get('line', 'TEST')
    duration_seconds    = config.get('duration_seconds', 60)
    serial_port         = config.get('serial_port', 'COM1')
    sleep_seconds       = config.get('sleep_seconds', 1)

print('')
print('-----------------------------------')
print('Program main.py berjalan.')
print('-----------------------------------')
print('')
print('Berikut konfigurasi yang terbaca:')
print('')
print(' •  api_url          : ' + str(api_url))
print(' •  baud_rate        : ' + str(baud_rate))
print(' •  line             : ' + str(line))
print(' •  duration_seconds : ' + str(duration_seconds))
print(' •  serial_port      : ' + str(serial_port))
print(' •  sleep_seconds    : ' + str(sleep_seconds))
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
        print(data_dict, end="\r")  # Print received data
    return data

while True:
    try:

        print('Membuka komunikasi serial...')
        ser = serial.Serial(serial_port, baud_rate)     
        print('Mendengar serial...')
        print('')

        collected = collect_data()
        print('\nJumlah data yang di dengar: ' + str(len(collected)) )

        # Send last data via HTTP API
        end = collected[-1:]
        payload = {'data': end }
        print('Menutup komunikasi serial...')
        ser.close()

        print('Mengirim data terakhir ke server...')
        response = requests.post(api_url, json=payload)

        # 200 artinya OK
        if response.status_code == 200:
            print('Balasan dari server: ' + str(response.content))

        else:
            print('Terjadi kesalahan pada server:' + str(response.status_code))

    except KeyboardInterrupt:
        print('Menutup komunikasi serial...')
        ser.close()
        print('Program dihentikan oleh user.')
        break  # Exit the loop if stopped by the user

    except Exception as e:
        with open('error.log', 'a') as error_log:
            error_log.write(f'Terjadi error: {str(e)}\n')
        print('')
        print('Terjadi error: ' + str(e))
        print('')

        if 'ser' in locals():
            if ser.is_open:
                print('Menutup komunikasi serial...')
                ser.close()
        print('Program tertidur selama ' + str(sleep_seconds) + ' menit...')
        time.sleep(sleep_seconds * 60)  # Wait before retrying
        print('')
        print('Melanjutkan program...')
