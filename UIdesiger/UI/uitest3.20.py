import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QPushButton, QMessageBox
from argparse import ArgumentParser

from mmdet3d.apis import inference_detector, init_model, show_result_meshlab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("基于三维点云的目标检测算法的软件系统设计与实现")

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 创建文件菜单
        file_menu = menu_bar.addMenu("文件")

        # 创建打开数据集动作
        open_dataset_action = QAction("打开数据集", self)
        open_dataset_action.triggered.connect(self.open_dataset)

        # 创建打开模型动作
        open_model_action = QAction("打开模型", self)
        open_model_action.triggered.connect(self.open_model)

        # 创建打开py动作
        open_py_action = QAction("打开py文件", self)
        open_py_action.triggered.connect(self.open_py)

        # 创建退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)

        # 添加动作到文件菜单
        file_menu.addAction(open_dataset_action)
        file_menu.addAction(open_model_action)
        file_menu.addAction(open_py_action)
        file_menu.addAction(exit_action)

        # 创建按钮
        self.start_button = QPushButton("开始执行", self)
        self.start_button.setGeometry(100, 100, 200, 50)
        self.start_button.clicked.connect(self.start_execution)

        # 初始化数据集、模型和py文件的路径
        self.dataset_path = None
        self.model_path = None
        self.py_path = None

    def open_dataset(self):
        # 打开数据集对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("bin文件 (*.bin)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.dataset_path = filenames[0]
            print("打开数据集:", self.dataset_path)

    def open_model(self):
        # 打开模型对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("模型文件 (*.pth)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.model_path = filenames[0]
            print("打开模型:", self.model_path)

    def open_py(self):
        # 打开模型对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("py文件 (*.py)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.py_path = filenames[0]
            print("打开py:", self.py_path)

    def start_execution(self):
        if self.dataset_path is None:
            QMessageBox.warning(self, "警告", "请先选择数据集")
            return
        if self.model_path is None:
            QMessageBox.warning(self, "警告", "请先选择模型")
            return
        if self.py_path is None:
            QMessageBox.warning(self, "警告", "请先选择py文件")
            return

        # 执行代码
        print("开始执行")

        parser = ArgumentParser()
        parser.add_argument('pcd', help='Point cloud file')
        parser.add_argument('config', help='Config file')
        parser.add_argument('checkpoint', help='Checkpoint file')
        parser.add_argument(
            '--device', default='cuda:0', help='Device used for inference')
        parser.add_argument(
            '--score-thr', type=float, default=0.0, help='bbox score threshold')
        parser.add_argument(
            '--out-dir', type=str, default='demo', help='dir to save results')
        parser.add_argument(
            '--show',
            action='store_true',
            help='show online visualization results')
        parser.add_argument(
            '--snapshot',
            action='store_true',
            help='whether to save online visualization results')
        args = parser.parse_args()
        print(args)
        # build the model from a config file and a checkpoint file
        model = init_model(args.config, args.checkpoint, device=args.device)
        # test a single image
        result, data = inference_detector(model, args.pcd)
        # show the results
        show_result_meshlab(
            data,
            result,
            args.out_dir,
            args.score_thr,
            show=args.show,
            snapshot=args.snapshot,
            task='det')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
