class Snip_copytool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0,0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.4)
        QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
        root.withdraw()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
        qp.setBrush(QtGui.QColor(126, 126, 200, 0))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox = (x1, y1, x2, y2))
        img_array = np.array(img)
        img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        text = pytesseract.image_to_string(img)
        pc.copy(text)
        print(text)

        if numpy_image is not None and snip_number is not None:
            self.image = self.convert_numpy_img_to_qpixmap(numpy_image)
            self.change_and_set_title("Snip #{0}".format(snip_number))
        else:
            self.image = QPixmap("background.PNG")
            self.change_and_set_title(Menu.default_title)

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Snip_copytool()
        window.show()
        app.aboutToQuit.connect(app.deleteLater)
        sys.exit(app.exec_())