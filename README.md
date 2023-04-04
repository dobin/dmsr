# DMSR - Does My Shit Run

A minimalistic monitoring solution to see if my shit still works.

* Agent based
* No history
* No DB
* Python plugins


## How it works

* Agent has plugins
* Agent plugins will generate a JSON and send it to the server
* Server stores JSON, overwriting previous
* Server will pretty print JSON (from all servers, all plugins)

Thats it.


## How to 

1) deploy the server. Set a password in server.yaml
2) deploy agents: 
  * set password and server URL in config.yaml
  * enable some plugins in config.yaml
  * configure the plugins in `plugins/<plugin>.yaml`


## install

We install it as a dedicated user:

```
$ sudo adduser --disabled-password dmsr
$ cd /home/dmsr
$ git clone https://github.com/dobin/dmsr
```

Use appropriate systemd file for `/etc/systemd/system`: 
* dmsragent.service
* dmsrserver.service

### WTF does that mean?

There is no state. Its either down, or it aint. 

What data is pushed is configured on the agents. 
How the data will look like is configured on the agents. 
Because thats where you decide what you want to monitor. 


### Why?

Too many projects. Too many VM's. Too many containers. 

