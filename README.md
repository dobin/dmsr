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


## Install

We install it as a dedicated user:

```
$ sudo adduser --disabled-password dmsr
$ cd /home/dmsr/
$ git clone https://github.com/dobin/dmsr
$ cd dmsr/
$ pip3 install -r requirements.txt
$ cp agent.yaml.sample agent.yaml
$ cp server.yaml.sample server.yaml
```

For persistence, use appropriate systemd file  (for `/etc/systemd/system`): 
* dmsragent.service
* dmsrserver.service


## How to Use

Server: 
* configure password in `server.yaml`
* start server: `./server.py`

Agent: 
* configure password and plugins in `agent.yaml`
* start agent: `./agent.py`


## Design Decisions

There is no state. Stuff is either down, or it aint.

There is no server side configuration.

Stuff is configured on the agents: 
* What data will be pushed
* How the data will look like
Because the content of the agent is the server, and in that context you
know what you want to monitor.