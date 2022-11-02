"""
Telecom Systems Development Kit - tsdk
"""

__all__ = ['SshConfig']


class SshConfig(object):
    """Ssh Configuration Object

    Args:
        host (str): Host Ip/Address
        port (int): Host Port
        uid (str): User Id
        pwd (str): Password
        retry_time (int): Retry Time
    Properties:
        All parameters are available as Get/Set properties
    """

    def __init__(self,
                 host: str,
                 port: int,
                 uid: str,
                 pwd: str,
                 retry_time: int) -> None:
        """
        Initialize Ssh Configuration
        """
        self.host: str = host
        self.port: int = port
        self.uid: str = uid
        self.pwd: str = pwd
        self.retry_time: int = retry_time
