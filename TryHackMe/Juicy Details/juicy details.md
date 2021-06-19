![](juicy%20details.png)

What we can learn from this machine?
* How to read and understand the firefox log files
* About sql injection

##  Reconnaissance 
1. What tools did the attacker use? (Order by the occurrence in the log)
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:08:34 +0000] "POST / HTTP/1.1" 200 1924 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)"

::ffff:192.168.10.5 - - [11/Apr/2021:09:16:29 +0000] "POST /rest/user/login HTTP/1.0" 401 26 "-" "Mozilla/5.0 (Hydra)"

::ffff:192.168.10.5 - - [11/Apr/2021:09:29:14 +0000] "GET /rest/products/search?q=1 HTTP/1.1" 200 - "-" "sqlmap/1.5.2#stable (http://sqlmap.org)"

::ffff:192.168.10.5 - - [11/Apr/2021:09:32:51 +0000] "GET /rest/products/search?q=qwert%27))%20UNION%20SELECT%20id,%20email,%20password,%20%274%27,%20%275%27,%20%276%27,%20%277%27,%20%278%27,%20%279%27%20FROM%20Users-- HTTP/1.1" 200 3742 "-" "curl/7.74.0"

::ffff:192.168.10.5 - - [11/Apr/2021:09:34:33 +0000] "GET /a54372a1404141fe8842ae5c029a00e3 HTTP/1.1" 200 1924 "-" "feroxbuster/2.2.1"
```
Answer : nmap,hydra,sqlmap,curl,feroxbuster

2. What endpoint was vulnerable to a brute-force attack?
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:16:31 +0000] "GET /rest/user/login HTTP/1.0" 500 - "-" "Mozilla/5.0 (Hydra)"
```
Answer : /rest/user/login

3. What endpoint was vulnerable to SQL injection?
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:29:14 +0000] "GET /rest/products/search?q=1 HTTP/1.1" 200 - "-" "sqlmap/1.5.2#stable (http://sqlmap.org)"
```
Answer : /rest/products/search

4. What parameter was used for the SQL injection?

Link to documentation : https://www.geeksforgeeks.org/use-sqlmap-test-website-sql-injection-vulnerability/

Answer : q

5. What endpoint did the attacker try to use to retrieve files? (Include the /)
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:34:40 +0000] "GET /ftp/www-data.bak HTTP/1.1" 403 300 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
```
Answer : /ftp

##  Stolen data 
1. What section of the website did the attacker use to scrape user email addresses?
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:10:19 +0000] "GET /rest/products/41/reviews HTTP/1.1" 200 284 "http://192.168.10.4/" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
```
Answer : products reviews

2. Was their brute-force attack successful? If so, what is the timestamp of the successful login? (Yay/Nay, 11/Apr/2021:09:xx:xx +0000)
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:16:31 +0000] "POST /rest/user/login HTTP/1.0" 200 831 "-" "Mozilla/5.0 (Hydra)"
```
Answer : yay, 11/Apr/2021:09:16:31 +0000

3. What user information was the attacker able to retrieve from the endpoint vulnerable to SQL injection?
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:31:04 +0000] "GET /rest/products/search?q=qwert%27))%20UNION%20SELECT%20id,%20email,%20password,%20%274%27,%20%275%27,%20%276%27,%20%277%27,%20%278%27,%20%279%27%20FROM%20Users-- HTTP/1.1" 200 - "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
```

Answer : email,password

4. What files did they try to download from the vulnerable endpoint? (endpoint from the previous task, question #5)
```js
::ffff:192.168.10.5 - - [11/Apr/2021:09:34:40 +0000] "GET /ftp/www-data.bak HTTP/1.1" 403 300 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
::ffff:192.168.10.5 - - [11/Apr/2021:09:34:43 +0000] "GET /ftp/coupons_2013.md.bak HTTP/1.1" 403 78965 "-" ""Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
```
Answer : www-data.bak,coupons_2013.md.bak

5. What service and account name were used to retrieve files from the previous question? (service, username)
```js
Sun Apr 11 08:29:34 2021 [pid 6846] [ftp] OK LOGIN: Client "::ffff:192.168.10.5", anon password "IEUser@"
```
Answer : ftp, anonymous

6. What service and username were used to gain shell access to the server? (service, username)
```js
Apr 11 09:41:32 thunt sshd[8494]: Accepted password for www-data from 192.168.10.5 port 40114 ssh2
```
Answer : ssh,www-data