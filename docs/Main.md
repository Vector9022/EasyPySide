<h1 align="center">📘 Документация 📘</h1>

* [EasyPySide](EasyPySide.md) - Библиотека (набор шаблонов) для быстрого создания графического интерфейса пользователя.
  * [setResizeEnabled](EasyPySide.md#setresizeenabled--функция-для-изменения-состояния-resize-назад) - Функция для изменения состояния Resize.
  * [setWindowTitleText](EasyPySide.md#setwindowtitletext--функция-для-изменения-текст-заголовка-окна-назад) - Функция для изменения текст заголовка окна.
  * [setWindowIconImage](EasyPySide.md#setwindowiconimage--функция-для-изменения-изображение-значка-окна-назад) - Функция для изменения изображение значка окна.

> ### 💡 Примечание
> У шаблона окна есть `contentArea` именно сюда и нужно прикрепить все виджети

### 🔍 Пример
```python
from localLib.EasyPySide import BaseWindow

window = BaseWindow()

content = QVBoxLayout(window.contentArea)
content.setContentsMargins(10, 10, 10, 10)
content.addWidget(QLabel("Контент окна"))
content.addWidget(QPushButton("Кнопка"))
```
<hr><br>