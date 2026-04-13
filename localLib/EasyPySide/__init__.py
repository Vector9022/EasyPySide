from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QEvent
from PySide6.QtGui import QFont, QIcon, QPixmap

class _ResizeZone(QWidget):
    """
    Внутренний служебный виджет.
    Отвечает за ресайз безрамочного окна.
    """

    _cursorMap = {
        "top": Qt.SizeVerCursor,
        "bottom": Qt.SizeVerCursor,
        "left": Qt.SizeHorCursor,
        "right": Qt.SizeHorCursor,
        "top_left": Qt.SizeFDiagCursor,
        "bottom_right": Qt.SizeFDiagCursor,
        "top_right": Qt.SizeBDiagCursor,
        "bottom_left": Qt.SizeBDiagCursor,
    }

    def __init__(self, parent: QWidget, edge: str):
        super().__init__(parent)

        self._edge = edge
        self._isResizing = False
        self._startMousePos = QPoint()
        self._startGeometry = QRect()

        self.setMouseTracking(True)
        self.setCursor(self._cursorMap[edge])

    # Mouse events
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        parent = self.parent()

        if not parent._resizeEnabled or parent._isMaximized:
            return

        self._isResizing = True
        self._startMousePos = event.globalPosition().toPoint()
        self._startGeometry = parent.geometry()
        event.accept()

    def mouseMoveEvent(self, event):
        if not self._isResizing:
            return

        delta = event.globalPosition().toPoint() - self._startMousePos
        newGeometry = QRect(self._startGeometry)

        parent = self.parent()
        minWidth = parent.minimumWidth()
        minHeight = parent.minimumHeight()

        # Правая грань
        if "right" in self._edge:
            newWidth = max(minWidth, self._startGeometry.width() + delta.x())
            newGeometry.setWidth(newWidth)

        # Нижняя грань
        if "bottom" in self._edge:
            newHeight = max(minHeight, self._startGeometry.height() + delta.y())
            newGeometry.setHeight(newHeight)

        # Левая грань
        if "left" in self._edge:
            newWidth = self._startGeometry.width() - delta.x()
            if newWidth < minWidth:
                delta.setX(self._startGeometry.width() - minWidth)
                newWidth = minWidth

            newGeometry.setLeft(self._startGeometry.left() + delta.x())
            newGeometry.setWidth(newWidth)

        # Верхняя грань
        if "top" in self._edge:
            newHeight = self._startGeometry.height() - delta.y()
            if newHeight < minHeight:
                delta.setY(self._startGeometry.height() - minHeight)
                newHeight = minHeight

            newGeometry.setTop(self._startGeometry.top() + delta.y())
            newGeometry.setHeight(newHeight)

        parent.setGeometry(newGeometry)

    def mouseReleaseEvent(self, event):
        self._isResizing = False

