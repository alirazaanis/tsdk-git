"""
Telecom Systems Development Kit - tsdk
"""

import os
import re

import paramiko
from paramiko_expect import SSHClientInteraction


def strip_ansi_codes(s):
    return re.sub(r'\x1b\[([\d,A-Z]{1,2}(;\d{1,2})?(;\d{3})?)?[m|K]?', '', s)


HOST = '10.242.66.8'
USERNAME = 'fmehmoo1'
PASSWORD = 'PassCode@987'
PORT = '5023'


class Connectivity:
    def __init__(self, HOST, USERNAME, PASSWORD, PORT, display_exec_msg):

        self.HOST = HOST
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.PORT = PORT
        self.display_exec_msg = display_exec_msg
        self.display = False
        self.client = None
        self.interact = None
        self.oss_PROMPT = None

        self.bts_PROMPT = r'.*>\s+$'

        self.ex_script_cmds = True
        self.oss_connected = False
        self.bts_connected = False

        self.response = None
        self.all_output = []
        self.bts_alive = False

        self.gen_oss_prompt()

    def gen_oss_prompt(self):

        # generate the OSS prompt which the paramiko will check after execution of commands
        # need to adjust accordingly to server trying to connect

        if self.HOST == '10.242.66.8':
            # self.oss_PROMPT = r'.*fmehmoo1\@scp\-3\-scripting\(syleenm1\).*'
            self.oss_PROMPT = r'.*fmehmoo1.*'

    def connect_oss(self):
        try:
            self.all_output.append('Connecting to OSS...')
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.HOST, port=self.PORT, username=self.USERNAME, password=self.PASSWORD,
                                look_for_keys=False)
            self.interact = SSHClientInteraction(self.client, timeout=30, display=self.display,
                                                 output_callback=self.display_exec_msg)
            self.interact.expect(self.oss_PROMPT)
            cmd_output_ls = self.interact.current_output_clean
            self.all_output.append(cmd_output_ls)
            self.oss_connected = True
        except Exception as e:
            print(str(e))
            self.oss_connected = False
            # cmd_output_ls = interact.current_output
            self.all_output.append('Failed to connect to OSS')
            # if cmd_output_ls:
            #     self.all_output.append(cmd_output_ls)
            self.all_output.append('Value:: ' + str(e))

    def disconnect_oss(self):
        print('Disconnecting OSS Now')
        if self.oss_connected:
            self.all_output.append('Disconnecting OSS...')
            self.interact.send('exit')
            # self.interact.expect()
            self.oss_connected = False
            self.client.close()

    def check_bts_connectivity(self, bts_ip):
        self.bts_alive = False
        # ping_cmd = 'ping ' + bts_ip
        ping_cmd = 'ping -c 3 ' + bts_ip
        ping_output = self.send_cmd(ping_cmd, self.oss_PROMPT)
        result = re.match(r'^.*is alive.*$', ping_output)
        regex = re.compile(r'.* ([1-9]) received, .*$', re.MULTILINE)
        matches = [m.groups() for m in regex.finditer(ping_output)]
        # print(matches)
        if matches:
            # eq_lst = [int(m[0]) for m in matches]
            eq_lst = int(matches[0][0])
            print(eq_lst)
        else:
            print('no match in ping output')
        if result or matches:
            self.bts_alive = True
        else:
            print('ping commands no response. Now Amos in bts to check')
            self.connect_bts(bts_ip)
            if self.bts_connected:
                self.bts_connected = False
                self.disconnect_bts()

    def connect_bts(self, bts_ip):
        # Checking ip contact...Not OK
        # Checking ip contact...OK
        print('Amos to BTS ', bts_ip)
        cmd = 'amos ' + bts_ip
        # Prompt = r'Checking ip contact\.\.\..*'
        Prompt = r'.*>\s+$|Unable to connect to.*'
        output = self.send_cmd(cmd, Prompt)
        if output:
            regex = re.search(r'Checking ip contact\.\.\.OK.*', output, re.MULTILINE)
            if regex:
                self.bts_alive = True
                self.bts_connected = True
                print('Amos OK')
            else:
                self.bts_alive = False
                self.bts_connected = False
                print('Amos NOK')
        else:
            self.bts_alive = False
            self.bts_connected = False
            print('Amos NOK')

    def disconnect_bts(self, ):
        print('Disconnecting BTS...')
        cmd = 'exit'
        Prompt = self.oss_PROMPT
        output = self.send_cmd(cmd, Prompt)
        self.all_output.append(output)
        self.bts_connected = False

    def send_cmd(self, cmd, PROMPT=None):
        cmd_output_ls = None
        try:
            if PROMPT is None:
                PROMPT = self.bts_PROMPT
            self.all_output.append("Command Sent <" + cmd + ">")
            # print('Command Send--->',cmd)
            if self.ex_script_cmds:
                self.interact.send(cmd)
                self.interact.expect(PROMPT)
                cmd_output_ls = strip_ansi_codes(self.interact.current_output_clean)
                print('raw ouput-->', self.interact.current_output)
                if cmd_output_ls:
                    self.all_output.append(cmd_output_ls)
                    # print(cmd_output_ls)
            return cmd_output_ls
        except Exception as ex:
            print('Exception in Send command')
            return cmd_output_ls

    @staticmethod
    def get_logfile(cmd_output_ls):
        log_file = ''
        log_file_output = strip_ansi_codes(cmd_output_ls)
        result = re.match(r'^\s*Logging to file:\s*(.*\.log)', log_file_output)
        if result:
            print("-------------\t log file found >" + result[1])
            log_file = result[1]
            # self.update_msg2.emit("Output Logs file for " + rnc + ": " + log_file)
        else:
            # self.update_msg2.emit("Output Logs file error")
            print("Log file not found")
        return log_file


