#!/usr/bin/python
# --------------------------------
# This python script will get interface IP address configured on the fabric devices
# --------------------------------
import os, sys, logging, getpass, time
import argparse
from pprint import pprint
from jnpr.junos import Device
import jnpr.junos.exception 

class GetInformation(object):
    def __init__(self, address, interface):
        self.host_ip = address
        self.intf_name = interface

    def connect_2_device(self, username='root', passwd='Embe1mpls', normalize=True):
        #print 'Connecting.. '+ self.host_ip
        #print 'Username...'+ username
        #print 'Password..'+ passwd
        self.dev_res = Device(host=self.host_ip, user=username, password=passwd, normalize=normalize)
        try:
            self.dev_res.open()
            #pprint(self.dev_res.facts)
            #print dir(self.dev_res)
            return self.dev_res
        except jnpr.junos.exception.ConnectAuthError as err:
            #print('\nConnect failed, Bad credentials : ')
            #print(err.message)
            return None
        except jnpr.junos.exception.ConnectTimeoutError as err:
            #print('\nConnect failed, Timeout : ')
            #print(err.message)
            return None
        except jnpr.junos.exception.ConnectRefusedError as err:
            #print('\nConnect failed, Refused : ')
            #print(err.message)
            return None
        except Exception as err:
            #print('\nConnect failed, unknown error type : ')
            #print(err.message)
            return None

    def GetInterfaceIp(self):
        #print 'Get Interface IP.. '+ self.intf_name
        intf_out = self.dev_res.rpc.get_interface_information(interface_name=self.intf_name)
        intf_ip_xpath='.//logical-interface/address-family[address-family-name = \'inet\']/interface-address/ifa-local/text()'
        intf_ip = intf_out.xpath(intf_ip_xpath)
        return intf_ip

    def close_connection(self):
        #print('Closing connection...' + self.host_ip)
        self.dev_res.close()


def parse_options(args):
    parser = argparse.ArgumentParser(
            description='Get junos information on fabric devices'
            )
    parser.add_argument('-a', '--device_ip', required=True, help='Fabric device IP address')
    parser.add_argument('-i', '--interface', required=True, help='Interface name')

    opt = parser.parse_args()
    return opt

def main(argv):
    options = parse_options(argv)
    #print options
    info = GetInformation(options.device_ip, options.interface)
    res = info.connect_2_device()
    ip_list = []
    if res is not None:
        ip_list = info.GetInterfaceIp()
        info.close_connection()
    if ip_list:
        print ip_list
        #return ip_list[-1]

if __name__ == "__main__":
    main(sys.argv[1:])
