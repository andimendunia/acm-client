title ASSEMBLY CONVEYOR MONITORING - MM
pnputil /enable-device "USB\VID_1A86&PID_7523\5&89f2c13&0&3"
cd /d C:\acm-py
nircmd cmdwait 3000 win hide ititle "CONVEYOR MONITORING"
python main.py
