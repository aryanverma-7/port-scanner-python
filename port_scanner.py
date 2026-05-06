import socket
import threading

# INPUT

target = input("Enter Target IP / Website: ")

try:
    start = int(input("Enter Start Port: "))
    end = int(input("Enter End Port: "))

    if start < 0 or end > 65535 or start > end:
        print("Invalid Port Range!")
        exit()

except:
    print("Invalid Input!")
    exit()

# COMMON SERVICES

services = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy"
}

print("\n" + "="*60)
print(f"Scanning Target : {target}")
print(f"Port Range      : {start} - {end}")
print("="*60 + "\n")

open_ports = []
closed_ports = []

# SCAN FUNCTION

def scan(port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:

            service = services.get(port, "Unknown Service")

            print(f"[OPEN] Port {port} --> {service}")

            open_ports.append((port, service))

        else:

            closed_ports.append(port)

        s.close()

    except:
        pass

# THREADING

threads = []

for port in range(start, end + 1):

    t = threading.Thread(target=scan, args=(port,))

    threads.append(t)

    t.start()

for t in threads:

    t.join()

# CLOSED PORT RANGE FUNCTION

def make_ranges(ports):

    ranges = []

    if not ports:
        return ranges

    ports = sorted(ports)

    start_port = ports[0]
    end_port = ports[0]

    for port in ports[1:]:

        if port == end_port + 1:

            end_port = port

        else:

            ranges.append((start_port, end_port))

            start_port = port
            end_port = port

    ranges.append((start_port, end_port))

    return ranges

# SHOW CLOSED RANGES

print("\n" + "="*60)
print("CLOSED PORT RANGES")
print("="*60)

closed_ranges = make_ranges(closed_ports)

for start_p, end_p in closed_ranges:

    if start_p == end_p:

        print(f"[CLOSED] Port {start_p}")

    else:

        print(f"[CLOSED] Ports {start_p}-{end_p}")

# SAVE RESULTS

with open("result.txt", "w") as f:

    f.write("OPEN PORTS\n")
    f.write("="*40 + "\n")

    for port, service in open_ports:

        f.write(f"Port {port} --> {service}\n")

    f.write("\nCLOSED PORT RANGES\n")
    f.write("="*40 + "\n")

    for start_p, end_p in closed_ranges:

        if start_p == end_p:

            f.write(f"Port {start_p} CLOSED\n")

        else:

            f.write(f"Ports {start_p}-{end_p} CLOSED\n")

# FINAL OUTPUT

print("\n" + "="*60)
print("SCAN COMPLETE")
print("="*60)

print(f"\nTotal Open Ports   : {len(open_ports)}")
print(f"Total Closed Ports : {len(closed_ports)}")

print("\nResults saved in result.txt")
