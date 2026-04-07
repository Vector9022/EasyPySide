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