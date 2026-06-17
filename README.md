# 🛡️ Network Sniffer 🌐

Este projeto consiste no desenvolvimento de um **Sniffer de Rede** em Python, utilizando a biblioteca **Scapy** para captura e manipulação de pacotes e **CustomTkinter** para uma interface gráfica (GUI) moderna e intuitiva.

A aplicação permite capturar, analisar e visualizar pacotes de rede em tempo real.

---

## 🚀 Funcionalidades

O sistema implementa as seguintes capacidades principais:

* **Captura em Tempo Real**
  Monitorização de tráfego instantânea com Scapy.

* **Análise de cabeçalho por nível protocolar**
  Decomposição dos pacotes segundo a pilha protocolar:

  * **Layer 2:** Ethernet, ARP
  * **Layer 3:** IPv4, IPv6, ICMP
  * **Layer 4:** TCP, UDP

* **Deteção de Protocolos de Aplicação**
  Identificação de HTTP, HTTPS, SSH, FTP, DNS, DHCP e NTP através da análise de portas capturadas nos pacotes TCP e UDP capturados.

* **Interface Gráfica Interativa**
  Visualização organizada dos pacotes capturados, com sistema de paginação para melhor organização.

* **Sistema de Filtragem Avançado**
  Permite isolar tráfego com expressões lógicas.

* **Exportação de Dados**
  Guarda capturas em formato **JSON**, tanto por clique do utilizador, como em modo live, cada vez que se inicia a captura.

---

## 🔍 Sistema de Filtros

Permite criar expressões lógicas para filtrar o tráfego.

### Operadores Suportados

| Tipo        | Operadores                       |
| ----------- | -------------------------------- |
| Comparação  | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Lógicos     | `and`, `or`                      |
| Agrupamento | `( )`                            |

### Campos Disponíveis

* `protocol` — protocolo do pacote
* `src` — endereço de origem (IP/MAC)
* `dst` — endereço de destino (IP/MAC)
* `length` — tamanho do pacote (bytes)
* `packet_id` — identificador único
* `timestamp` — instante da captura

### Deep Packet Inspection

Acesso a campos por camada com `layerX.campo`. Possibilidades:
### Layer4:
layer4.protocol
layer4.app_protocol
layer4.srcPrt
layer4.dstPrt

### Layer3:
`IPv4:`
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

`IPv6:`
layer3.ipv6.traffic_class
layer3.ipv6.flow_label
layer3.ipv6.payload_length
layer3.ipv6.next_header
layer3.ipv6.hop_limit
layer3.ipv6.src
layer3.ipv6.dst

`ICMP:`
layer3.icmp.protocol
layer3.icmp.type
layer3.icmp.code

### Layer2:
`ARP:`
layer2.arp.protocol
layer2.arp.sender_mac
layer2.arp.target_mac

`Ethernet`
layer2.arp.protocol
layer2.arp.src_mac
layer2.arp.dst_mac
layer2.arp.type

**Exemplos:**

```python
protocol == TCP
src == 192.168.1.1
length > 100
protocol == ICMP and length > 60
layer4.dport == 53
layer3.ip.ttl > 64
```

---

## 🐧 Instalação (Linux - Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3-venv python3-full python3-tk -y

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install scapy customtkinter pillow cryptography
```

---

## 🪟 Instalação (Windows)

```bash
pip install scapy customtkinter pillow cryptography
```

---

## 🛠️ Como Executar

⚠️ É necessário executar com privilégios de administrador/root.

### Linux

```bash
sudo ./venv/bin/python main.py
```

### Windows

Executar o terminal como administrador:

```bash
python main.py
```

---

## 🌐 Seleção de Interface

Antes de iniciar a captura, selecione uma interface de rede válida (ex: `eth0`, `wlan0`).
As interfaces são detetadas automaticamente pelo Scapy.

---

## 🧪 Execução no CORE

Para exportar a GUI:

### Sistema anfitrião

```bash
xhost +
```

### Nó CORE

* No terminal, ir até à pasta onde se encontra o sniffer 

```bash
export DISPLAY=:0
sudo -E python main.py
```

---

## 💾 Exportação

* Os pacotes são guardados automaticamente num ficheiro JSON
* Pode exportar apenas os resultados filtrados através do botão de exportação

---

## ⚠️ Notas Importantes

* **Permissões:** Sem privilégios de administrador, a captura falha
* **Interface:** Escolha a interface correta
* **Performance:** Os filtros afetam apenas a visualização, não a captura
