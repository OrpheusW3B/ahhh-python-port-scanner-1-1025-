import argparse
import socket
from urllib.parse import urlparse
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

N_THREADS = 200
q = Queue()
print_lock = Lock()

open_ports = []
closed_ports = []

def port_scan(port):
    """Scan a port on the global variable `host`"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
    except:
        with print_lock:
            closed_ports.append(port)
            print(f"{GRAY}[CLOSED] Port {port:5}{RESET}")
    else:
        with print_lock:
            open_ports.append(port)
            print(f"{GREEN}[OPEN]   Port {port:5}{RESET}")
    finally:
        s.close()

def scan_thread():
    while True:
        port = q.get()
        port_scan(port)
        q.task_done()

def main():
    global host
    parser = argparse.ArgumentParser(description="Basic CLI Port Scanner")
    parser.add_argument("-S", "--site", help="Target URL to scan (e.g. https://example.com)")
    parser.add_argument("host", nargs="?", help="Target host to scan (e.g. example.com)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1025, help="End port (default: 1025)")
    args = parser.parse_args()

    if args.site:
        parsed = urlparse(args.site)
        host = parsed.hostname or parsed.path
    else:
        host = args.host

    if not host:
        parser.error("Provide a target host or URL (-S)")
    start = args.start
    end = args.end

    for _ in range(N_THREADS):
        t = Thread(target=scan_thread, daemon=True)
        t.start()

    for port in range(start, end + 1):
        q.put(port)

    q.join()

    print(f"\n{GREEN}=== Scan Summary ===")
    print(f"Open ports:   {len(open_ports)}")
    if open_ports:
        print(f"  {open_ports}")
    if closed_ports:
        print(f"{GRAY}Closed ports: {len(closed_ports)}")
        print(f"  {closed_ports}")
    print(f"{RESET}")


if __name__ == "__main__":
    main()