def display_exec_msg(msg):
    print(msg)


class Implementation:

    def __init__(self):
        pass

    def main(self):

        self.remote_path = r'/home/shared/fmehmoo1/Scripts/'
        self.local_path = r'D:\scripts'
        self.files = ['L700_V123.txt', 'L700_V11.txt', 'L700_V122.txt', 'L700_V124.txt']
        self.files = ['L700_V123.txt', 'L700_V11.txt']
        self.bts_info = ['NJ01059A']
        # self.upload(self.remote_path, self.local_path,self.files)
        self.conectivity()

    def conectivity(self):
        # Initiate connection object
        oss_con = Connectivity(HOST, USERNAME, PASSWORD, PORT, display_exec_msg)
        # connect to oss
        oss_con.connect_oss()
        # check if connected to oss
        if oss_con.oss_connected:
            print('Connected to host')
            # cmd = 'time'
            # response = oss_con.send_cmd(cmd, oss_con.oss_PROMPT)
            # cmd = 'ls -ltr'
            # response = oss_con.send_cmd(cmd, oss_con.oss_PROMPT)
            for bts in self.bts_info:
                # cmd = r'cat /opt/ericsson/amos/moshell/sitefiles/ipdatabase | grep -i NJ01059A'
                cmd = r'cat /opt/ericsson/amos/moshell/sitefiles/ipdatabase | egrep -h NJ01059A'
                response = oss_con.send_cmd(cmd, oss_con.oss_PROMPT)
                # print(response)
                parsed_output = response.split('\n')
                parsed_output = parsed_output[1:-1]
                # print(parsed_output)
                for line in parsed_output:
                    print('line-->', line)
                    temp = line.split()
                    print('parsed_output->>', temp[0])
            output = {}
            # for bts in self.bts_info:
            #     oss_con.check_bts_connectivity(bts)
            #
            #     print(' Connectiving to bts {}'.format(bts))
            #     # if bts connectivity is ok
            #     if oss_con.bts_alive:
            #
            #         # connect to bts now
            #         oss_con.connect_bts(bts)
            #         print('connected to bts')
            #
            #         # check if connected to bts ok
            #         if oss_con.bts_connected:
            #             # sample command to send to bts after connected
            #
            #             output[str(bts)] = []
            #
            #             for script in self.files:
            #                 cmd ='run ' + os.path.join(self.remote_path,script)
            #                 print('\tImplementing script --->{}',cmd)
            #                 # response of the command --> do whatever required simeple print or save in file ...
            #                 response = oss_con.send_cmd(cmd)
            #
            #                 output[str(bts)].append(response)
            #
            #             # #------------optional -----------------
            #             # #sample command -2 . this will enable loggin on the oss side -- optiional depends on scenario
            #             # cmd = 'l+'
            #             # response = oss_con.send_cmd(cmd)
            #             # # auto generated log file on the oss , depends on if l+ command is sent or not
            #             # log_file = oss_con.get_logfile(response)
            #             # print('log_file-->', log_file)
            #             # # ------------optional -----------------
            #             #
            #             # # repeat above cmds procedure as required
            #             #
            #             #
            #             # #send command if l+ is sent before otherwise skip this
            #             # cmd = 'l-'
            #             # response = oss_con.send_cmd(cmd)
            #
            #             # disconnect the BTS once done
            #             oss_con.disconnect_bts()
            #
            #         else:
            #             print('Failed to Connect to BTS')
            #
            #     else:
            #         print('BTS {} not Reachable...'.format(bts))
            #
            #
            # dis connect the OSS
            oss_con.disconnect_oss()
            print('Respnose print')
            # print(oss_con.all_output)
            with open(os.path.join(self.local_path, 'logs.txt'), 'w') as file:
                file.writelines('\n'.join(oss_con.all_output))
        else:
            print('Failed to connect OSS')

    @staticmethod
    def upload(remote_path, local_path, files):
        transport = paramiko.Transport((HOST, int(PORT)))
        transport.connect(username=USERNAME, password=PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        import os
        if isinstance(files, list):
            for file in files:
                sftp.put(os.path.join(local_path, file), os.path.join(remote_path, file))
        else:
            sftp.put(os.path.join(local_path, files), os.path.join(remote_path, files))
            pass
        sftp.close()
        transport.close()
        print('upload done')


if __name__ == "__main__":
    imp = Implementation()
    imp.main()
    print('Completed')
