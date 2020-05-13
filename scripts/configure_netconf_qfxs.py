#!/usr/bin/python
# --------------------------------
# This python script will get interface IP address configured on the fabric devices
# --------------------------------
import os, sys, logging, getpass, time
import argparse
import paramiko
from socket import error as SocketError

class CommitConfig(object):
    def __init__(self, address):
        self.host_ip = address
        self.username = 'root'
        self.password = 'Embe1mpls'

    def connect_2_device(self):
        print 'Connecting.. '+ self.host_ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try: 
            self.client.connect(self.host_ip, username=self.username, password=self.password)
            #print self.client
            return self.client
        except SocketError as err:
            print('\nSocket error: ')
            print(err.message)
            return None
        except paramiko.AuthenticationException as err:
            print('\nConnect failed, Auth error : ')
            print(err.message)
            return None
        except Exception as err:
            print('\nConnect failed, unknown error type : ')
            print(err.message)
            return None

    def commit_config(self):
        print 'Commit configuration .. '+ self.host_ip
        configure = self.client.invoke_shell()
        configure.send('cli\n')
        configure.send('configure\n')
        configure.send('set system services ssh\n')
        configure.send('set system services netconf ssh\n')
        configure.send('set system services netconf traceoptions file netconf-ops.log\n')
        configure.send('set system services netconf traceoptions file size 3m\n')
        configure.send('set system services netconf traceoptions file files 20\n')
        configure.send('set system services netconf traceoptions file world-readable\n')
        configure.send('set system services netconf traceoptions flag all\n')
        configure.send('commit\n')
        configure.send('quit\n')
        time.sleep(2)
        print 'Commit Done!'
        #op = configure.recv(1048576)
        #print op

    def close_connection(self):
        print('Closing connection...' + self.host_ip)
        self.client.close()


def parse_options(args):
    parser = argparse.ArgumentParser(
            description='Commit netconf configuration on vQFX fabric devices'
            )
    parser.add_argument('-a', '--device_ip', required=True, help='Fabric device IP address')

    opt = parser.parse_args()
    return opt

def main(argv):
    options = parse_options(argv)
    config = CommitConfig(options.device_ip)
    res = config.connect_2_device()
    if res is not None:
        config.commit_config()
        config.close_connection()

if __name__ == "__main__":
    main(sys.argv[1:])
