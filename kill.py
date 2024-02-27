import psutil

def close_port(port):
    for conn in psutil.net_connections(kind='inet'):
        print(conn)
        if conn.laddr.port == port:
            print(f"Closing port {port} by terminating PID {conn.pid}")
            process = psutil.Process(conn.pid)
            process.terminate()

close_port('11')