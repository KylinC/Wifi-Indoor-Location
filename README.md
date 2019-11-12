# **Wifi-Indoor-Location**

> SJTU-CS339 Project, Use WiFi RSSI to locate mobile devices indoors.

<img src='https://img.shields.io/badge/python-3.5.7-blue.svg'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/flask-1.1.1-brightgreen'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/pyobjc-6.1-red'  align='left' style=' width:100px'/></br>



### Environment:

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



### Launch:

- Run **app.py**

```bash
cd Wifi-Indoor-Location/source

python app.py
```

- View [http://localhost:5000/](http://localhost:5000/) on Chrome

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-11-12-%E6%88%AA%E5%B1%8F2019-11-12%E4%B8%8B%E5%8D%8810.37.38.png)



### References:

PyWifi: https://github.com/awkman/pywifi

Mac OS CWInterface: https://developer.apple.com/documentation/corewlan/cwinterface