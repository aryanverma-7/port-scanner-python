import socket
import threading

target = input("Enter target IP: ")

try:
    start = int(input("Enter start port: "))
    end = int(input("Enter end port: "))
    if start < 0 or end > 65535 or start > end:
        print("Invalid port range!")
        exit()
except:
    print("Invalid port range!")
    exit()

print("\n" + "="*50)
print(f"Scanning Target: {target}")
print(f"Port Range: {start} - {end}")
print("="*50 + "\n")

open_ports = []

def scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"[OPEN] Port {port}")
            open_ports.append(port)

        s.close()
    except:
        pass

threads = []

for port in range(start, end + 1):
    t = threading.Thread(target=scan, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Save results
with open("result.txt", "w") as f:
    for port in open_ports:
        f.write(f"Port {port} is OPEN\n")

print("\n" + "="*50)
print("SCAN COMPLETE")
print("="*50)

print(f"Total Open Ports: {len(open_ports)}")
print("Open Ports List:", open_ports)
print("\nResults saved in result.txt")
