
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import subprocess,res,re,sys
from scapy.all import RandMAC

vendor_mac = {'Raytheon Raylink/WebGear Aviator2.4': '00:00:f1', 'Samsung MagicLan (+ some other PrismII cards)': '00:02:78', '3Com 3CRWE62092A': '00:01:03',
            'Lucent (WaveLAN, Orinoco, Silver/Gold), Orinoco (Silver, PC24E), Buffalo and Avaya': '00:02:2d', 'Senao SL-2011CD': '00:02:6f', 'Compaq WL110': '00:02:a5', 'Linksys WPC11, Repotec GL241101': '00:03:2f', 
            'Linksys WPC11, WUSB11': '00:04:5a', '3Com 3CRWE62092B': '00:04:75', 'SMC SMC2632W': '00:04:e2', 'D-Link DWL-650, DWL-650H': '00:05:5d', 'Linksys WPC11 v2.5, D-Link DCF-650W, Linksys WPC11 v3': '00:06:25', 
            'Cisco AIR-PCM352': '00:0a:8a', 'Cisco AIR-LMC352': '00:09:e8', 'Netgear MA701, MA401RA': '00:09:5b', 'Apple Airport Card 2002': '00:30:65', 'Netgear MA401': '00:30:ab', 'Belkin F5D6020': '00:30:bd',
            'Cisco AIR-PC4800, 350, AIR-PCM340, AIR-PCM352': '00:40:96', 'Compaq WL100': '00:50:08', '3Com 3CRWE73796B': '00:50:da', 'Lucent WaveLAN Silver': '00:60:01', 'Lucent WaveLAN Bronze, WaveLAN Gold, Silver, Orinoco Gold': '00:60:1d',
            'Cabletron CSIBB-AA': '00:60:6d', 'SMC SMC2642W': '00:60:b3', 'Netwave (Xircom Netwave/Netwave Airsurfer)': '00:80:c7', 'LeArtery SyncByAir LN101': '00:90:d1', 'Symbol Spectrum24': '00:a0:f8', 
            'Intel Pro 2100': '00:0c:f1', 'OEM OEM': '00:e0:29', 'Old Lucent Wavelan': '08:00:0e', 'Sony PCWA-C10': '08:00:46', 'Global Apps Corp.': 'fc:13:49', 'Hewlett Packard': 'fc:15:b4', 'Taian Technology(Wuxi) Co.,Ltd.': 'fc:16:07',
            'InterCreative Co., Ltd': 'fc:17:94', 'Cloud Vision Networks Technology Co.,Ltd.': 'fc:19:d0', 'V-ZUG AG': 'fc:1b:ff', 'I Smart Cities HK Ltd': 'fc:1d:59', 'IPEVO corp': 'fc:1e:16',
            'SAMSUNG ELECTRO-MECHANICS CO., LTD.': 'fc:1f:19', 'EURECAM': 'fc:1f:c0', 'Han Kyung I Net Co.,Ltd.': 'fc:22:9c', 'Apple': 'fc:25:3f', 'TRANS ELECTRIC CO., LTD.': 'fc:27:a2', 'Connected Data, Inc.': 'fc:2a:54',
            'Lorom Industrial Co.LTD.': 'fc:2e:2d', 'Calxeda, Inc.': 'fc:2f:40', 'Favite Inc.': 'fc:35:98', 'Visteon corp': 'fc:35:e6', 'Henan Lanxin Technology Co., Ltd': 'fc:3f:ab', 'Universal Audio': 'fc:44:63',
            'Swarco LEA d.o.o.': 'fc:44:99', 'JIANGXI SHANSHUI OPTOELECTRONIC TECHNOLOGY CO.,LTD': 'fc:45:5f', 'HUAWEI TECHNOLOGIES CO.,LTD': 'fc:48:ef', 'Castlenet Technology Inc.': 'fc:4a:e9', 'INTERSENSOR S.R.L.': 'fc:4b:1c', 
            'Sunplus Technology Co., Ltd.': 'fc:4b:bc', 'Universal Global Scientific Industrial Co., Ltd.': 'fc:4d:d4', 'SIMEX Sp. z o.o.': 'fc:50:90', 'Control iD': 'fc:52:ce', 
            'Shen Zhen Shi Xin Zhong Xin Technology Co.,Ltd.': 'fc:58:fa', 'Weibel Scientific A/S': 'fc:5b:24', 'MikroBits': 'fc:5b:26', 'Zhejiang Kangtai Electric Co., Ltd.': 'fc:60:18', 'NEC Personal Products, Ltd': 'fc:61:98',
            'Beijing MDC Telecom': 'fc:62:6e', 'Directed Perception, Inc': 'fc:68:3e', 'LXinstruments GmbH': 'fc:6c:31', 'D-Link International': 'fc:75:16', 'Handreamnet': 'fc:75:e6', 'FCI USA LLC': 'fc:7c:e7',
            'Trei technics': 'fc:83:29', 'Avaya, Inc': 'fc:a8:41', 'Shenzhen Gongjin Electronics Co.,Ltd': 'fc:8b:97', 'Pace plc': 'fc:8e:7e', 'Intelligent Technology Inc.': 'fc:8f:c4', 'Nokia Corporation': 'fc:92:3b', 
            'UBIVELOX': 'fc:94:6c', 'Technicolor USA Inc.': 'fc:94:e3', 'Cisco': 'fc:99:47', 'Fidus Systems Inc': 'fc:9f:ae', 'Samsung Electronics': 'fc:a1:3e', 'MIARTECH (SHANGHAI),INC.': 'fc:a9:b0', 'QTS NETWORKS': 'fc:ad:0f', 
            'Conemtech AB': 'fc:af:6a', 'Shanghai DareGlobal Technologies Co., Ltd': 'fc:b0:c4', 'Shenzhen Minicreate Technology Co.,Ltd': 'fc:bb:a1', 'Atmel Corporation': 'fc:c2:3d', 'Murata Manufacturing Co., Ltd.': 'fc:c2:de', 
            'Samsung Electronics Co.,Ltd': 'fc:c7:34', 'ZTE Corporation': 'fc:c8:97', 'Ascon Ltd.': 'fc:cc:e4', 'IBM Corp': 'fc:cf:62'}

