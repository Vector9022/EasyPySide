from PySide6.QtWidgets import QApplication
from localLib.absPath import absPath
import localLib.PySideTray as PST 
import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.tray = TrayIcon(self)

    def Run(self):
        self.app.exec()

    def Quit(self):
        self.app.quit()

class TrayIcon:
    def __init__(self, UIApp: App):
        self.UIApp = UIApp

        self.trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))
        self.trayIcon.onRightClick = lambda: self.trayIcon.showMenu()
        self.trayIcon.setToolTip("BasicPythonProject")

        self.themes = self.trayIcon.menu.addSubMenu("Themes")
        self.themes.addQActionGroup([{"text": "Light"}, {"text": "Dark", "checked": True}], callback=self.toggleDarkTheme,stayOpen=True)
        self.trayIcon.menu.addQAction("!checkable", callback=lambda a: print("Clicked:", a.text()), icon=absPath("resources\\terminalWhite.ico"), stayOpen=False)
        self.trayIcon.menu.addSeparator()
        self.trayIcon.menu.addCheckableQAction("checkable", callback=lambda a: print("Clicked:", a.text()), checked=True, stayOpen=True)

        self.trayIcon.show()

    def toggleDarkTheme(self, action):
        print("Clicked:", action.text())
        if action.text() == "Dark":
            self.trayIcon.menu.setStyleSheet()
        else:
            self.trayIcon.menu.setStyleSheet("")