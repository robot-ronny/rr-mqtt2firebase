# rr-mqtt2firebase
Bridge between mqtt messages and Google Realtime Firebase

## Install

```
sudo pip3 install -r requirements.txt
```

## Use

Edit config file to specific mqtt broker and firebase realtime database url. Then run script.

config.yaml file example

```
connection:
  host: 127.0.0.1
  port: 1883

firebase:
  url: https://yourdatabase.firebaseio.com/
```

Run
```
python3 run.py
```