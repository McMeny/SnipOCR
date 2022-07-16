import sys
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QImage
import engine

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
        self.Snip_tool = engine.Snip_tool()

        new_snip = QAction('New', self)
        new_snip.setStatusTip('Snip')
        new_snip.clicked.connect(self.new_img_window)

        def new_img_window(self):
            if self.Snip_tool.background:
                self.close()
            self.Snip_tool.start()

        #snipcopy_btn = QPushButton(window)
        #snipcopy_btn.move(110, 10)
        #snipcopy_btn.setText('Snip and Copy Text')
        #snipcopy_btn.resize(130,50)
        #layout.addWidget(snipcopy_btn)
        #closes the application with the 'x' button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
