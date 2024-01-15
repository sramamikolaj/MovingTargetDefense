
## Moving Target Defense for Linux device

Moving Target Defense (MTD) is a cybersecurity concept, which main goal is to dynamically change system configuration and, as a result, change attack surface for potential intruder. System reconfiguration makes pre-attack reconnaissance more difficult and less effective. MTD can also involve dynamic change of system parameters in case that a potential attack is detected.

One of MTD strategies is to periodically change IP address of device, to make IP mapping process harder and to stop some attacks that are aimed at a device with specified IP. 

### About project
Project is an implementation of MTD for Linux device with static IP configurations. Python script periodically changes IP of specified interface, but also monitors incoming traffic and performs reconfiguration if unusually high traffic is detected. 

_This project's main goal is to demonstrate the idea of MTD. It's usage in real scenarios can make effective network communication impossible. Real MTD usages require more advanced software and possibly external security devices_  

### Usage

Script configuration is placed at the bottom of the file: 

- interface - device interface name to which MTD strategy should be applied
- baseIp - base for new IP generation           
- mask - subnet mask 
- changeIpPeriod - regular IP change period (seconds)
- threshold - amount of incoming packets per second above which dynamic reconfiguration should be applied immediately

Below is an usage example. Script performed reconfiguration every 10 seconds on virtual interface _enp0s3_. At some point high amount of traffic destined for interface's IP addres was generated to demonstrate unusual traffic situation.
![image](https://github.com/sramamikolaj/MovingTargetDefense/assets/31731062/ec58f5ae-154c-45a7-821e-6b1086415757)

### Authors
Mikolaj Srama \
Pawel Biniak

