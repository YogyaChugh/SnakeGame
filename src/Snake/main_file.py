import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor, QFont


class FPSWindow(QWidget):
    def __init__(self, target_fps=60):
        super().__init__()

        self.setWindowTitle("Stable FPS Counter")
        self.setGeometry(100, 100, 400, 300)

        # Set fixed FPS
        self.target_fps = target_fps
        self.frame_time = int(1000 / target_fps)  # Convert FPS to milliseconds per frame

        # Timer to update the screen at a fixed FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.frame_time)

    def update_frame(self):
        """ Updates the frame at a fixed FPS """
        self.update()  # Triggers a repaint

    def paintEvent(self, event):
        """ Handles the rendering of FPS text on the window. """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background color
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Draw constant FPS text
        painter.setFont(QFont("Arial", 20))
        painter.setPen(QColor(0, 255, 0))
        fps_text = f"FPS: {self.target_fps:.2f}"  # Fixed FPS
        painter.drawText(20, 40, fps_text)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FPSWindow(target_fps=60)  # Set FPS to 60
    window.show()
    sys.exit(app.exec())
