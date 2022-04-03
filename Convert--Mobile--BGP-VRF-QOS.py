import paramiko
import time
from termcolor import colored
from timeit import default_timer as timer
import sys

global password
username = "ldap"
password = "pwd"

def vrf_implement_control(device_ip):
    producttype =""
    host_ci =""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    file = open("logs/"+"results.log", "a")

    try:
        remote_connection = ssh.connect(device_ip, port="22", username=username, password=password, timeout=15)
        remote_connection = ssh.invoke_shell()
        print (colored ("connected_ip_address_"+ device_ip,"blue"))

        ############################device_type_check##################################
        remote_connection.send(" display  current-configuration   | include  sysname"+"\n")
        time.sleep(3)
        output25 = remote_connection.recv(65535)
        result25 = output25.decode('ascii').strip("\n")
        output_list_ciname = result25.splitlines()

        for j in (output_list_ciname):
            if ("sysname" in j and "include" not in j):
                words = j.split()
                host_ci = words[1]
                print("host_cı="+host_ci)

        if ("nw_ra_a98c" in host_ci):
            producttype = "APE"

        elif (("TH95"  in host_ci)  or ( "TH91" in host_ci) or ( "TH9C" in host_ci) ):
            producttype = "ATN"

        print(producttype)

        vrf_default_route = "NOK"
        vrf_implement = "NOK"
        dummy_vrf_for_ape ="NOK"
        bgp_vrf="NOK"
        export_policy ="NOK"
        general_config_control ="NOK"

        ################################Default_Route_Check#######################################
        if producttype == "APE" :

            remote_connection.send("dis ip rou vpn DATA-VRF | inc 192.168.10.2/29 \n") ## new VRF entered
            time.sleep(4)
            output = remote_connection.recv(65535)
            result = output.decode('ascii').strip("\n")
            output_list_fnk = result.splitlines()
            print(result)

            for line_fnk in output_list_fnk:
                if ("10.186.176.8/29" in line_fnk and "RD" in line_fnk) :
                    vrf_default_route = "OK"

        ################################Vrf_İmplement_Check#######################################

            remote_connection.send("display current config vpn-instance DATA-VRF\n")  ## new VRF entered
            time.sleep(4)
            output2 = remote_connection.recv(65535)
            result2 = output2.decode('ascii').strip("\n")
            output_list_fnk_2 = result2.splitlines()
            print(result2)
            print(len(output_list_fnk_2))
            if len(output_list_fnk_2) == 15 :
                vrf_implement = "OK"

        ################################Dummy_Vrf_Check#######################################

            remote_connection.send("display current config vpn-instance dummy-vpn-for-inline-rr\n")  ## new VRF entered
            time.sleep(4)
            output3 = remote_connection.recv(65535)
            result3 = output3.decode('ascii').strip("\n")
            output_list_fnk_3 = result3.splitlines()
            print(result3)

            for line_fnk3 in output_list_fnk_3:

                if ("vpn-target 34984:3896 import-extcommunity" in line_fnk3 ):
                    dummy_vrf_for_ape = "OK"


        ################################Bgp_Vrf_Check#######################################

            remote_connection.send("dis curr  |    include  DATA-VRF \n")  ## new VRF entered
            time.sleep(4)
            output4 = remote_connection.recv(65535)
            result4 = output4.decode('ascii').strip("\n")
            output_list_fnk_4 = result4.splitlines()
            print(result4)

            for line_fnk in output_list_fnk_4:
                if (" ipv4-family" in line_fnk ):
                    bgp_vrf = "OK"

        ################################Export_Policy_Check#######################################

            remote_connection.send("display  current config route-policy deny-default-and-permit-all\n")  ## new VRF entered
            time.sleep(4)
            output5 = remote_connection.recv(65535)
            result5 = output5.decode('ascii').strip("\n")
            output_list_fnk_5 = result5.splitlines()
            print(result5)
            print(len(output_list_fnk_5))
            if len(output_list_fnk_5) == 9:
                export_policy = "OK"

        elif  producttype == "ATN" :

            remote_connection.send("dis ip rou vpn DATA-VRF | inc 10.186.176.8/29 \n") ## new VRF entered
            time.sleep(4)
            output = remote_connection.recv(65535)
            result = output.decode('ascii').strip("\n")
            output_list_fnk = result.splitlines()
            print(result)

            for line_fnk in output_list_fnk:
                if ("10.186.176.8/29" in line_fnk and "RD" in line_fnk) :
                    vrf_default_route = "OK"

        ################################Vrf_İmplement_Check#######################################
            remote_connection.send("display current config vpn-instance DATA-VRF\n")  ## new VRF entered
            time.sleep(4)
            output2 = remote_connection.recv(65535)
            result2 = output2.decode('ascii').strip("\n")
            output_list_fnk_2 = result2.splitlines()

            if ('  tnl-policy seamless' in output_list_fnk_2)  and  ( '  export route-policy deny-default-and-permit-all'  in output_list_fnk_2) and ('  vpn-target 34984:3896 export-extcommunity'  in output_list_fnk_2) :
                vrf_implement = "OK"

        ################################Bgp_Vrf_Check#######################################

            remote_connection.send(  "dis curr | include  DATA-VRF \n")  ## new VRF entered
            time.sleep(4)
            output4 = remote_connection.recv(65535)
            result4 = output4.decode('ascii').strip("\n")
            output_list_fnk_4 = result4.splitlines()
            print(result4)

            for line_fnk in output_list_fnk_4:
                if (" ipv4-family" in line_fnk ):
                    bgp_vrf = "OK"

        ################################Route_Policy_Check#######################################

            remote_connection.send("display  current config route-policy deny-default-and-permit-all\n")  ## new VRF entered
            time.sleep(4)
            output5 = remote_connection.recv(65535)
            result5 = output5.decode('ascii').strip("\n")
            output_list_fnk_5 = result5.splitlines()
            print(result5)
            print(len(output_list_fnk_5))
            if len(output_list_fnk_5) > 8 :
                export_policy = "OK"

        elif producttype == "":

            print("There is issue in Ne Type !!!")

        if producttype == "APE":

            print("VRF_Default_route_Status = "+vrf_default_route)
            print("VRF_implement_Status = "+vrf_implement)
            print("Dummy_Vrf_Config = "+dummy_vrf_for_ape)
            print("BGP_Vrf_Config = "+bgp_vrf)
            print("VRF_export_policy = "+export_policy)
            if (dummy_vrf_for_ape == "OK" ) and (bgp_vrf == "OK" ) and( vrf_default_route == "OK") and (vrf_implement =="OK") and (export_policy =="OK"):
                general_config_control = "OK"

        elif producttype == "ATN":

            print("VRF_Default_route_Status = "+vrf_default_route)
            print("VRF_implement_Status = "+vrf_implement)
            print("BGP_Vrf_Config = "+bgp_vrf)
            print("VRF_export_policy = "+export_policy)
            if  (bgp_vrf == "OK" ) and( vrf_default_route == "OK") and (vrf_implement =="OK") and (export_policy =="OK"):
                general_config_control = "OK"

        print(general_config_control)
        return general_config_control
        ssh.close()

    except Exception as e:
        print(device_ip +"\n"+ "no connection_to_device " + str(e), end=" ")
        print("\n")
        print(colored("Ipmlementation Failed, for "+device_ip+" Control SSH parameters or Do ip Manually !!","red"))
        time.sleep(2)
        with open("unreachables.txt", "a") as f:
            f.write(device_ip + "\n")
        f.close()

while True :
    user_input = str(input("\n\n2G3G_ORTAK_VRF_IMPLEMENTATION_SCRIPT\n\n""type_1_for_2G3G_ORTAK_VRF__Implementation\ntype_2_for_quit\n"))
    if user_input == "1":
        f1 = open('hostfile.txt', 'r')

        devices = f1.readlines()
        device_number=0
        for device in devices:
            device_number = device_number + 1
            print("Control Started for device number : " + str(device_number))
            column = device.split()
            host = str(column[0])
            t1_start = timer()
            if  vrf_implement_control(host) == "OK" :
                f2 = open("implement_control_ok.txt", 'a')
                f2.write(host+"\n")
                f2.close()
            else:
                f3 = open("implement_control_nok.txt", 'a')
                f3.write(host+"\n")
                f3.close()
            t1_stop = timer()
            print("Elapsed time during the whole program in seconds:",
                  int(t1_stop) - int(t1_start))
            time.sleep(4)
        f1.close()

    elif user_input == "2" :
        print ("Logout....")

        break
