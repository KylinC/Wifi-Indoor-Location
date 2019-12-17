# Wifi-Indoor-Location

> SJTU CS339, Computer Networks, 2019fall 

https://kylinchen.top/Wifi-Indoor-Location/

[![](https://img.shields.io/badge/python-3.5.7-blue.svg)]()

[![](https://img.shields.io/badge/Torch-1.0-orange)]()

[![](https://img.shields.io/badge/flask-1.1.1-brightgreen)]()

[![](https://img.shields.io/badge/pyobjc-6.1-red)]()

<br/>

Refers to RSSI fingerprinting and RNN, we've coded a demo to achieve indoor location in our last-summer-merely-destroyed dormetory D19. We also build a 3D front-end to visualize the location result.


### Dependency

- Ubuntu/Windows:

```bash
cd Wifi-Indoor-Location

pip install packages/requirements_win_ubuntu.txt
```

- Mac OS:

```bash
cd Wifi-Indoor-Location

pip install packages/requirements_macos.txt
```

```bash
cd Wifi-Indoor-Location/packages/pywifi_macos

pip install .
```

**Tips:** Firefox web-browser is recommanded for the demo!


### Launch

- Run **app.py**

```bash
cd Wifi-Indoor-Location/src

python run.py
```

- View [http://localhost:5000/](http://localhost:5000/) on **Firefox**

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-12-17-msmsm.jpg)



### References:

PyWifi: https://github.com/awkman/pywifi

Mac OS CWInterface: https://developer.apple.com/documentation/corewlan/cwinterface
