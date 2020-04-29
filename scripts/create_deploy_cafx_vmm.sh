#!/bin/bash

set -o nounset -o pipefail -ex

# Load all the env variables from setup.env to make available for ansible 
set -o allexport
source "$(dirname "$0")"/setup.env
set +o allexport

usage() {
  echo "Usage: $0 [  ] [ -c ] [ -d ]" 1>&2
  exit 1
}

while getopts ":cdfh" opt; do
  case ${opt} in
    c ) CLEANUP="true"
      ;;
    f ) FORCE_CLEANUP="true"
      ;;
    d ) DEBUG="true"
      ;;
    h ) 
        usage
      ;;
  esac
done

# set vault information
extra_args="--extra-vars ${extra_args:-}"
  
if [ ! -z "${DEBUG:-}" ]; then
  export ANSIBLE_VERBOSITY=3
fi

if [ -n "${CLEANUP:-}" ] || [ ! -z "${FORCE_CLEANUP:-}" ]; then
  read -p "You are going to execute destructive operation. Are you sure (y/N)? " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
       echo "Aborted."
       exit 1
  fi
  # Run playbook cleanup
  echo CLEANING: CAFX VMM topology
  ansible-playbook -i inventory/pod ${extra_args:-} playbooks/vmm_cleanup.yml
else
  # Run playbook creation
  echo RUNNING: CAFX VMM topology playbooks
  ansible-playbook -i inventory/ ${extra_args:-} playbooks/provision_vmm.yml ${TAGS:-}
  ansible-playbook -i inventory/${VMM_TOPO_TYPE} ${extra_args:-} playbooks/deploy_cafx_vmm.yml ${TAGS:-}
fi

