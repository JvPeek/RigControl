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
#usage: cli.py [-h] --port {/dev/cu.Bluetooth-Incoming-Port,/dev/cu.usbmodem1201,/dev/cu.wlan-debug} {adapter,run} ...
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