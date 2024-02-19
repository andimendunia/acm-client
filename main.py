import serial
import requests
import time
import json
import datetime
import subprocess
import logging
import os

print('')
print('-----------------------------------')
print('Program main.py berjalan.')
print('-----------------------------------')
print('')

# Konfigurasi sistem logging
log_dir     = "log"
os.makedirs(log_dir, exist_ok=True)
now         = datetime.datetime.now()
log_file    = f"{log_dir}/{now.strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logging.info('Memulai program...')
instance_id = ""

# Baca konfigurasi config.json
try:
    with open('config.json', 'x') as file:
        logging.info('Membuat config.json baru...')
        json.dump({}, file)
except:
    pass

with open('config.json', 'r') as config_file:
    config                  = json.load(config_file)
    api_url                 = config.get('api_url', 'http://172.70.87.101/api/ins-acm-metrics')
    baud_rate               = config.get('baud_rate', 9600)
    device_name             = config.get('device_name', 'USB-SERIAL CH340')
    line                    = config.get('line', 'TEST')
    duration_seconds        = config.get('duration_seconds', 10)
    serial_port             = config.get('serial_port', 'COM10')
    sleep_seconds           = config.get('sleep_seconds', 300)
    restart_device_enabled  = config.get('restart_device_enabled', False)

print('')
print(' •  api_url                  : ' + str(api_url))
print(' •  baud_rate                : ' + str(baud_rate))
print(' •  device_name              : ' + str(device_name))
print(' •  line                     : ' + str(line))
print(' •  duration_seconds         : ' + str(duration_seconds))
print(' •  serial_port              : ' + str(serial_port))
print(' •  sleep_seconds            : ' + str(sleep_seconds))
print(' •  restart_device_enabled   : ' + str(restart_device_enabled))
print('')

def get_instance_id():
    name = f"{device_name} ({serial_port})"
    ps_command = f"""
    $device = Get-PnpDevice -PresentOnly | Where-Object {{ $_.Name -eq "{name}" }} | Select-Object -First 1 InstanceId
    $device.InstanceId
    """
    process = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
    return process.stdout.strip()

def collect_data():
    data = [] 
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        now = datetime.datetime.now()
        try:
            data_line = ser.readline().decode().strip()
            data_list = data_line.split(",")
            data_dict = {
                'line': line,
                'dt_client': now.strftime('%Y-%m-%d %H:%M:%S'),
                'rate_min': int(data_list[0]),
                'rate_max': int(data_list[1]),
                'rate_act': int(data_list[2]),
                'length_data': len(data_line),
            }  
        except Exception as e:
            print('', end="\r")
        else:
            data.append(data_dict) 
            print(data_dict, end="\r")
    return data

def restart_device():
    logging.debug('Hit restart device function')

    if not restart_device:
        logging.info('Fitur restart_device tidak dieksekusi karena dimatikan')
        time.sleep(3)

    elif instance_id:
        disable_command = f"Disable-PnpDevice -InstanceId \"{instance_id}\" -Confirm:$false"
        enable_command  = f"Enable-PnpDevice -InstanceId \"{instance_id}\" -Confirm:$false"

        subprocess.run(["powershell", "-Command", disable_command], capture_output=True, text=True)
        logging.info('Perintah Disable-PnpDevice dieksekusi')
        time.sleep(3)

        subprocess.run(["powershell", "-Command", enable_command], capture_output=True, text=True)
        logging.info('Perintah Enable-PnpDevice dieksekusi')
        time.sleep(3)

    else:
        logging.info('Tidak dapat menjalankan ulang device karena instance_id tidak ada')

def close_serial():
    try:
        logging.info('Menutup serial...')
        ser.close()
    except Exception as e:
        logging.warning(str(e)) 

def user_quit():
    close_serial()
    logging.info('Program dihentikan oleh user. Selamat tinggal!')
    time.sleep(3)
    quit()


# Mendapatkan instance_id untuk restart_device
if not instance_id and restart_device_enabled:
    logging.info('Mendapatkan instance_id...')
    instance_id = get_instance_id()

    if not instance_id:
        logging.error('Gagal mendapatkan instance_id')
        time.sleep(3)
        quit()
    else:
        logging.info(f"instance_id: {instance_id}")

else:
    logging.info('Fitur restart_device dimatikan')

# Mulai membuka serial
logging.info('Membuka serial...')
ser = serial.Serial(serial_port, baud_rate, timeout=30)  
logging.info('Mendengar serial...')
print('')


while True:
    try:
        collected = collect_data()
        print('')
        logging.info('Jumlah data yang di dengar: ' + str(len(collected)) )

        if len(collected) == 0:
            restart_device()
        else: 
            # Send last data via HTTP API
            end = collected[-1:]
            payload = {'data': end }

            logging.info('Mengirim data terakhir ke server...')
            response = requests.post(api_url, json=payload)

            # 200 artinya OK
            if response.status_code == 200:
                logging.info('Balasan dari server: ' + str(response.content))

            else:
                logging.warning('Server: ' + str(response.status_code))
            print('')            

    except serial.SerialTimeoutException:
        print('')
        logging.exception('Durasi mendengar serial mencapai timeout')
        restart_device()

    except KeyboardInterrupt:
        print('')
        user_quit()

    except Exception as e:
        print('')
        logging.error(str(e))
        logging.info('Program tertidur selama ' + str(sleep_seconds) + ' detik...')

        try:
            time.sleep(sleep_seconds)  # Wait before retrying
        except KeyboardInterrupt:
            print('')
            user_quit()

        print('')
        logging.info('Melanjutkan program...')
