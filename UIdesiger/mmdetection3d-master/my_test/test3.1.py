import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import numpy as np
import copy



class App:
    MENU_OPEN = 1

    MENU_SHOW = 5

    MENU_QUIT = 20
    MENU_ABOUT = 21

    show = True

    _picked_indicates = []
    _picked_points = []
    _pick_num = 0

    _label3d_list = []

    def __init__(self):
        gui.Application.instance.initialize()

        self.window = gui.Application.instance.create_window("Pick Points", 800, 600)
        w = self.window
        em = w.theme.font_size

        # 渲染窗口
        self._scene = gui.SceneWidget()
        self._scene.scene = rendering.Open3DScene(w.renderer)


        self._info = gui.Label("")
        self._info.visible = False

        # 布局回调函数
        w.add_child(self._scene)
        w.add_child(self._info)

        # ---------------Menu----------------
        # 菜单栏是全局的（因为macOS上是全局的）
        # 无论创建多少窗口，菜单栏只创建一次。

        # ----以下只针对Windows的菜单栏创建----
        if gui.Application.instance.menubar is None:
            # 文件菜单栏
            file_menu = gui.Menu()
            file_menu.add_item("Open", App.MENU_OPEN)
            file_menu.add_separator()
            file_menu.add_item("Quit", App.MENU_QUIT)

            # 显示菜单栏
            show_menu = gui.Menu()
            show_menu.add_item("Show Geometry", App.MENU_SHOW)
            show_menu.set_checked(App.MENU_SHOW, True)

            # 帮助菜单栏
            help_menu = gui.Menu()
            help_menu.add_item("About", App.MENU_ABOUT)
            help_menu.set_enabled(App.MENU_ABOUT, False)

            # 菜单栏
            menu = gui.Menu()
            menu.add_menu("File", file_menu)
            menu.add_menu("Show", show_menu)
            menu.add_menu("Help", help_menu)

            gui.Application.instance.menubar = menu



    def _on_cancel(self):
        # 关闭当前对话框
        self.window.close_dialog()


    def run(self):
        gui.Application.instance.run()


if __name__ == "__main__":
    app = App()
    app.run()
