# 创新项目
# 编程：任宏培
# 开发时间：2023/3/16 0:25
import open3d.visualization.opengl_renderer as o3dgl
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QOpenGLFramebufferObjectFormat
from PyQt5.QtOpenGL import QGLWidget, QOpenGLContext


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = o3dgl.OpenGLRenderer()
        self.timer = self.startTimer(10)

    def initializeGL(self):
        self.renderer.clear_color = (0.2, 0.2, 0.2, 1.0)

    def resizeGL(self, w, h):
        self.renderer.viewport = (0, 0, w, h)
        self.renderer.projection = o3dgl.PinholeCameraIntrinsic(w, h, 500, 500, w / 2, h / 2)

    def paintGL(self):
        self.renderer.clear()
        # 绘制Open3D场景
        # self.renderer.draw_geometry(my_geometry)

    def timerEvent(self, event):
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建OpenGL视图窗口
        self.gl_widget = GLWidget(self)

        # 创建按钮
        self.button = QPushButton('Button', self)

        # 创建布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.gl_widget)
        layout.addWidget(self.button)

        # 连接按钮的点击事件
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        print('Button clicked')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()