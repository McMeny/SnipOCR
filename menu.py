import sys
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QImage
import SnipOCR

app = QApplication(sys.argv)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0 ,0 , 450, 70)
        self.setWindowTitle('SnipOCR')

        layout = QHBoxLayout()
        snip_btn = QPushButton(self)
        snip_btn.move(10, 10)
        snip_btn.setText('Snip')
        snip_btn.resize(80,50)
        layout.addWidget(snip_btn)
        snip_btn.clicked.connect(SnipOCR.Snip_tool)

        #snipcopy_btn = QPushButton(window)
        #snipcopy_btn.move(110, 10)
        #snipcopy_btn.setText('Snip and Copy Text')
        #snipcopy_btn.resize(130,50)
        #layout.addWidget(snipcopy_btn)
        self.show()
        #closes the application with the 'x' button
        sys.exit(app.exec_())

if __name__ == '__main__':
    window = Window()
    window.show()
    sys.exit(app.exec_())
