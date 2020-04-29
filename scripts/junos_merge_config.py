#!/usr/bin/python
# --------------------------------
# This python script will merge configuration on the fabric devices
# If merge is failed, it will rollback-commit and quit the connection
# --------------------------------
import os, sys, logging, getpass, time
import argparse
from pprint import pprint
from jnpr.junos import Device
import jnpr.junos.exception 
from jnpr.junos.utils.config import Config

class MergeJunosConfig(object):
    def __init__(self, options):
        self.opt = options

    def connect_2_device(self, username='root', passwd='Embe1mpls', gather_facts=True):
        print 'Connecting.. '+ self.opt.host_ip
        print 'Username...'+ username
        print 'Password..'+ passwd
        self.dev_res = Device(host=self.opt.host_ip, user=username, password=passwd, gather_facts=gather_facts)
        try:
            self.dev_res.open()
            #pprint(self.dev_res.facts)
            #print dir(self.dev_res)
            return self.dev_res
        except jnpr.junos.exception.ConnectAuthError as err:
            print('\nConnect failed, Bad credentials : ')
            print(err.message)
            return None
        except jnpr.junos.exception.ConnectTimeoutError as err:
            print('\nConnect failed, Timeout : ')
            print(err.message)
            return None
        except jnpr.junos.exception.ConnectRefusedError as err:
            print('\nConnect failed, Refused : ')
            print(err.message)
            return None
        except Exception as err:
            print('\nConnect failed, unknown error type : ')
            print(err.message)
            return None

    def merge_junos_config(self, merge=True, overwrite=False):
        print 'Merging config to.. '+ self.opt.host_ip
        cfg = Config(self.dev_res)
        #print dir(cfg)
        try:
            cfg.load(path=self.opt.cfg_file, format='text', merge=merge, overwrite=overwrite)
        except jnpr.junos.exception.ConfigLoadError as err:
            print('\nThere were some errors/warnings while loading the config :')
            print(err.message)
            self.rollback_and_quit()
            return None
        #print(cfg.diff())
        try:
            cfg.commit(comment='Junos configuration committed via Ansible deployment')
        except jnpr.junos.exception.CommitError as err:
            print('\nCommit fail happened on' + self.opt.host_ip)
            print(err.message)
            self.rollback_and_quit()
            return None
        return True

    def rollback_and_quit(self):
        print 'Rollback config on.. '+ self.opt.host_ip
        cfg = Config(self.dev_res)
        cfg.rollback()
        print('\nRollback done on' + self.opt.host_ip)
        print('Closing connection...' + self.opt.host_ip)
        self.dev_res.close()
        sys.exit(0)

    def close_connection(self):
        print('Closing connection...' + self.opt.host_ip)
        self.dev_res.close()
        sys.exit(0)


def parse_options(args):
    parser = argparse.ArgumentParser(
            description='Merge junos configuration on to fabric devices'
            )
    parser.add_argument('--device_ip', dest='host_ip', help='Fabric device IP address')
    parser.add_argument('--cfg_file', dest='cfg_file', help='The device configuration file')

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    options = parse_options(sys.argv[1:])
    #print options
    commit = MergeJunosConfig(options)
    res = commit.connect_2_device()
    if res is not None:
        commit.merge_junos_config()
        commit.close_connection()
    sys.exit(1)