class mainapp(QMainWindow):
    def __init__(self):
        super(mainapp,self).__init__()
        loadUi("mc.ui",self)
        self.change.clicked.connect(self.changemac)
        self.getmac.clicked.connect(self.current_mac)
        self.refrech.clicked.connect(self.getdevices)
        self.reset.clicked.connect(self.permanent)
        a = [i for i in vendor_mac]
        a.sort()
        self.vendor.addItems(list(a))
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def changemac(self):
        msg = QMessageBox()
        i=self.devices.currentText()
        msg.setStandardButtons(QMessageBox.Ok)
        try:
            
            if self.custom_mac.isChecked() :
                if re.search(r"(\w\w:){5}\w\w",self.mac.text()):
                    m = self.mac.text()
                    
                    
                else: 
                    msg.setWindowTitle('Error')
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText('Please enter a valide MAC address!')
                    x = msg.exec_()
            elif self.rand_mac.isChecked():
                m = vendor_mac[self.vendor.currentText()] + str(RandMAC())[8::]
                


            subprocess.call(["ifconfig",i,"down"])
            subprocess.call(["ifconfig",i,"hw","ether",m])
            subprocess.call(["ifconfig",i,"up"])
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('MAC changed')
            msg.setText('Your MAC address changed succesfully to :\n'+self.get_mac())        
            x = msg.exec_()

        except:
            if not self.get_mac :
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Error')
                msg.setText('Please specefiy a device!')
                x = msg.exec_()
           

    def get_mac(self):
        try:
            ifconfig_result = subprocess.check_output(["ifconfig",self.devices.currentText()])
            current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
            return current_mac.group(0)
        except:
            pass
        

    def current_mac(self):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.devices.currentText() + ' Current MAC Address : ' + self.get_mac())
            x = msg.exec_()
        except:
            pass
    def getdevices(self):
        ifconfig_result = subprocess.check_output(["ifconfig"])
        interface =re.findall(r'(?:n)(\w*)(?::\s)|(\w*)(?::\s)',str(ifconfig_result))
        self.devices.clear()
        self.devices.addItems([''.join(i) for i in interface if 'lo' not in i])
    def permanent(self):
        msg = QMessageBox()
        try:
            subprocess.getoutput(['macchanger -p '+self.devices.currentText()])
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('MAC changed')
            msg.setText('MAC address reset succesfully to :\n'+self.get_mac())
            
        except:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('ERROR')
            msg.setText('Can\'t change MAC\nPlease try again!')
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = mainapp()
    Form.show()
    sys.exit(app.exec_())
