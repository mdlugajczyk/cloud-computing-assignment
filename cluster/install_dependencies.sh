#!/bin/sh

pip install python-novaclient
pip install python-neutronclient
pip install paramiko
pip install ansible

# Packages required by tests
pip install mock
pip install mockito
pip install nose
