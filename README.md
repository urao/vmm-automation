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
3. Copy Linux, vMX, vQFX images under /vmm/data/user_disks/\<username\>/ folder
4. Create appropriate version folder, as per below
5. Copy Appformix and Appformix flows images in the below location based on the version
```
/vmm/data/user_disks/<username>/appformix/3_1_11/
/vmm/data/user_disks/<username>/xflow/1_0_6/
```
6. Update scripts/setup.env file with what topology you want to deploy
```
# Available Topologies
# Demo => demo
# Healthbot => hbvm
# Contrail+Appformix => cafx
# Kubernetes Cluster => k8s

VMM_TOPO_TYPE=demo
```
7. Run the script to deploy the selected topology
```
./scripts/create_deploy_demo_vmm.sh
```
8. Run the above script with `-c` option to cleanup the topology
```
./scripts/create_deploy_demo_vmm.sh -c
```



## References
[Ansible Doc](https://docs.ansible.com/)
