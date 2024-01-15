import subprocess
import time
import re
import random
 
#Function for generating IP from given base
def generateIp(baseIp, mask):
    base_octets = baseIp.split('.')
    random_octet = str(random.randint(1, 254))
    new_ip = f"{base_octets[0]}.{base_octets[1]}.{base_octets[2]}.{random_octet}/{mask}"
    return new_ip
 
#Function for checking Ip availability on the network using ping
def checkIpAvailability(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            #There is device with this IP on the network
            return True  
        else:
            #There is no device with this IP on the network
            return False  
    except Exception as e:
        print(f"checkIpAvailability: error occurred: {e}")
        return False
 
#Function for changing interface IP address using Linux ip commands
def changeIp(interface, new_ip):
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
        subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', interface], check=True)
        subprocess.run(['sudo', 'ip', 'addr', 'add', new_ip, 'dev', interface], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
        print(f"changeIp: IP address changed to {new_ip} on {interface}")
    except Exception as e:
        print(f"changeIp: error occurred: {e}")
 
#Function for counting packets incoming to interface in 1 second using linux tpdump
def countPackets(interface, packetLimit=100):
    try:
        #Count incoming packets for one second
        command = f"sudo timeout 1 tcpdump -i {interface}"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = process.stderr
        #Count tcpdump records
        packetCount = re.search(r"(\d+) packets received by filter", output)
        if(packetCount): 
            return int(packetCount.group(1))
        else:
            return 0
    except Exception as e:
        print(f"countPackets: error occured: {e}")
        return None
 
#Main loop - change Ip addres every given period (changeIpPeriod) or when too many packets are coming to the interface
def main(interface, baseIp, mask, changeIpPeriod, threshold):
    while True:
        start_time = time.time()
 
        #Regular Ip change to make reconnaissance harder
        new_ip = generateIp(baseIp, mask)
        if not checkIpAvailability(new_ip.split('/')[0]):
            print("main: perform routine IP change")
            changeIp(interface, new_ip)
        else:
            print("main: IP address generation conflict during periodic change")
 
        #Monitor incoming packets amount
        while time.time() - start_time < changeIpPeriod:
            packetCount = countPackets(interface)
            print(f"main: monitoring incoming traffic, packet count = {packetCount}")
            if packetCount > threshold:
                #Change IP if amount exceeds treshold
                print(f"main: packet amount ({packetCount}) exceeding trehsold ({threshold}), changing IP")
                new_ip = generateIp(baseIp, mask)
                if not checkIpAvailability(new_ip.split('/')[0]):
                    changeIp(interface, new_ip)
                else:
                    print("main: IP address generation conflict after threshold exceeded")
            time.sleep(1)
 
################ Parameters ############################
interface = 'enp0s3'        #Interface to apply MTD 
baseIp = '10.0.2'           #Base for generating new IP
mask = '24'                 #Mask
changeIpPeriod = 20         #IP changing period
threshold = 100             #Threshold for incoming packets
########################################################
 
main(interface, baseIp, mask, changeIpPeriod, threshold)
