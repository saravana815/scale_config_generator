
# scale config generator

Python2 based scale config generator for generating scale configs using a template file for cisco and cisco like devices.

This script currently supports
* Incrementing Numbers
* Incrementing IP address
* Incrementing IPv6 address for whole two quads such as [0000:0000] to [FFFF:FFFF]


### Example usage 1

Template file name - config.txt
Default output config file - config_out.txt

```
[sargandh:SARGANDH-3QLQC]$ cat config.txt

interface GigabitEthernet0/0/3.[2000]     # Number increment
 encapsulation dot1Q [2000]
 ip address 20.0.[0.2] 255.255.255.252    # IP address increment
 ipv6 address 2001:[11AA:22BB]::2/64      # IPv6 address increment

[sargandh:bgl-ads-1214]$ ./scale_config.py
usage: scale_config.py [-h] -f FILE -c COUNT # -c number of iterations to run

[sargandh:SARGANDH-3QLQC]$ python scale_config_new.py -f config.txt -c 2
 interface GigabitEthernet0/0/3.2000
  encapsulation dot1Q 2000
  ip address 20.0.0.2 255.255.255.252
  ipv6 address 2001:11AA:22BB::2/64

 interface GigabitEthernet0/0/3.2001
  encapsulation dot1Q 2001
  ip address 20.0.0.3 255.255.255.252
  ipv6 address 2001:11AA:22BC::2/64

[sargandh:SARGANDH-3QLQC]$
[sargandh:SARGANDH-3QLQC]$ ls -lh config_out.txt
-rwxrwxrwx 1 sargandh sargandh  282 Dec 21 21:51 config_out.txt
[sargandh:SARGANDH-3QLQC]$

```

### Example usage 2

Template file name - config2.txt

Increment number by value more than 1 from a starting number to end number
Increment IP address, IPv6 address by value more than one

```
[sargandh:SARGANDH-3QLQC]$ cat config2.txt

interface GigabitEthernet0/0/3.[2000,2,2002]    # Increment number from 2000 to 2002 by 2 for every iteration
 encapsulation dot1Q [2000,2,2002]
 ip address 20.0.[0.2,4] 255.255.255.252        # Increment IP address by 4 for every iteration
 ipv6 address 2001:[11AA:22BB,4]::2/64          # Increment IPv6 address by 4 for every iteration

[sargandh:SARGANDH-3QLQC]$ python scale_config.py -f config2.txt -c 4
interface GigabitEthernet0/0/3.2000
 encapsulation dot1Q 2000
 ip address 20.0.0.2 255.255.255.252
 ipv6 address 2001:11AA:22BB::2/64

interface GigabitEthernet0/0/3.2002
 encapsulation dot1Q 2002
 ip address 20.0.0.6 255.255.255.252
 ipv6 address 2001:11AA:22BF::2/64

interface GigabitEthernet0/0/3.2000
 encapsulation dot1Q 2000
 ip address 20.0.0.10 255.255.255.252
 ipv6 address 2001:11AA:22C3::2/64

interface GigabitEthernet0/0/3.2002
 encapsulation dot1Q 2002
 ip address 20.0.0.14 255.255.255.252
 ipv6 address 2001:11AA:22C7::2/64

[sargandh:SARGANDH-3QLQC]$
```