class BaseWindow(QWidget):
    """
    Базовый шаблон окна.
    """

    def __init__(self):
        super().__init__()

        self._isMaximized = False
        self._normalGeometry: QRect | None = None
        self._dragOffset: QPoint | None = None
        self._resizeEnabled = True
        self._resizeMargin = 5

        self._setupWindow()
        self._createLayout()
        self._createTitleBar()
        self._createContentArea()
        self._createResizeZones()
        self._applyStyles()

    def _setupWindow(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(161, 35)
        self.resize(1000, 500)

    def _createLayout(self):
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

    def _createTitleBar(self):
        self._titleBar = QWidget(self)
        self._titleBar.setFixedHeight(35)
        self._titleBar.setProperty("titleBar", "")

        mainLayout = QHBoxLayout(self._titleBar)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # === LEFT SECTION ===
        self._titleLeft = QWidget()
        self.leftLayout = QHBoxLayout(self._titleLeft)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(0)
        self.leftLayout.setAlignment(Qt.AlignLeft)

        self._titleIcon = QLabel()
        self._titleIcon.setFixedSize(self._titleBar.height(), self._titleBar.height())
        self._titleIcon.setAlignment(Qt.AlignCenter)

        self._titleLabel = QLabel()
        self._titleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.leftLayout.addWidget(self._titleIcon)
        self.leftLayout.addWidget(self._titleLabel)

        # === CENTER SECTION ===
        self._titleCenter = QWidget()
        self.centerLayout = QHBoxLayout(self._titleCenter)
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.centerLayout.setSpacing(0)
        self.centerLayout.setAlignment(Qt.AlignCenter)

        # === RIGHT SECTION ===
        self._titleRight = QWidget()
        self.rightLayout = QHBoxLayout(self._titleRight)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(0)
        self.rightLayout.setAlignment(Qt.AlignRight)

        iconFont = QFont("Segoe Fluent Icons")
        iconFont.setPointSize(10)

        self._btnMinimize = QPushButton("\ue921")
        self._btnMaximize = QPushButton("\ue922")
        self._btnClose = QPushButton("\ue8bb")

        for button in (self._btnMinimize, self._btnMaximize, self._btnClose):
            button.setFixedSize(self._titleBar.height() + 5, self._titleBar.height())
            button.setFont(iconFont)

        self._btnClose.setProperty("closeButton", "")

        # Connect
        self._btnClose.clicked.connect(QApplication.quit)
        self._btnMinimize.clicked.connect(self.showMinimized)
        self._btnMaximize.clicked.connect(self._toggleMaximize)

        self.rightLayout.addWidget(self._btnMinimize)
        self.rightLayout.addWidget(self._btnMaximize)
        self.rightLayout.addWidget(self._btnClose)

        # === ADD TO MAIN LAYOUT ===
        mainLayout.addWidget(self._titleLeft)
        mainLayout.addWidget(self._titleCenter, 1)  # растягивается
        mainLayout.addWidget(self._titleRight)

        self._mainLayout.addWidget(self._titleBar)

        self._titleBar.installEventFilter(self)

    def _createContentArea(self):
        self.contentArea = QWidget(self)
        self._mainLayout.addWidget(self.contentArea)

    def _createResizeZones(self):
        self._resizeZones = {
            edge: _ResizeZone(self, edge)
            for edge in (
                "top",
                "bottom",
                "left",
                "right",
                "top_left",
                "top_right",
                "bottom_left",
                "bottom_right",
            )
        }

        self._updateResizeZones()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._updateResizeZones()

    def _updateResizeZones(self):
        margin = self._resizeMargin
        width = self.width()
        height = self.height()

        zones = self._resizeZones

        zones["top"].setGeometry(margin, 0, width - 2 * margin, margin)
        zones["bottom"].setGeometry(margin, height - margin, width - 2 * margin, margin)
        zones["left"].setGeometry(0, margin, margin, height - 2 * margin)
        zones["right"].setGeometry(width - margin, margin, margin, height - 2 * margin)

        zones["top_left"].setGeometry(0, 0, margin, margin)
        zones["top_right"].setGeometry(width - margin, 0, margin, margin)
        zones["bottom_left"].setGeometry(0, height - margin, margin, margin)
        zones["bottom_right"].setGeometry(width - margin, height - margin, margin, margin)

        enabled = self._resizeEnabled and not self._isMaximized

        for zone in zones.values():
            zone.setVisible(enabled)
            zone.raise_()

    def setResizeEnabled(self, enabled: bool):
        self._resizeEnabled = enabled
        self._updateResizeZones()

    def setWindowTitleText(self, title: str):
        self.setWindowTitle(title)
        self._titleLabel.setText(title)

    def setWindowIconImage(self, iconPath: str):
        self.setWindowIcon(QIcon(iconPath))

        pixmap = QPixmap(iconPath)
        if pixmap.isNull():
            return

        iconSize = int(self._titleIcon.height() * 0.75)

        self._titleIcon.setPixmap(
            pixmap.scaled(
                iconSize,
                iconSize,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def eventFilter(self, obj, event):
        if obj is self._titleBar:

            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self._dragOffset = (
                        event.globalPosition().toPoint()
                        - self.frameGeometry().topLeft()
                    )
                    return True

            elif event.type() == QEvent.MouseMove:
                if event.buttons() & Qt.LeftButton and self._dragOffset:

                    if self._isMaximized:
                        self._toggleMaximize()
                        self._dragOffset = QPoint(self.width() // 2, 16)

                    self.move(
                        event.globalPosition().toPoint()
                        - self._dragOffset
                    )
                    return True

            elif event.type() == QEvent.MouseButtonRelease:
                self._dragOffset = None
                return True

            elif event.type() == QEvent.MouseButtonDblClick:
                if event.button() == Qt.LeftButton:
                    self._toggleMaximize()
                    return True

        return super().eventFilter(obj, event)

    def _toggleMaximize(self):
        screenGeometry = QApplication.primaryScreen().availableGeometry()

        if self._isMaximized:
            self.setGeometry(self._normalGeometry)
            self._btnMaximize.setText("\ue922")
            self._isMaximized = False
        else:
            self._normalGeometry = self.geometry()
            self.setGeometry(
                screenGeometry.x(),
                screenGeometry.y(),
                screenGeometry.width(),
                screenGeometry.height() - 1,
            )
            self._btnMaximize.setText("\ue923")
            self._isMaximized = True

        self._updateResizeZones()

    def _applyStyles(self):
        self.setStyleSheet("""
        QWidget[titleBar] {
            background: #181818;
        }

        QWidget[titleBar] QLabel {
            color: white;
        }

        QWidget[titleBar] QPushButton {
            border: none;
            background: transparent;
            color: white;
        }

        QWidget[titleBar] QPushButton:hover {
            background-color: rgba(255, 255, 255, 20);
        }

        QWidget[titleBar] QPushButton[closeButton]:hover {
            background-color: #E81123;
            color: white;
        }
        """)