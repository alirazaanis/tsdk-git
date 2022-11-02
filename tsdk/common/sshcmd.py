"""
Telecom Systems Development Kit - tsdk
"""

import sys
import time
from copy import deepcopy

import paramiko
import select

from tsdk.common.sshconfig import SshConfig as _SshConfig


class Ssh:
    def __init__(self,
                 sshconfig: _SshConfig):
        self._sshconfig = deepcopy(sshconfig)

    @property
    def sshconfig(self):
        """Get Ssh Configuration

        Returns:
            SshConfig: Ssh Configuration Parameters in SshConfig Class
        """
        return self._sshconfig

    @sshconfig.setter
    def sshconfig(self, sshconfig: _SshConfig) -> None:
        """Set Ssh Configuration

        Args:
            sshconfig (SshConfig): Ssh Configuration Parameters in SshConfig class
        """
        self._sshconfig = deepcopy(sshconfig)

    def run_cmd(self, host_ip, cmd_list):
        i = 0
        while True:
            print("Trying to connect to %s (%i/%i)" % (host_ip, i, self._sshconfig.retry_time))
            try:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host_ip, port=7777, username="atec", password="atecadmin")
                break
            except paramiko.AuthenticationException:
                print("Authentication failed when connecting to %s" % host_ip)
                sys.exit(1)
            except:
                print("Could not SSH to %s, waiting for it to start" % host_ip)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
        if i >= self._sshconfig.retry_time:
            print("Could not connect to %s. Giving up" % host_ip)
            sys.exit(1)
        # After connection is successful
        # Send the command
        for command in cmd_list:
            # print command
            print("> " + command)
            # execute commands
            stdin, stdout, stderr = ssh.exec_command(command)
            # TODO() : if an error is thrown, stop further rules and revert back changes
            # Wait for the command to terminate
            while not stdout.channel.exit_status_ready():
                # Only print data if there is data to read in the channel
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        tmp = stdout.channel.recv(1024)
                        output = tmp.decode()
                        print(output)

        # Close SSH connection
        ssh.close()
        return
