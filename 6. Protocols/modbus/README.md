# Modbus protocol
_Maurice Snoeren, 19 November 2022_

Modbus was created for the industrial control systems and it is a serial protocol. It was created in the late 1970s by Modicon, which is now Scheinder Electric. It was used to communicate with their programmable logic controllers (PLCs) that where used within industrial control systems (ICS). Modbus is very simple and still used as today. It was not invented with security in mind and therefore it is also vulnerable for attacks when exposed. In order to work with Ethernet networks, it has been altered to work on the TCP/IP stack and it uses the default port 502.

# Protocol: Modbus RTU
The Modbus packet frame can be broken down into two sections: the Application Data Unit (ADU) and the Protocol Data Unit (PDU). The ADU consists out of a Adress, PDU, and an Error Checking method. The PDU consist out of the function code (FC) and the data sections of the Modbus frame. An example of a frame is shown below and is known as the Modbus RTU (Remote Telemetry Unit):

| Slave Address | Function Code | Data 1 | ... | Data n | |

# Protocol: Modbus+, Modbus ASCII, Modbus TCP/IP, Modbus over TCP/IP
The Modbus RTU differs from all the other versions of Modbus, like Modbus TCP/IP. One difference is between Modbus TCP/IP and Modbus over TCP/IP is in Modbus TCP/IP, there is no checksum inside of the payload of the packet, like in Modbus RTU. Modbus TCP/IP is composed of an ADU and PDU, where the ADU consists out of a Modbus Application (MBAP) header and the PDU. The MBAP header is containing the Transaction ID, Protocol ID, Length and Unit ID. The PDU has the same structure as in the Modbus RTU with the function code (FC) and data payloads. The Modbus function code helps to determine the nature of the packet. For example, the function code 0x2b is a Read Device Identification function code. It asks for information from the device, such as PLC manufacturer and model number. The packets looks like:

| Transaction ID | Protocol ID | Length | Unit ID | Function Code | Data |

Example: | 00 00 | 00 00 | 00 05 | 00 | 2b | 0e 03 00 |

The data sections has a specific format for each function code. For the Read Device Identification, the data is asking for specific parts that is requested from the device.

# nmap
Using nmap, a TCP/IP Modbus port can be scanned and identified. Nmap is also trying to get some device information, so you know the slave ID info. See the website https://nmap.org/nsedoc/scripts/modbus-discover.html for more information. 

```
nmap --script modbus-discover.nse --script-args='modbus-discover.aggressive=true' -p 502 <host>

PORT    STATE SERVICE
502/tcp open  modbus
| modbus-discover:
|   sid 0x64:
|     Slave ID data: \xFA\xFFPM710PowerMeter
|     Device identification: Schneider Electric PM710 v03.110
|   sid 0x96:
|_    error: GATEWAY TARGET DEVICE FAILED TO RESPONSE
```

# Function codes
The table below shows the description of the different function code. In here you also see the function code 2B that returns the device identification according to the table.

| Function Code (hex) | Function description            |
|---------------------|---------------------------------|
| 1  (01)             | Read coils                      |
| 2  (02)             | Read discrete inputs            |
| 3  (03)             | Read multiple holding registers |
| 4  (04)             | Read input registers            |
| 5  (05)             | Write single coil               |
| 6  (06)             | Write single holding resgiter   |
| 7  (07)             | Read exception status           |
| 8  (08)             | Diagnostics                     |
| 11 (0B)             | Get com event counter           |
| 12 (0C)             | Get com event log               |
| 14 (0E)             | Read device identification      |
| 15 (0F)             | Write multiple coils            |
| 16 (10)             | Write mulitple holding registers|
| 17 (11)             | Report slave register           |
| 20 (14)             | Read file record                |
| 21 (15)             | Write file record               |
| 22 (16)             | Mask write register             |
| 23 (17)             | Read/Write multiple registers   |
| 24 (18)             | Read FIFO queue                 |
| 43 (2B)             | Read device identification      |

One of the difficult aspect of Modbus, is trying to figure out what each coil and register do. These values do not have more descriptions. You need to know what is controlled by the system and how are the coils and registers attached to it. Which coil is controlling a valve for example. 

# Attacks
While it is an older protocol, Modbus does not have any security features build in. Therefore unauthicated attacks are possible and replay attacks. When you have access to the serial line or the ethernet port, you can send and receive anything to and from the server. 

# Testing
A complex pentest tool is scapy, that also has a modbus extension to pentest the modbus: https://scapy.net/. A more simple approach is the commandline Python application: https://github.com/tallakt/modbus-cli. It creates an easy tool to interact with a modbus interface. 

# Libraries
- https://www.npmjs.com/package/modbus-serial
- https://github.com/node-modbus/stream
- https://pymodbus.readthedocs.io/en/latest/readme.html
