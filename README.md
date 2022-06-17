# RigControl - Python Edition

## Usage

### main
For testing and programming adapters use the `main.py`
### cli
The `cli.py` should be used as the primary entrypoint for RigControl in production (or when bundled as `.exe`).
Currently there is no way to define configurations, but all adapters are using the `localhost`. 

#### Examples
The CLI shows all possibly values for a parameter:
```bash
python3 cli.py
# usage: cli.py [-h] --port {/dev/cu.Bluetooth-Incoming-Port,/dev/cu.usbmodem1201,/dev/cu.wlan-debug} {adapter,run} ...
```

```bash
python3 cli.py --port /dev/cu.usbmodem1201 run 
# usage: cli.py run [-h] -a {monkey,trackmania,warthunder}
```

Run the **SpaceMonkey** adapter for DCS on serial port `/dev/cu.usbmodem1201`: 
```bash
python3 cli.py --port /dev/cu.usbmodem1201 run -a monkey
```


## Adapters

### WarThunder (`WTAdapter`)

### SpaceMonkey (`monkeyAdapter`)

### Test (`TestAdapter`)

## `WIP` Configuration
***!!!NOTHING IS IMPLEMENTED!!!*** This is only to show a possible configuration pattern
### Default
```yaml
filters:
  ramp:
    type: sigmoid
    parameters:
    c1: 1.5
    c2: 1
  map:
    type: linear
    parameters:
      fromMin: -90
      fromMax: 90
      toMin: -22
      toMax: 22
adapters: 
  monkey:
    parameters:
      ip: '0.0.0.0'
      port: 12001
    filters: ['ramp', 'map']
  warthunder:
    parameters:
      ip: '0.0.0.0'
      port: 8111
    filters: ['ramp', 'map']
```

### Override Configuration
To override a configuration start the `cli.py` with the `--configuration` parameter and pass the path to the configuration file as value.

*configuration.yaml*
```yaml
adapters: 
  monkey:
    filters: 
      ramp:
      map: 
        parameters:
          toMin: -12
          toMax: 12
  warthunder:
    parameters:
      ip: '192.168.178.25'
```