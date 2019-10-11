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
