# DMSR - Does My Shit Run

A minimalistic monitoring solution to see if my shit still works.
See [mon.yookiterm.ch](https://mon.yookiterm.ch) for how I use it.

* Agent based
* HTTP communication from agent to server
* Simple python plugins
* No history
* No DB, No time series DB
* No query language
* No need to run as root
* No filtering, aggregation, transformation or processing


## How it works

* Agent has plugins
* Agent plugins will generate a JSON and send it to the server with HTTP POST
* Server stores JSON, overwriting previous
* Server will pretty print JSON (from all servers, all plugins)

Thats it.


## Screenshot

![Screenshot](https://raw.githubusercontent.com/dobin/dmsr/main/doc/doesmyshitrun.png)


## Install

We install it as a dedicated user:

```
$ sudo adduser --disabled-password dmsr
$ cd /home/dmsr/
$ su dmsr
$ git clone https://github.com/dobin/dmsr
$ cd dmsr/
$ pip3 install -r requirements.txt
$ cp agent.yaml.sample agent.yaml    # for agent
$ cp server.yaml.sample server.yaml  # for server
$ ./server.py &
$ ./agent.py
```

For persistence, use appropriate systemd file  (for `/etc/systemd/system`): 
* dmsragent.service
* dmsrserver.service


## How to Use

Server: 
* configure `password` in `server.yaml`
* start server: `./server.py`

Agent: 
* configure `password` and plugins in `agent.yaml`
* start agent: `./agent.py`


## Sample `agent.yaml`

Refreshes are always in seconds.

`agent.yaml.sample`:
```
server: http://localhost:5000
password: password
refresh: 60

plugins:
  http:
    enabled: true
    urls: 
    - http://localhost:5000
    refresh: 120

  process:
    enabled: true
    processes:
    - init
    - asdf

  sysinfo:
    enabled: true
    disks:
    - /
    show load: true
    show memory: true

  systemdunit:
    enabled: false
    private: true
    units:
    - ssh
```

## Sample `server.yaml`

`server.yaml.sample`:
```yaml
password: password
adminpw: password
pagerefresh: 60
```


## Admin

Configure `adminpw` in `server.yaml`. 

Login with `/admin`. 

To make a plugin data private, set `private = true` in `agent.yaml`.


## Alarming

Plugins may return non empty `status`, most often with the string `warn`. They decide by themselves when to send it.

The endpoint `/status` will return HTTP `200` if all status
are ok, and `500` if at least one is not ok.

Use [Desktop Web Scheduler (DWS)](https://github.com/ozzi-/DWS) to get a notification if some shit doesnt run anymore.


## Design Decisions

There is no history. Stuff is either down currently, or it aint.

There is no persistence. Dont care about the status 5 minute ago.

There is no server side configuration.
* Agent decides what data will be pushed
* Agent decides how the data will look like
* Agent decides what the error conditions are
