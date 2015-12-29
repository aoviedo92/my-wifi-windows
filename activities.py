from PyQt4.QtGui import *
ACTION_BAR_HEIGHT = 50


class HotSpot(QFrame):
    def __init__(self, parent=None):
        super(HotSpot, self).__init__(parent)
        # read = start_hosted_network()
        # print(read)
        label = QLabel("k")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.move(10, 60)
