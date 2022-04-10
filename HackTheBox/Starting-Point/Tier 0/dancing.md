## Task 1

What does the 3-letter acronym SMB stand for? server message block

## Task 2

What port does SMB use to operate at? 445

## Task 3

What network communication model does SMB use, architecturally speaking? client-server model 

## Task 4

What is the service name for port 445 that came up in our nmap scan? microsoft-ds
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

What is the tool we use to connect to SMB shares from our Linux distribution? smbclient

## Task 6

What is the `flag` or `switch` we can use with the SMB tool to `list` the contents of the share? -L

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

What is the name of the share we are able to access in the end? workshares

## Task 8

What is the command we can use within the SMB shell to download the files we find? get

```bash
┌──(defalt@kali)-[~/Documents/htb/starting point /Tier 0]
└─$ smbclient \\\\10.129.1.12\\WorkShares                                                                                                                                                 1 ⨯
Enter WORKGROUP\defalt's password: 
Try "help" to get a list of possible commands.
smb: \> help
?              allinfo        altname        archive        backup         
blocksize      cancel         case_sensitive cd             chmod          
chown          close          del            deltree        dir            
du             echo           exit           get            getfacl        
geteas         hardlink       help           history        iosize         
lcd            link           lock           lowercase      ls             
l              mask           md             mget           mkdir          
more           mput           newer          notify         open           
posix          posix_encrypt  posix_open     posix_mkdir    posix_rmdir    
posix_unlink   posix_whoami   print          prompt         put            
pwd            q              queue          quit           readlink       
rd             recurse        reget          rename         reput          
rm             rmdir          showacls       setea          setmode        
scopy          stat           symlink        tar            tarmode        
timeout        translate      unlock         volume         vuid           
wdel           logon          listconnect    showconnect    tcon           
tdis           tid            utimes         logoff         ..             
!              
smb: \> help get
HELP get:
    <remote name> [local name] get a file
```

 
## Submit Flag

Submit root flag

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


