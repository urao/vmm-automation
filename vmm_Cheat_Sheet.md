### Useful commands

#### Create a new topology
```
vmm config <config_file> -g vmm-default
vmm bind
vmm start
vmm list
vmm ping
```
#### Destroy exisiting topology
```
vmm stop
vmm unbind
```
#### Operational commands on VMM
```
vmm args vmx_gw
vmm ip
vmm ip | grep -v fpc | grep -v cosim | grep -v MPC | awk '{print $2}'
vmm capacity
vmm start <name_of_device>
vmm serial <name_of_device>
vmm stop <name_of_device>
```
