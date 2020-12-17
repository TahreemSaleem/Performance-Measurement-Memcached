#!/bin/bash

#systemctl start memcached
#sudo service ssh start
/usr/sbin/sshd -f /home/ubuntu/.ssh/sshd_config
tail -f /dev/null

