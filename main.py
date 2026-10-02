import argparse
import asyncio
import socket
from urllib.parse import urlparse
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

open_ports = []
MAX_CONCURRENT = 5000


async def scan_port(ip, port):
    """Scan a single port asynchronously using a non-blocking socket."""
    loop = asyncio.get_event_loop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    try:
        await asyncio.wait_for(
            loop.sock_connect(s, (ip, port)),
            timeout=0.5
        )
    except (OSError, asyncio.TimeoutError):
        pass
    else:
        open_ports.append(port)
        print(f"{GREEN}[OPEN]   Port {port:5}{RESET}")
    finally:
        s.close()


async def scan_all(host, ports):
    """Scan all ports concurrently."""
    loop = asyncio.get_event_loop()
    try:
        addr = await loop.getaddrinfo(host, None, family=socket.AF_INET)
        ip = addr[0][4][0]
    except socket.gaierror:
        print(f"Error: could not resolve {host}")
        return
    tasks = [scan_port(ip, port) for port in ports]
    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Fast Async CLI Port Scanner")
    parser.add_argument("-S", "--site", help="Target URL (e.g. https://example.com)")
    parser.add_argument("host", nargs="?", help="Target host (e.g. example.com)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1025, help="End port (default: 1025)")
    parser.add_argument("-P", "--ports", help="Comma-separated ports (e.g. 21,22,80). Overrides -s/-e")
    args = parser.parse_args()

    if args.site:
        parsed = urlparse(args.site)
        host = parsed.hostname or parsed.path
    else:
        host = args.host

    if not host:
        parser.error("Provide a target host or URL (-S)")

    if args.ports:
        ports = [int(p.strip()) for p in args.ports.split(",") if p.strip()]
    else:
        ports = list(range(args.start, args.end + 1))

    print(f"Scanning {host} on {len(ports)} ports...\n")
    asyncio.run(scan_all(host, ports))

    total = len(ports)
    print(f"\n{GREEN}=== Scan Summary ===")
    print(f"Scanned: {total} | Open: {len(open_ports)}")
    if open_ports:
        print(f"  {open_ports}")
    print(f"{RESET}")


if __name__ == "__main__":
    main()
