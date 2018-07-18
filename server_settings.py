import socket
import fcntl
import struct

NETDATA_PORT = ':19999'
PLEX_PORT = ':32400'
ROUTER_ADDRESS = '192.168.1.254'
WEATHER_IP = '192.168.1.75'


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                        0x8915,
                                        struct.pack('256s',
                                                    ifname[:15].encode())
                                        )[20:24])
