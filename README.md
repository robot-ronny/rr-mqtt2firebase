# rr-mqtt2firebase
Bridge between mqtt messages and Google Realtime Firebase

## Install
```
sudo pip3 install -e .
```

## Use
First install and run [bcg tool](https://github.com/bigclownlabs/bch-gateway)


```
mqtt2firebase -f https://your-firebase.firebaseio.com/
```

You can specify many things with arguments
```
>>> mqtt2firebase --help
Usage: mqtt2firebase [OPTIONS]

Options:
  -f, --firebase TEXT  Firebase url  [required]
  -h, --host TEXT      MQTT broker host
  -p, --port INTEGER   MQTT broker port
  -d, --delay INTEGER  Delay between reporting data to firebase
  --help               Show this message and exit.
```