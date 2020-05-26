#!/usr/bin/env bash

# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Initiate Ansible playbook script

. ../../openrc.sh; ansible-playbook -i hosts assignment2.yaml

# Tags can be used as follows:
# . ../../openrc.sh; ansible-playbook -i hosts assignment2.yaml --tags="frontend"