import sys
import psutil

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QToolBar, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtGui import QAction, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QPointF


class CpuDataThread(QThread):
    new_data = Signal(float)

    def __init__(self, interval=100, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.timer = None

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.collect_data)
        self.timer.start(self.interval)
        self.exec()

    def collect_data(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        self.new_data.emit(cpu_usage)


class RamDataThread(QThread):
    new_data = Signal(float)

    def __init__(self, interval=100, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.timer = None

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.collect_data)
        self.timer.start(self.interval)
        self.exec()

    def collect_data(self):
        memory = psutil.virtual_memory()
        ram_usage = memory.percent
        self.new_data.emit(ram_usage)


class CpuGraphWidget(QWidget):
    def __init__(self, parent=None):
        super(CpuGraphWidget, self).__init__(parent)
        self.data = [0] * 100

        self.thread = CpuDataThread(interval=70) # 70
        self.thread.new_data.connect(self.update_data)
        self.thread.start()

    def update_data(self, value):
        self.data.append(value)
        if len(self.data) > 100:
            self.data.pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(30, 30, 30))

        pen = QPen(QColor(50, 50, 50), 1, Qt.SolidLine)
        painter.setPen(pen)
        self.draw_grid(painter)

        pen = QPen(QColor(0, 200, 255), 2, Qt.SolidLine)
        painter.setPen(pen)

        width = self.size().width()
        height = self.size().height()

        max_x = len(self.data)
        max_y = 100

        points = [
            QPointF(
                (i / max_x) * width,
                height - (value / max_y) * height
            )
            for i, value in enumerate(self.data)
        ]

        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

    def draw_grid(self, painter):
        width = self.size().width()
        height = self.size().height()

        for i in range(0, width, width // 10):
            painter.drawLine(i, 0, i, height)

        for i in range(0, height, height // 10):
            painter.drawLine(0, i, width, i)


class GpuGraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GpuGraphWidget, self).__init__(parent)
        self.data = [0] * 100

        self.thread = CpuDataThread(interval=70) # 70
        self.thread.new_data.connect(self.update_data)
        self.thread.start()

    def update_data(self, value):
        self.data.append(value)
        if len(self.data) > 100:
            self.data.pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(30, 30, 30))

        pen = QPen(QColor(50, 50, 50), 1, Qt.SolidLine)
        painter.setPen(pen)
        self.draw_grid(painter)

        pen = QPen(QColor(190, 10, 170), 2, Qt.SolidLine)
        painter.setPen(pen)

        width = self.size().width()
        height = self.size().height()

        max_x = len(self.data)
        max_y = 100

        points = [
            QPointF(
                (i / max_x) * width,
                height - (value / max_y) * height
            )
            for i, value in enumerate(self.data)
        ]

        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

    def draw_grid(self, painter):
        width = self.size().width()
        height = self.size().height()

        for i in range(0, width, width // 10):
            painter.drawLine(i, 0, i, height)

        for i in range(0, height, height // 10):
            painter.drawLine(0, i, width, i)


class RamGraphWidget(QWidget):
    def __init__(self, parent=None):
        super(RamGraphWidget, self).__init__(parent)
        self.data = [0] * 100

        self.thread = RamDataThread(interval=70) # 70
        self.thread.new_data.connect(self.update_data)
        self.thread.start()

    def update_data(self, value):
        self.data.append(value)
        if len(self.data) > 100:
            self.data.pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(30, 30, 30))

        pen = QPen(QColor(50, 50, 50), 1, Qt.SolidLine)
        painter.setPen(pen)
        self.draw_grid(painter)

        pen = QPen(QColor(50, 255, 100), 2, Qt.SolidLine)
        painter.setPen(pen)

        width = self.size().width()
        height = self.size().height()

        max_x = len(self.data)
        max_y = 100

        points = [
            QPointF(
                (i / max_x) * width,
                height - (value / max_y) * height
            )
            for i, value in enumerate(self.data)
        ]

        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

    def draw_grid(self, painter):
        width = self.size().width()
        height = self.size().height()

        for i in range(0, width, width // 10):
            painter.drawLine(i, 0, i, height)

        for i in range(0, height, height // 10):
            painter.drawLine(0, i, width, i)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window")
        self.setFixedSize(440, 290)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.stack = QStackedWidget(self)
        self.cpu_widget = CpuGraphWidget()
        self.gpu_widget = GpuGraphWidget()
        self.ram_widget = RamGraphWidget()

        self.stack.addWidget(self.cpu_widget)
        self.stack.addWidget(self.gpu_widget)
        self.stack.addWidget(self.ram_widget)

        self.interface()

    def create_main_toolbar(self):
        toolbar = QToolBar("MainToolBar")
        toolbar.setMovable(True)

        self.addToolBar(toolbar)

        cpu_action = QAction("CPU", self)
        cpu_action.triggered.connect(self.show_cpu)
        toolbar.addAction(cpu_action)

        gpu_action = QAction("GPU", self)
        gpu_action.triggered.connect(self.show_gpu)
        toolbar.addAction(gpu_action)

        ram_action = QAction("RAM", self)
        ram_action.triggered.connect(self.show_ram)
        toolbar.addAction(ram_action)

    def show_cpu(self):
        self.stack.setCurrentWidget(self.cpu_widget)

    def show_gpu(self):
        self.stack.setCurrentWidget(self.gpu_widget)

    def show_ram(self):
        self.stack.setCurrentWidget(self.ram_widget)

    def interface(self):
        self.create_main_toolbar()

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
