
# scale config generator

Python based scale config generator for generating big scale configs using a template file.

The script currently supports 

* Incrementing Numbers
* Incrementing IP address 
	* Only two dotted decimal fields of IP address can be incremented 
* Incrementing IPv6 address
	* Only single 2 byte word from IPv6 address can be incremented 


Example usage 1

Template file name - config.txt 

```
[sargandh:bgl-ads-1214]$ cat config.txt 

interface GigabitEthernet0/0/3.[2000]
 encapsulation dot1Q [2000] # Number increment
 ip address 20.0.[0.2] 255.255.255.252 # IP address increment
 ipv6 address 2001:[0x10]::2/64 # IPv6 address increment. IPv6 two byte word has to begin with 0x
 
[sargandh:bgl-ads-1214]$ ./scale_config.py 
usage: scale_config.py [-h] -f FILE -c COUNT # -c number of iterations to run

[sargandh:bgl-ads-1214]$ ./scale_config.py -f config.txt -c 2 

interface GigabitEthernet0/0/3.2000
 encapsulation dot1Q 2000
 ip address 20.0.0.2 255.255.255.252
 ipv6 address 2001:10::2/64
 

interface GigabitEthernet0/0/3.2001
 encapsulation dot1Q 2001
 ip address 20.0.0.3 255.255.255.252
 ipv6 address 2001:11::2/64
 
[sargandh:bgl-ads-1214]$ 
```

Example usage 2

Increment number by value more than 1 from a starting number to end number

Increment IP address, IPv6 address by value more than one
```
[sargandh:bgl-ads-1214]$ cat config.txt 

interface GigabitEthernet0/0/3.[2000,2,2002] # Increment number from 2000 to 2002 by 2 for every iteration
 encapsulation dot1Q [2000,2,2002]
 ip address 20.0.[0.2,4] 255.255.255.252 # Increment IP address by 4 for every iteration 
 ipv6 address 2001:[0x10,4]::2/64 # Increment IPv6 address by 4 for every iteration 



[sargandh:bgl-ads-1214]$ ./scale_config.py -f config.txt -c 4

interface GigabitEthernet0/0/3.2000
 encapsulation dot1Q 2000
 ip address 20.0.0.2 255.255.255.252
 ipv6 address 2001:10::2/64

interface GigabitEthernet0/0/3.2002
 encapsulation dot1Q 2002
 ip address 20.0.0.6 255.255.255.252
 ipv6 address 2001:14::2/64

interface GigabitEthernet0/0/3.2000
 encapsulation dot1Q 2000
 ip address 20.0.0.10 255.255.255.252
 ipv6 address 2001:18::2/64

interface GigabitEthernet0/0/3.2002
 encapsulation dot1Q 2002
 ip address 20.0.0.14 255.255.255.252
 ipv6 address 2001:1c::2/64
/ws/sargandh-bgl/gitlab/scale_config_generator
[sargandh:bgl-ads-1214]$ 
```
