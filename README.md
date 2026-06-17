# 🛡️ Network Sniffer 🌐

This project consists of the development of a **Network Sniffer** in Python, using the **Scapy** library for packet capture and manipulation, and **CustomTkinter** for a modern and intuitive graphical user interface (GUI).

The application allows users to capture, analyze, and visualize network packets in real time.

---

## 🚀 Features

The system implements the following core capabilities:

* **Real-Time Packet Capture**
  Instant network traffic monitoring using Scapy.

* **Protocol Layer Header Analysis**
  Packet decomposition according to the protocol stack:

  * **Layer 2:** Ethernet, ARP
  * **Layer 3:** IPv4, IPv6, ICMP
  * **Layer 4:** TCP, UDP

* **Application Protocol Detection**
  Identification of HTTP, HTTPS, SSH, FTP, DNS, DHCP, and NTP through analysis of the ports found in captured TCP and UDP packets.

* **Interactive Graphical Interface**
  Organized visualization of captured packets, including a pagination system for improved navigation.

* **Advanced Filtering System**
  Allows traffic isolation using logical expressions.

* **Data Export**
  Saves captures in **JSON** format, either through user interaction or automatically in live mode whenever a capture session starts.

---

## 🔍 Filtering System

Allows the creation of logical expressions to filter traffic.

### Supported Operators

| Type       | Operators                        |
| ---------- | -------------------------------- |
| Comparison | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Logical    | `and`, `or`                      |
| Grouping   | `( )`                            |

### Available Fields

* `protocol` — packet protocol
* `src` — source address (IP/MAC)
* `dst` — destination address (IP/MAC)
* `length` — packet size (bytes)
* `packet_id` — unique identifier
* `timestamp` — capture timestamp

### Deep Packet Inspection

Access packet fields by layer using `layerX.field`.

### Layer4:

```text
layer4.protocol
layer4.app_protocol
layer4.srcPrt
layer4.dstPrt
```

### Layer3:

`IPv4:`

```text
layer3.ip.version
layer3.ip.header_length
layer3.ip.len
layer3.ip.id
layer3.ip.flags, (MF | DF | 0)
layer3.ip.offset
layer3.ip.protocol
layer3.ip.ttl
layer3.ip.src
layer3.ip.dst
```

`IPv6:`

```text
layer3.ipv6.traffic_class
layer3.ipv6.flow_label
layer3.ipv6.payload_length
layer3.ipv6.next_header
layer3.ipv6.hop_limit
layer3.ipv6.src
layer3.ipv6.dst
```

`ICMP:`

```text
layer3.icmp.protocol
layer3.icmp.type
layer3.icmp.code
```

### Layer2:

`ARP:`

```text
layer2.arp.protocol
layer2.arp.sender_mac
layer2.arp.target_mac
```

`Ethernet`

```text
layer2.arp.protocol
layer2.arp.src_mac
layer2.arp.dst_mac
layer2.arp.type
```

**Examples:**

```python
protocol == TCP
src == 192.168.1.1
length > 100
protocol == ICMP and length > 60
layer4.dport == 53
layer3.ip.ttl > 64
```

---

## 🐧 Installation (Linux - Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3-venv python3-full python3-tk -y

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install scapy customtkinter pillow cryptography
```

---

## 🪟 Installation (Windows)

```bash
pip install scapy customtkinter pillow cryptography
```

---

## 🛠️ How to Run

⚠️ The application must be executed with administrator/root privileges.

### Linux

```bash
sudo ./venv/bin/python main.py
```

### Windows

Run the terminal as Administrator:

```bash
python main.py
```

---

## 🌐 Interface Selection

Before starting a capture, select a valid network interface (e.g., `eth0`, `wlan0`).

The available interfaces are automatically detected by Scapy.

---

## 🧪 Running in CORE

To export the GUI:

### Host System

```bash
xhost +
```

### CORE Node

* In the terminal, navigate to the folder containing the sniffer

```bash
export DISPLAY=:0
sudo -E python main.py
```

---

## 💾 Exporting Data

* Packets are automatically saved to a JSON file
* Only filtered results can be exported using the export button

---

## ⚠️ Important Notes

* **Permissions:** Packet capture will fail without administrator privileges
* **Interface:** Make sure the correct network interface is selected
* **Performance:** Filters affect only the visualization, not the packet capture process
