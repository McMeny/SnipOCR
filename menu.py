import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from SnipOCR import *


class Window():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0 ,0 , 450, 70)
    window.setWindowTitle('SnipOCR')

    layout = QHBoxLayout()
    snip_btn = QPushButton(window)
    snip_btn.move(10, 10)
    snip_btn.setText('Snip')
    snip_btn.resize(80,50)
    layout.addWidget(snip_btn)
    snip = Snip_tool()
    snip_btn.clicked(snip)

    #snipcopy_btn = QPushButton(window)
    #snipcopy_btn.move(110, 10)
    #snipcopy_btn.setText('Snip and Copy Text')
    #snipcopy_btn.resize(130,50)
    #layout.addWidget(snipcopy_btn)
    window.show()
    #closes the application with the 'x' button
    sys.exit(app.exec_())

if __name__ == '__main__':
    Window()
