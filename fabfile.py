import boto, urllib2
from   boto.ec2 import connect_to_region
from   fabric.api import env, run, cd, settings, sudo
from   fabric.api import parallel
import os
import sys

REGION       = os.environ.get("AWS_EC2_REGION")

# Server user, normally AWS Ubuntu instances have default user "ubuntu"
env.user      = "centos"

# List of AWS private key Files
env.key_filename = ["~/.ssh/ao-poc-user-key.pem"]

# Fabric task to restart Apache, runs in parallel
# To execute task using fabric run following
# fab set_hosts:phpapp,2X,us-west-1 restart_apache

@parallel
def start_test():
    run('cd /home/centos/ao-client-pubnub && ./run.sh 4', pty=False)

@parallel
def check_count():
    run('ps -ef | grep node | grep -v grep', pty=False)

@parallel
def stop_test():
    run('cd /home/centos/ao-client-pubnub && ./kill.sh', pty=False)

# Your custom Fabric task here after and run them using,
# fab set_hosts:phpapp,2X,us-west-1 task1 task2 task3

@parallel
def git_pull():
    run('cd /home/centos/ao-client-pubnub && git pull', pty=False)

@parallel
def free():
    run('free -m', pty=False)

@parallel
def npm_update():
    run('cd /home/centos/ao-client-pubnub && npm update', pty=False)

# Fabric task to set env.hosts based on tag key-value pair
def set_hosts(tag = "aws:ec2spot:fleet-request-id", value="*", region=REGION):
    key              = "tag:"+tag
    env.hosts    = _get_public_dns(region, key, value)

# Private method to get public DNS name for instance with given tag key and value pair
def _get_public_dns(region, key, value ="*"):
    public_dns   = []
    connection   = boto.ec2.connect_to_region(region)
    reservations = connection.get_all_instances(filters = {key : value})
    for reservation in reservations:
        for instance in reservation.instances:
            print "Instance", instance.public_dns_name
            public_dns.append(str(instance.public_dns_name))
    return public_dns
