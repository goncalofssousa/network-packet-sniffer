from scapy.all import AsyncSniffer, IFACES
from src.packet_processer import (
    IPProcesser,
    ARPProcesser,
    IPv6Processer,
    EthernetProcesser,
    ICMPProcesser,
    TCPProcesser,
    UDPProcesser,
)
from src.parser import parse_filter
from typing import Optional
import datetime
import math
import threading

_current_log_file = None
_interface = None
_sniffer: Optional[AsyncSniffer] = None
_history = []
_filter = ""
_page = 1
_is_stopping = False
_packet_id = 0


def getInterface():
    return _interface


def setInterface(interface):
    global _interface
    if interface not in getInterfaces():
        raise ValueError("Interface Inválida")
    _interface = interface
    destroySniffer()


def setSniffer():
    global _sniffer
    _sniffer = AsyncSniffer(
        iface=getInterface(),
        prn=lambda x: _processPacket(x),
        store=False,
    )


def destroySniffer():
    global _sniffer
    if _sniffer:
        if _sniffer.running:
            _sniffer.stop()
        _sniffer = None


def startSniffer():
    from components.dashboard import hideBeforeButton, hideAfterButton, setStartStatus

    global _page, _current_log_file, _is_stopping, _packet_id
    _is_stopping = False
    _packet_id = 0
    _history.clear()
    if not _sniffer:
        setSniffer()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _current_log_file = f"log_{ts}.json"

    import json

    with open(_current_log_file, "w") as f:
        json.dump([], f)

    _sniffer.start()
    _page = 1

    hideBeforeButton()
    hideAfterButton()
    setStartStatus()


def stopSniffer():
    global _sniffer, _is_stopping
    if _is_stopping:
        return

    _is_stopping = True

    def shutdown():
        global _sniffer, _is_stopping
        try:
            if _sniffer and _sniffer.running:
                _sniffer.stop()
        except:
            pass
        finally:
            _sniffer = None
            _is_stopping = False
            from components.dashboard import setStopStatus

            setStopStatus()

    threading.Thread(target=shutdown, daemon=True).start()


def getInterfaces():
    return sorted(IFACES.data.values(), key=lambda x: x.name)


def _processPacket(packet):
    global _is_stopping, _sniffer

    if _is_stopping or _sniffer is None:
        return
    from components.dashboard import (
        receivePacket,
        showAfterButton,
        setPacketCounter,
        setMaxPage,
    )

    global _packet_id
    _packet_id += 1

    layer2_eth = EthernetProcesser(packet)
    layer2_arp = ARPProcesser(packet)
    layer2 = {}
    if layer2_eth:
        layer2["ethernet"] = layer2_eth

    if layer2_arp:
        layer2["arp"] = layer2_arp

    if not layer2:
        layer2 = None

    layer3_ip = IPProcesser(packet)
    layer3_icmp = ICMPProcesser(packet)
    layer3_ipv6 = IPv6Processer(packet)

    layer3 = None
    if layer3_ip or layer3_icmp or layer3_ipv6:
        layer3 = {}
        if layer3_ip:
            layer3["ip"] = layer3_ip
        if layer3_icmp:
            layer3["icmp"] = layer3_icmp
        if layer3_ipv6:
            layer3["ipv6"] = layer3_ipv6

    layer4_tcp = TCPProcesser(packet)
    layer4_udp = UDPProcesser(packet)
    layer4 = layer4_tcp or layer4_udp

    if not layer2 and not layer3 and not layer4:
        return

    if layer3_ipv6:
        src = layer3_ipv6.get("src")
        dst = layer3_ipv6.get("dst")
    elif layer3_ip:
        src = layer3_ip.get("src")
        dst = layer3_ip.get("dst")
    elif layer2_eth:
        src = layer2_eth.get("src_mac")
        dst = layer2_eth.get("dst_mac")
    elif layer2_arp:
        src = layer2_arp.get("sender_mac")
        dst = layer2_arp.get("target_mac")
    else:
        src = None
        dst = None

    if layer4:
        protocol = layer4.get("app_protocol") or layer4.get("protocol")
        summary = layer4.get("summary")

    elif layer3_icmp:
        protocol = layer3_icmp.get("protocol")
        summary = layer3_icmp.get("summary")
    elif layer3_ipv6:
        protocol = "IPv6"
        summary = layer3_ipv6.get("summary")
    elif layer3_ip:
        protocol = "IP"
        summary = layer3_ip.get("summary")

    elif layer2_arp:
        protocol = layer2_arp.get("protocol")
        summary = layer2_arp.get("summary")

    elif layer2_eth:
        protocol = layer2_eth.get("protocol")
        summary = layer2_eth.get("summary")

    if not summary:
        summary = "-"

    data = {
        "layer2": layer2,
        "layer3": layer3,
        "layer4": layer4,
        "packet_id": _packet_id,
        "timestamp": datetime.datetime.fromtimestamp(float(packet.time)).strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        "length": len(packet),
        "src": src,
        "dst": dst,
        "protocol": protocol,
        "summary": summary,
    }

    _history.append(data)

    if _current_log_file:
        write_to_log(data)

    if _filter:
        filtered = parse_filter(_filter, _history)
    else:
        filtered = _history

    length = len(filtered)
    total_pages = math.ceil(length / 10) if length > 0 else 1

    setMaxPage(total_pages)

    # só mostra se estiver na página atual
    if length <= 10 * _page:
        if not _filter or data in filtered:
            receivePacket(data)
    else:
        showAfterButton()
    setPacketCounter(length)


def getHistory(page=None):
    from components.dashboard import receivePacket, setPacketCounter, setMaxPage

    start = (_page - 1) * 10
    end = start + 10

    if _filter:
        filtered = parse_filter(_filter, _history)
    else:
        filtered = _history

    total = len(filtered)
    total_pages = math.ceil(total / 10) if total > 0 else 1

    if page is not None:
        setPage(page, length=total)

    setMaxPage(total_pages)
    setPacketCounter(total)

    page_data = filtered[start:end]

    for e in page_data:
        receivePacket(e)


def setFilter(f):
    global _filter, _page

    _filter = f
    setPage(1)


def setPage(page, length=None):
    from components.dashboard import (
        showBeforeButton,
        hideBeforeButton,
        showAfterButton,
        hideAfterButton,
    )

    global _page
    _page = page

    if length is None:
        if _filter:
            data = parse_filter(_filter, _history)
        else:
            data = _history
        length = len(data)

    total_pages = max(1, math.ceil(length / 10))

    if page > 1:
        showBeforeButton()
    else:
        hideBeforeButton()

    if page < total_pages:
        showAfterButton()
    else:
        hideAfterButton()


def setNextPage():
    setPage(_page + 1)


def setPreviousPage():
    setPage(_page - 1)


def downloadHistory(filepath: str = None):
    import json

    target = parse_filter(_filter, _history) if _filter else _history

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if filepath is None:
        filepath = f"history_{ts}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=4, ensure_ascii=False)

    return filepath


def write_to_log(data):
    import json
    import os

    try:
        with open(_current_log_file, "r+") as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)  # Remove o último ]

            # Se não for o primeiro pacote, adiciona uma vírgula
            if len(_history) > 1:
                f.write(",")

            f.write(json.dumps(data, indent=4))
            f.write("]")  # Fecha a lista novamente
    except Exception as e:
        print(f"Erro ao gravar log: {e}")
