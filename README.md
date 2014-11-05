multi-socks
===========

SOCKSv4 proxy for servers with multiple IPs

Cloud providers have a feature to assign multiple IPs to a single server. That is a cheap and 
safe way to create proxies for your data scraping tasks to avoid IP bans.
I couldn't find and easy way to set up a SOCKS proxy to use all IPs so I made my own.

So the first step is to buy multiple IPs from your cloud provider and set up Linux networking using
those IPs (http://askubuntu.com/questions/313877/how-do-i-add-an-additional-ip-address-to-etc-network-interfaces)

You have to install Python Twisted framework and then install multi-socks:

    sudo python setup.py

Now you can run it:

    twistd multi-socks -a 192.168.1.101:1080,192.168.1.102:1080,192.168.1.103:1080,192.168.1.104:1080 -w whitelist.txt

This will create proxies on:

- 192.168.1.101:1080 that will connect to destination from IP 192.168.1.101
- 192.168.1.102:1080 that will connect to destination from IP 192.168.1.102
- 192.168.1.103:1080 that will connect to destination from IP 192.168.1.103
- 192.168.1.104:1080 that will connect to destination from IP 192.168.1.104

Since Twisted has support only for SOCKSv4, you should use a whitelist file (one IP per line) for proxy to accept connections only from listed IPs. You can update this file while proxy is running and it will pick up all changes.
Otherwise sooner or later proxy scanners will find your proxy and use it for evil things.

You can test that your proxies work by using curl command:

    curl --socks4 192.168.1.101:1080 -s whatsmyip.net | grep 'class="ip"' 

will show  192.168.1.101 as your ip

    curl --socks4 192.168.1.102:1080 -s whatsmyip.net | grep 'class="ip"' 

will show  192.168.1.102 as your ip

    curl --socks4 192.168.1.103:1080 -s whatsmyip.net | grep 'class="ip"' 

will show  192.168.1.103 as your ip

    curl --socks4 192.168.1.104:1080 -s whatsmyip.net | grep 'class="ip"' 

will show  192.168.1.104 as your ip
