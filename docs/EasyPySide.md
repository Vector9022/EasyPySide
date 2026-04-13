# `BaseWindow` 📝 Базовый шаблон окна. [[Назад](Main.md)]

> ### 💡 Примечание
> У шаблона окна есть `contentArea` именно сюда и нужно прикрепить все виджети

### 🔍 Пример использования
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

content = QVBoxLayout(window.contentArea)
content.setContentsMargins(10, 10, 10, 10)
content.addWidget(QLabel("Контент окна"))
content.addWidget(QPushButton("Кнопка"))
```

> ### 💡 Примечание
> У шаблона окна также есть `leftLayout`, `centerLayout` и `rightLayout` именно сюда и нужно прикрепить виджети если они должны бить в titleBar

### 🔍 Пример использования
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

window.leftLayout.addWidget(QLabel("left"))
window.centerLayout.addWidget(QLabel("center"))
window.rightLayout.addWidget(QLabel("right"))
```
<hr><br>



## `setResizeEnabled` 📝 Функция для изменения состояния Resize. [[Назад](Main.md)]

### ⚙️ Параметры
- `enabled`[bool] - Новое состояние Resize.

### 🔍 Пример использования
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

window.setResizeEnabled(False)
```
<hr><br>



## `setWindowTitleText` 📝 Функция для изменения текст заголовка окна. [[Назад](Main.md)]

### ⚙️ Параметры
- `title`[str] - Новий текст.

### 🔍 Пример использования
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

window.setWindowTitleText("Главное окно")
```
<hr><br>



## `setWindowIconImage` 📝 Функция для изменения изображение значка окна. [[Назад](Main.md)]

### ⚙️ Параметры
- `iconPath`[str] - Путь к иконке.

### 🔍 Пример использования
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

window.setWindowIconImage(r"resources\terminalWhite.ico")
```
<hr><br>