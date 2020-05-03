#!/usr/bin/env bash

. ../../openrc.sh; ansible-playbook -i hosts --ask-become-pass assignment2.yaml -vv