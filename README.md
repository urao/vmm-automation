### Steps to run the deployment in VMM Infra
----------------------------------------------


1. Clone the repo 
```
git clone https://github.com/urao/vmm-automation.git
```
2. Fill in the details which has string \"\__fill\__in\" script in the files
```
cd vmm-automation
grep -irn "fill__" *
```
```
scripts/setup.env:4:VMM_USERNAME=__fill__in
scripts/setup.env:20:LAPTOP_SSH_KEY="__fill__in"
scripts/setup.env:21:VMM_SSH_KEY="__fill__in"
scripts/setup.env:27:CONTRAIL_REGISTRY_USERNAME="__fill__in"
scripts/setup.env:28:CONTRAIL_REGISTRY_PASSWORD="__fill__in"
```
3. Copy Linux, vMX, vQFX images under /vmm/data/user_disks/\<username\>/ folder
4. Copy required healthbot version of the image to be installed, under /vmm/data/user_disks/\<username\>/ folder
5. For Appformix deployment, Create appropriate version folder, as per below
6. Copy Appformix and Appformix flows images in the below location based on the version
```
/vmm/data/user_disks/<username>/appformix/3_1_11/
/vmm/data/user_disks/<username>/xflow/1_0_6/
```
7. Currently supported topologies are showed [here](https://github.com/urao/vmm-automation/tree/master/automated-topologies)
8. Update scripts/setup.env file with what topology you want to deploy
```
# Available Topologies
# Demo => demo
# Healthbot => hbvm
# Contrail+Appformix => cafx
# Kubernetes Cluster => k8s

VMM_TOPO_TYPE=demo
```
9. Enable passwordless login to VMM servers
10. Run the script to deploy the selected topology [Ex. demo]
```
./scripts/create_deploy_demo_vmm.sh
```
11. Run the above script with `-c` option to cleanup the topology [Ex. demo]
```
./scripts/create_deploy_demo_vmm.sh -c
```

## References
[Ansible Doc](https://docs.ansible.com/)
