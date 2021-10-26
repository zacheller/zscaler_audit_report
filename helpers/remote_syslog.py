import logging
import logging.handlers
import socket


class SendLogs(object):
    """
    Class to send logs to a remote sys log server
    """

    def __init__(self, ip, port, protocol):
        """
        :param ip: type str. IP address of the remote syslog server
        :param port: type int. Service port
        :param protocol: type int. TCP or UDP
        """
        self.remote_logger = logging.getLogger('MyLogger')
        self.remote_logger.setLevel(logging.INFO)
        self.handler = self._select_handler(ip, protocol, port)
        self.remote_logger.addHandler(self.handler)
        self.version = '1.0'

    def _select_handler(self, ip, protocol, port):
        """
        Internal method that configures syslog handler, based on ip, port and protocol
        :param ip: type str: IP address of the remote syslog server
        :param protocol: type str. TCP or UDP
        :param port: type int. Service port
        : return None
        """
        if 'tcp' in protocol.lower():
            socket_type = socket.SOCK_STREAM
        elif 'udp' in protocol.lower():
            socket_type = socket.SOCK_DGRAM
        else:
            raise ValueError("Invalid protocol")
        try:
            handler = logging.handlers.SysLogHandler(address=(ip, port), socktype=socket_type)
            handler.setFormatter(logging.Formatter('%(message)s'))
        except (socket.herror, socket.error):
            raise ValueError(f"Socket Error. Review Firewall rules and confirm server is listening on"
                             f" port {protocol} {port}")
        return handler

    def send_logs(self, msg):
        self.remote_logger.info(msg)
