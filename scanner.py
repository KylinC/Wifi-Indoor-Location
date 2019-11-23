"""
    Scan Aim AP Program, https://kylinchen.top/Wifi-Indoor-Location/
    Kylinchen, www.kylinchen.top, k1017856853@icloud.com
"""

import sys
import pywifi
import time

from config import INIT_AP, INTERFACE
from exceptionHandler import AP_NOT_EXIST

class Scanner(object):
    def __init__(self,init_ap_list=INIT_AP):
        self.aplist = init_ap_list
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def scan_all(self):
        """
        return a ap_list as [
            {"ssid":item.ssid, "signal":item.signal, "akm":item.akm, "freq":item.freq}
            ......
        ]
        """
        self.iface.scan()
        result=self.iface.scan_results()
        ret = []
        for item in result:
            ret.append({"ssid":item.ssid, "signal":item.signal, "akm":item.akm, "freq":item.freq})
        return ret

    def scan_aim(self):
        """
        rerturn all the wifi-information about aps in aplist
        """
        ret_dict = {}
        check_dict = {}
        tmp_flag = 0
        full_flag = len(self.aplist)
        for item in self.aplist:
            check_dict[item]=0
            ret_dict[item]={}
        scan_result = self.scan_all()
        for item in scan_result:
            if((item["ssid"] in self.aplist) and (check_dict[item["ssid"]]==0)):
                ret_dict[item["ssid"]] = item
                check_dict[item["ssid"]] = 1
                tmp_flag += 1
            if(tmp_flag>=full_flag):
                break
        return ret_dict

    def append_aim(self,aim):
        """
        manually add some ap from aim_list(aplist)
        """
        if(aim in self.aplist):
            pass
        else:
            self.aplist.append(aim)
        pass

    def dump_aim(self):
        """
        return aplist refreshed 
        """
        return self.aplist

    def drop_aim(self,aim):
        """
        manually remove some ap from aim_list(aplist)
        """
        try:
            self.aplist.remove(aim)
        except:
            raise AP_NOT_EXIST
        pass

    def check(self, aim):
        """
        manually add an ap and return its inforamation(do not add it to aplist)
        """
        ret_dict = {}
        ret_dict[aim]={}
        scan_result = self.scan_all()
        for item in scan_result:
            if(item["ssid"]==aim):
                ret_dict[aim]=item["ssid"]
        return ret_dict
        pass

    @staticmethod
    def clock(): 
        return time.localtime()

    @staticmethod
    def manu_sleep(interval):
        time.sleep(interval)

if __name__ == "__main__":
    test = Scanner(INIT_AP)
    while(True):
        os.system("networksetup -setairportpower en0 on")
        a = test.scan_aim()
        print(a)
        os.system("networksetup -setairportpower en0 off")