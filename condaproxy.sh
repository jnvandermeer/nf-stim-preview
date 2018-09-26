# conda uses the https proxy.

# id:pw can be your QIMR id and PW
# address is webproxy.qimr.edu.au or webproxy.adqimr.ad.lan, it doesn't matter -- the IP is 10.10.2.71 for both
# port is 8080

conda config --set proxy_servers.http http://id:pw@address:port
conda config --set proxy_servers.https https://id:pw@address:port
