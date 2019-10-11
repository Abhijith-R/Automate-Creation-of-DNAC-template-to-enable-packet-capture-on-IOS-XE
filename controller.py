#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
               
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import paramiko
import time
from scp import SCPClient

ip_address = raw_input("Enter IP Address:")
port = 22
username = raw_input("Username:")
password = raw_input("Password:")
cap_name = raw_input("Capture Name:")
interface_name = raw_input("Interface:")
pcap_file = raw_input("PCAP file name:")
dest = raw_input("Local path to store PCAP file(Ex: /Users/username/somefolder): ")

def connect_router():
    # Establish remote connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip_address, port=port, username=username, password=password, allow_agent=False, look_for_keys=False)
    # print "Success!!!",ip_address
    return ssh_client


def send_commands():
    # Execute packet capture commands
    ssh_client = connect_router()
    remote_conn = ssh_client.invoke_shell()
    print("********************************************************")
    print("Packet capture started for a duration of 20 seconds.....")
    remote_conn.send("monitor capture "+cap_name+" interface "+interface_name+" both\n")
    remote_conn.send("monitor capture "+cap_name+" file location flash:"+pcap_file+".pcap\n")
    remote_conn.send("monitor capture "+cap_name+" match ipv4 protocol tcp any any\n")
    remote_conn.send("monitor capture "+cap_name+" start\n")
    remote_conn.send("monitor capture "+cap_name+" limit duration 20\n")
    time.sleep(25)
    remote_conn.send("monitor capture "+cap_name+" stop\n")
    time.sleep(5)
    print("Packet capture stopped with PCAP file "+pcap_file)
    # remote_conn.send("show monitor capture "+cap_name+" \n")
    # time.sleep(10)
    # output = remote_conn.recv(5000)
    # time.sleep(1)
    return


def retrieve_pcap_file():
    # Get File from Remote
    send_commands()
    ssh_client = connect_router()
    # Copy .pcap file from remote source
    scp_client = SCPClient(ssh_client.get_transport())
    scp_client.get("flash:"+pcap_file+".pcap", dest)
    print("PCAP file copied to destination "+dest)
    print("********************************************************")

if __name__ == "__main__":
    retrieve_pcap_file()
