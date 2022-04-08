# Task 1
What does the acronym VM stand for? Virtual machine

#  Task 2
What tool do we use to interact with the operating system in order to start our VPN connection? Terminal

#  Task 3
What service do we use to form our VPN connection? Openvpn

#  Task 4
What is the abreviated name for a tunnel interface in the output of your VPN boot-up sequence output? Tun

#  Task 5
What tool do we use to test our connection to the target? Ping

#  Task 6
What is the name of the tool we use to scan the target's ports? Nmap

#  Task 7
What service do we identify on port 23/tcp during our scans? Telenet

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 0]
└─$ nmap -sC -sV 10.129.244.123 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-08 00:32 PDT
Nmap scan report for 10.129.244.123
Host is up (0.18s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
23/tcp open  telnet  Linux telnetd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 39.40 seconds
```
# Task 8
What username ultimately works with the remote management login prompt for the target? root

#  Submit Flag

Submit root flag 
```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 1]
└─$ telnet 10.129.244.123                                                                                                                                                                 1 ⨯
Trying 10.129.244.123...
Connected to 10.129.244.123.
Escape character is '^]'.

  █  █         ▐▌     ▄█▄ █          ▄▄▄▄
  █▄▄█ ▀▀█ █▀▀ ▐▌▄▀    █  █▀█ █▀█    █▌▄█ ▄▀▀▄ ▀▄▀
  █  █ █▄█ █▄▄ ▐█▀▄    █  █ █ █▄▄    █▌▄█ ▀▄▄▀ █▀█


Meow login: root
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-77-generic x86_64)

Last login: Fri Apr  8 07:39:36 UTC 2022 on pts/0
root@Meow:~# ls
flag.txt  snap
root@Meow:~# cat flag.txt
b40abdfe23665f766f9c61ecba8a4c19
```
