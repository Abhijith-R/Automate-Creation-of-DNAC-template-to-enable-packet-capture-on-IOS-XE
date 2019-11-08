[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Abhijith-R/Automate-Creation-of-DNAC-template-to-enable-packet-capture-on-IOS-XE)

# Packet_Capture_Automation_IOS-XE
A python script to automate the packet capture on IOS-XE, create a pcap file and copy it to local machine using secure copy and also automate the creation of a DNAC template to configure packet capture on a switch and push the pcap file to a remote ftp server for further processing. This script can be used to configure packet capture on multiple switches registered in DNAC.

### Author:

* Abhijith R (abhr@cisco.com)
*  Oct 2019
***

### Prerequisites
* Python 2.7
* PyCharm/Any text editor
* Make sure SCP is enabled on the remote device ```ip scp server enable``` if ```controller.py``` is used.

### Steps to Reproduce
* Download/clone the repository
* Install the requirements using requirements.txt using ```pip install -r requirements.txt```
* There are two python files which can be executed for two different requirements 
* ```controller.py``` - Python script which connects to the switch with the credentials using ssh, creates a capture and copies  pcap file from the switch to the local machine
* ```dnac_template.py``` - Python script with the help of DNAC REST API automates the creation of a template, commit and deploy the template to configure packet capture on the switch registered with DNAC and copies the pcap file to a ftp server for further processing.
* Execute controller.py/dnac_template.py using a text editor such as pycharm
* Terminal can also be used to run the script.
      ```python controller/dnac_template.py```

### Screenshots

![alt text](https://github.com/Abhijith-R/Automate-Creation-of-DNAC-template-to-enable-packet-capture-on-IOS-XE/blob/master/Python_Terminal1.png)

![alt text](https://github.com/Abhijith-R/Automate-Creation-of-DNAC-template-to-enable-packet-capture-on-IOS-XE/blob/master/dnac_screenshot.png)

### API Reference/Documentation:
* [Embedded Packet Capture for Cisco IOS and IOS-XE](https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-embedded-packet-capture/116045-productconfig-epc-00.html)
* [Programmability Configuration Guide, Cisco IOS XE](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/169/b_169_programmability_cg/cli_python_module.html)
* [DNA Center REST API Documentation] (https://developer.cisco.com/docs/dna-center/#!using-the-cisco-dna-center-api-documentation)
* [DNA Center Platform Overview] (https://developer.cisco.com/docs/dna-center/)

### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
    
