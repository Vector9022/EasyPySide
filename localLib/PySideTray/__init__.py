from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QWidgetAction
from PySide6.QtGui import QIcon, QAction, QCursor, QActionGroup
from .base64Icon import getIcon

def _popupAllMenu(menu):
    menus = []
    m = menu
    while isinstance(m, QMenu):
        menus.append(m)
        m = m.parentWidget()

    for m in reversed(menus):
        m.popup(m.pos())

class DefaultMenu(QMenu):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet()

    def setStyleSheet(self, styleSheet=None):
        if styleSheet is None:
            styleSheet = """
                QMenu {
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 1px solid #444444;
                }

                QMenu::item {
                    padding-left: 10px;
                    padding-right: 20px;
                    padding-top: 4px;
                    padding-bottom: 4px;
                    margin-left: 0px;
                }

                QMenu::item:selected {
                    background-color: #505050;
                }

                QMenu::separator {
                    height: 1px;
                    background: #444444;
                    margin: 5px 0px 5px 0px;
                }

                QMenu::icon {
                    margin-left: 13px;
                }
            """

        super().setStyleSheet(styleSheet)

        for action in self.actions():
            submenu = action.menu()
            if submenu:
                submenu.setStyleSheet(styleSheet)

    def addQAction(self, text, callback=None, icon=None, stayOpen=False):
        action = QAction(text, self)

        if icon:
            action.setIcon(QIcon(icon))

        def handler():
            if callable(callback):
                callback(action)

            if stayOpen:
                QTimer.singleShot(0, lambda: _popupAllMenu(self))

        action.triggered.connect(handler)

        self.addAction(action)
        return action

    def addCheckableQAction(self, text, callback=None, checked=False, stayOpen=False):
        def updateIcon():
            if action.ischecked:
                action.setIcon(QIcon(getIcon("CheckBoxTrue")))
            else:
                action.setIcon(QIcon(getIcon("CheckBoxFalse")))

        action = QAction(text, self)
        action.ischecked = checked
        updateIcon()

        def handler():
            action.ischecked = not action.ischecked
            updateIcon()

            if callable(callback):
                callback(action)

            if stayOpen:
                QTimer.singleShot(0, lambda: _popupAllMenu(self))

        action.triggered.connect(handler)

        self.addAction(action)
        return action

    def addQActionGroup(self, items, callback=None, stayOpen=False):
        """
        items = [
            {"text": "Light", "checked": True},
            {"text": "Dark"},
        ]
        """
        group = QActionGroup(self)
        group.setExclusive(True)

        actions = []

        for item in items:
            action = QAction(item["text"], self)
            action.setCheckable(True)

            if item.get("checked", False):
                action.setChecked(True)

            group.addAction(action)
            self.addAction(action)
            actions.append(action)

        def handler(action):
            if callable(callback):
                callback(action)

            if stayOpen:
                QTimer.singleShot(0, lambda: _popupAllMenu(self))

        group.triggered.connect(handler)

        return actions

    def addSubMenu(self, text, icon=None):
        submenu = DefaultMenu(text, self)

        if icon:
            submenu.setIcon(QIcon(icon))

        self.addMenu(submenu)
        submenu.setStyleSheet(self.styleSheet())

        return submenu

    def addSeparator(self):
        return super().addSeparator()

    def hideEvent(self, event):
        for action in self.actions():
            submenu = action.menu()
            if submenu and submenu.isVisible():
                submenu.hide()
        super().hideEvent(event)

class SystemTrayIcon(QObject):
    def __init__(self, iconPath, parent=None):
        super().__init__(parent)

        self.tray = QSystemTrayIcon()
        self.setIcon(iconPath)

        self.onLeftClick = None
        self.onRightClick = None
        self.onDoubleClick = None
        self.onMiddleClick = None
        self.menu = DefaultMenu()

        self.tray.activated.connect(self._onActivated)

    def show(self):
        self.tray.show()

    def hide(self):
        self.tray.hide()

    def setIcon(self, iconPath):
        self.tray.setIcon(QIcon(iconPath))

    def setToolTip(self, toolTip):
        self.tray.setToolTip(toolTip)

    def showMenu(self):
        if self.menu:
            self.menu.exec(QCursor.pos())

    def _onActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if callable(self.onLeftClick):
                self.onLeftClick()

        elif reason == QSystemTrayIcon.ActivationReason.Context:
            if callable(self.onRightClick):
                self.onRightClick()

        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if callable(self.onDoubleClick):
                self.onDoubleClick()

        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            if callable(self.onMiddleClick):
                self.onMiddleClick()