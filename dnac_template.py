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

import json
import os
import sys
import time
import requests
from requests.auth import HTTPBasicAuth

dnac = "dnac ip"
uname="your usename"
pwd="your password"

dnac_headers = {'X-Auth-Token':'',
                'content-type': 'application/json'}
dnac_session = requests.Session()
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

def get_auth_token(controller_ip):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
       """

    login_url = "https://{0}/api/system/v1/auth/token".format(controller_ip)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(uname, pwd), verify=False)
    result.raise_for_status()

    dnac_headers['X-Auth-Token'] = result.json()["Token"]
    return

def create_project():
    url = "https://{0}/dna/intent/api/v1/template-programmer/project".format(dnac)
    proj_name = raw_input("Enter a Project name")
    payload = {"name": proj_name}
    r = requests.post(url,verify=False,headers=dnac_headers,data=json.dumps(payload))
    return r.text

def select_project():
    url = "https://{0}/dna/intent/api/v1/template-programmer/project".format(dnac)

    response = requests.get(url, headers=dnac_headers,verify=False)
    resp_json = json.loads(response.text)
    out = {}
    for i in resp_json.__iter__():
        out.update({i.get(u'id'):i.get(u'name')})
    return out


def create_template(tempName,projId):
    url = "https://{0}/dna/intent/api/v1/template-programmer/project/{1}/template".format(dnac,projId)

    payload = {
        "composite": False,
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
                "productSeries": "Cisco Catalyst 9300 Series Switches"
            }
        ],
        "failurePolicy": "ABORT_ON_ERROR",
        "name": tempName,
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
        "templateContent": "#MODE_ENABLE\nmonitor capture $capture_name interface $interface_name both\nmonitor capture $capture_name file location flash:$pcap_file\nmonitor capture $capture_name match ipv4 protocol tcp any any\nmonitor capture $capture_name start\nmonitor capture $capture_name limit duration 5\nmonitor capture $capture_name stop\n#MODE_END_ENABLE",
        "templateParams": [
            {
                "parameterName": "capture_name",
                "dataType": None,
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 1,
                "selection": None,
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            },
            {
                "parameterName": "interface_name",
                "dataType": None,
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 2,
                "selection": None,
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            },{
                "parameterName": "pcap_file",
                "dataType": None,
                "defaultValue": None,
                "description": None,
                "required": True,
                "notParam": False,
                "paramArray": False,
                "displayName": None,
                "instructionText": None,
                "group": None,
                "order": 3,
                "selection": None,
                "range": [],
                "key": None,
                "provider": None,
                "binding": ""
            }
        ],
        "version": "1"
    }
    r = requests.post(url,
                      verify=False,
                      headers=dnac_headers,
                      data=json.dumps(payload))
    return r


def commit_template(template_name, project_name):
    """DNAC Module to commit the created template"""
    tmp_url = 'https://{0}/dna/intent/api/v1/template-programmer/project'.format(dnac)

    r = requests.get(tmp_url,
                     verify=False,
                     headers=dnac_headers)
    # r.raise_for_status()

    for project in r.json():
        if project['name'] == project_name:
            for template in project['templates']:
                if template['name'] == template_name:
                    tmp_url = 'https://{0}/dna/intent/api/v1/template-programmer/template/version'.format(dnac)
                    payload = {"comments": "first commit", "templateId": template['id']}
                    r_com = requests.post(tmp_url,
                                      verify=False,
                                      headers=dnac_headers,
                                      data=json.dumps(payload))


    tmp_id_url = 'https://{0}/dna/intent/api/v1/template-programmer/template'.format(dnac)
    r_id = requests.get(tmp_id_url,
                     verify=False,
                     headers=dnac_headers)
    resp = r_id.json()
    for i in resp:
        if (i.get("name") == template_name):
            temp_id = i.get("templateId")
    return temp_id


def get_devices():
    """DNAC Module Get Devices"""
    devices_dict = {}
    tmp_url = 'https://{0}/dna/intent/api/v1/network-device'.format(dnac)

    r = requests.get(tmp_url,
                         verify=False,
                         headers=dnac_headers)
    #r.raise_for_status()
    #print('DNAC Response Body: ' + r.text)
    devices = r.json()['response']

    for dev in devices:
        if(dev.get("type")== "Cisco Catalyst 9300 Switch"):
            devices_dict.update({dev.get("id"):dev.get("hostname")})
    return devices_dict


def deploy_template(template_v_id, switch_id,cap_name,intf_name,pcap_file_name):
    """DNAC Module deploy template"""
    tmp_url = 'https://{0}/dna/intent/api/v1/template-programmer/template/deploy'.format(dnac)
    payload = {"forcePushTemplate": "True",
                  "targetInfo": [
                      {
                          "id": switch_id,
                          "params": {"capture_name": cap_name, "interface_name": intf_name, "pcap_file":pcap_file_name  },
                          "type": "MANAGED_DEVICE_UUID"
                      }
                  ],
                  "templateId": template_v_id
              }

    # payload ={ "forcePushTemplate": "True",
    #               "targetInfo": [
    #                   {
    #                       "id": switch_id,
    #                       "params": {"capture_name": cap_name, "interface_name": intf_name, "pcap_file":pcap_file_name},
    #                       "type": "MANAGED_DEVICE_UUID"
    #                   }
    #               ],
    #               "templateId": "480ac7f3-88a7-4a39-8fe4-283e32d0daef"
    #           }

    r = requests.post(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         data=json.dumps(payload))
    return r.json()


def get_deployment_status(dep_id):
    """DNAC Module Get Deployment Status"""
    tmp_url = 'https://{0}/dna/intent/api/v1/template-programmer/template/deploy/status/{1}'.format(dnac,dep_id)

    r = requests.get(tmp_url,
                     verify=False,
                     headers=dnac_headers)
    return r.json()


if __name__ == "__main__":
    get_auth_token(dnac)
    out = select_project()
    projectId_dict = {}
    print("************************************************************")
    print("Select/Create a project to assign before creating a template")
    print("************************************************************")
    out_len = out.__len__()
    print("______________________")
    print("Sl No.  Project Name")
    print("______________________")
    for z in range(out_len):
        print("{0}:   {1}".format(z, out.values()[z]))
        projectId_dict.update({z:out.keys()[z]})
    print("{0}:   {1}".format(out_len, "Create a new project\n"))
    print("----------------------")
    opt = raw_input("Select a Sl No. - ")
    if(opt == str(out_len)):
        create_project()
        print("\n************************************************************")
        print("Project Created!!! Restarting Program.......")
        print("************************************************************\n")
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        projId = projectId_dict.get(int(opt))
        projName = out.get(projId)
        print("\n************************************************************")
        print("Creating a template for project - "+projName)
        print("************************************************************\n")
        template_name = raw_input("Enter Template Name: ")
        print("____________________________________________________________\n")
        create_template(template_name, projId)
        print("Template "+template_name+" created\n")
        print("Commiting " +template_name+" started...........")
        print("____________________________________________________________\n")
        tem_id = commit_template(template_name,projName)
        #tem_id = commit_template("testmod3", "testProj")
        print("\nList of Cisco Catalyst 9300 Switch to deploy the template\n")
        dev_list = get_devices()
        for i in dev_list.values():
            print(i)
        print("____________________________________________________________\n")
        dev_name = raw_input("\nEnter the device name\n")
        for i, j in dev_list.items():
            if (dev_name == j):
                dev_id = i
        #print(dev_id)
        cap_name = raw_input("\nEnter Capture name: ")
        intf_name = raw_input("\nEnter Interface: ")
        pcap_file_name = raw_input("\nEnter Capture File name: ")
        print("\nDeploying template " +template_name+" to device "+dev_name)
        dep_response = deploy_template(tem_id,dev_id,cap_name,intf_name,pcap_file_name)
        deploy_id_raw = dep_response.get("deploymentId")
        dep_split = deploy_id_raw.split(":")
        deployment_id = dep_split[-1]
        time.sleep(15)
        deployment_statistics = get_deployment_status(deployment_id.lstrip(" "))
        deployment_devices = deployment_statistics.get("devices")
        for i in deployment_devices.__iter__():
            status_message = i.get("detailedStatusMessage")
        print("\n****************************************************************")
        print(deployment_statistics)
        print("******************************************************************")
