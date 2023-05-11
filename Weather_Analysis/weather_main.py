import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from weather_api3 import *

form_main = uic.loadUiType("weather_ui.ui")[0] #ui 파일 불러오기

class MainWindow(QMainWindow,QWidget,form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Weather API")
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.pushButton.clicked.connect(self.buttonClicked) # 버튼 클릭 시 실행되는 이벤트

    def buttonClicked(self):
        self.text = self.lineEdit.text() # textEdit의 값을 가져와서 변수 text에 저장
        self.textEdit.setText(get_weather(self.text)) # 날씨 정보를 스트링으로 가져옴
        self.textEdit.append("")
        self.textEdit.append(">> 날씨 분석")
        self.textEdit.append(current_time())
        self.textEdit.append(weather_analysis())
        self.textEdit.append("")
        self.textEdit.append("현재 불러온 API 배포 시간: " + str(weather_data['time'][0]) + "시")
        self.textEdit.append("다음 API 배포 시간: " + str(weather_data['time'][3]) + "시")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())