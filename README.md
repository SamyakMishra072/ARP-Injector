# ARP Cache Poisoning Demonstration

This project shows how to perform a simple ARP cache poisoning (Man-in-the-Middle) attack on a controlled LAN using a Python/Scapy script, and how to capture & analyze it in Wireshark.

## 🖥️ Lab Setup
1. Two Linux VMs (`victim`, `gateway`) on the same isolated network.
2. Attacker VM with:
   - Python 3
   - Scapy
   - Wireshark/tshark

## 🔧 Usage
```bash
git clone https://github.com/SamyakMishra072/ARP-Injector.git
cd ARP-Injector
pip3 install -r requirements.txt
sudo python3 arp_poison.py <Victim_IP> <Gateway_IP>
