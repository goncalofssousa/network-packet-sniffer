from scapy.all import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether
from scapy.layers.dhcp import DHCP

icmp_sessions = {}
tcp_sessions = {}


def EthernetProcesser(packet: Packet):
    if packet.haslayer(Ether):
        eth = packet[Ether]

        return {
            "protocol": "Ethernet",
            "src_mac": eth.src,
            "dst_mac": eth.dst,
            "type": hex(eth.type),
        }
    return None


def ARPProcesser(packet: Packet):
    if packet.haslayer(ARP):
        arp = packet[ARP]

        if arp.op == 1:
            summary = "ARP request"
            info = f"Quem é {arp.pdst}? Digam a {arp.psrc}"
        elif arp.op == 2:
            summary = "ARP reply"
            info = f"{arp.psrc} está em {arp.hwsrc}"
        else:
            summary = f"ARP op {arp.op}"
            info = "Protocolo de controlo ARP"

        return {
            "protocol": "ARP",
            "sender_mac": arp.hwsrc,
            "target_mac": arp.hwdst,
            "info": info,
            "summary": summary
        }
    return None


def IPProcesser(packet: Packet):
    if packet.haslayer(IP):
        ip = packet[IP]

        return {
            "version": ip.version,
            "header_length": ip.ihl,
            "len": ip.len,
            "id": ip.id,
            "flags": str(ip.flags) if ip.flags else "0",
            "offset": ip.frag,
            "protocol": ip.proto,
            "ttl": ip.ttl,
            "src": ip.src,
            "dst": ip.dst,
            "summary": "Datagrama Fragmentado" if (ip.frag != 0 or ip.flags.MF) else "Datagrama Normal"
        }
    return None


def ICMPProcesser(packet: Packet):
    if packet.haslayer(ICMP):
        icmp = packet[ICMP]

        if icmp.type == 8:
            summary = "ICMP echo request"
        elif icmp.type == 0:
            summary = "ICMP echo reply"
        elif icmp.type == 3:
            summary = "Destination unreachable"
        elif icmp.type == 11:
            summary = "Time exceeded"
        else:
            summary = f"ICMP type {icmp.type}"

        return {
            "protocol": "ICMP",
            "type": icmp.type,
            "code": str(icmp.code),
            "summary": summary,
        }
    return None

def IPv6Processer(packet: Packet):
    if packet.haslayer(IPv6):
        ip6 = packet[IPv6]

        return {
            "version": ip6.version,
            "traffic_class": ip6.tc,
            "flow_label": ip6.fl,
            "payload_length": ip6.plen,
            "next_header": ip6.nh,
            "hop_limit": ip6.hlim,
            "src": ip6.src,
            "dst": ip6.dst,
            "summary": "Datagrama IPv6"
        }

    return None


def TCPProcesser(packet: Packet):
    if packet.haslayer(TCP):
        tcp = packet[TCP]

        flags = tcp.flags

        if flags == "S":
            summary = "TCP SYN"
        elif flags == "SA":
            summary = "TCP SYN-ACK"
        elif flags == "A":
            summary = "TCP ACK"
        elif flags == "F":
            summary = "TCP FIN"
        elif flags == "R":
            summary = "TCP RST"
        else:
            summary = "TCP"

        # APP LAYER
        app_protocol = None

        if tcp.dport == 80 or tcp.sport == 80:
            app_protocol = "HTTP"
        elif tcp.dport == 443 or tcp.sport == 443:
            app_protocol = "HTTPS"
        elif tcp.dport == 22 or tcp.sport == 22:
            app_protocol = "SSH"
        elif tcp.dport == 21 or tcp.sport == 21:
            app_protocol = "FTP"

        if app_protocol:
            summary += f" ({app_protocol})"

        summary += f" {tcp.sport} → {tcp.dport}"

        return {
            "protocol": "TCP",
            "srcPrt": tcp.sport,
            "dstPrt": tcp.dport,
            "app_protocol": app_protocol,
            "summary": summary,
        }

    return None

def UDPProcesser(packet: Packet):
    if not packet.haslayer(UDP):
        return None

    udp = packet[UDP]

    app_protocol = None
    extra = None

    # DHCP
    if udp.sport in [67, 68] or udp.dport in [67, 68]:
        app_protocol = "DHCP"

        if packet.haslayer(DHCP):
            dhcp = packet[DHCP]

            msg_types = {
                1: "Discover",
                2: "Offer",
                3: "Request",
                5: "ACK",
            }

            for opt in dhcp.options:
                if isinstance(opt, tuple) and opt[0] == "message-type":
                    extra = msg_types.get(opt[1], str(opt[1]))
                    break

    # DNS
    elif udp.dport == 53 or udp.sport == 53:
        app_protocol = "DNS"

    # NTP
    elif udp.dport == 123 or udp.sport == 123:
        app_protocol = "NTP"

    # Summary (igual lógica ao TCP)
    summary = "UDP"

    summary += f" {udp.sport} → {udp.dport}"

    if app_protocol:
        summary += f" {app_protocol}"

    if extra:
        summary += f" {extra}"

    return {
        "protocol": "UDP",
        "srcPrt": udp.sport,
        "dstPrt": udp.dport,
        "app_protocol": app_protocol,
        "summary": summary,
    }
