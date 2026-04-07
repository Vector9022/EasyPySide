# `DefaultMenu` 📝 Класс отвечающий за меню при взаимодействии с значком. [[Назад](Main.md)]



## `setStyleSheet` 📝 Функция для установки стиля в меню. [[Назад](Main.md)]

### ⚙️ Параметры
- `styleSheet`[str] - Cтили styleSheet.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

styleSheet = ...

trayIcon.menu.setStyleSheet() # Установит стандартный стиль
trayIcon.menu.setStyleSheet(styleSheet) # Установит заданный стиль
```
<hr><br>



## `addQAction` 📝 Функция для добавления пункта в меню. [[Назад](Main.md)]

### ⚙️ Параметры
- `text`[str] - Надпись на пункте.
- `callback`[callable] - Функция которую нужно вызывать при клике.
- `icon`[str] - Путь к иконки.
- `stayOpen`[bool] - Закривать ли меню при нажатии.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.menu.addQAction(
    "Action",
    callback=lambda a: print("Clicked:", a.text()),
    icon=absPath("resources\\terminalWhite.ico"),
    stayOpen=False
)
```
<hr><br>



## `addCheckableQAction` 📝 Функция для добавления проверяемого пункта в меню. [[Назад](Main.md)]

### ⚙️ Параметры
- `text`[str] - Надпись на пункте.
- `callback`[callable] - Функция которую нужно вызывать при клике.
- `checked`[bool] - Изначальное состояние нажатия.
- `stayOpen`[bool] - Закривать ли меню при нажатии.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.menu.addCheckableQAction(
    "Checkable Action",
    callback=lambda a: print("Clicked:", a.text()),
    checked=True,
    stayOpen=False
)
```
<hr><br>



## `addQActionGroup` 📝 Функция для добавления группы пунктов в меню. [[Назад](Main.md)]

### ⚙️ Параметры
- `items`[list of dictionaries] - Список пунктов.
- `callback`[callable] - Функция которую нужно вызывать при клике.
- `stayOpen`[bool] - Закривать ли меню при нажатии.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

def toggleTheme(action):
    print("Clicked:", action.text())

items = [
    {"text": "Light Theme"},
    {"text": "Dark Theme", "checked": True},
]

trayIcon.menu.addQActionGroup(
    items,
    callback=toggleTheme,
    stayOpen=True
)
```
<hr><br>



## `addSubMenu` 📝 Функция для добавления под меню. [[Назад](Main.md)]

### ⚙️ Параметры
- `text`[str] - Надпись на под меню.
- `icon`[str] - Путь к иконки.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

subMenu = trayIcon.menu.addSubMenu("subMenu")

subMenu.addQAction(
    "SubMenu Action",
    callback=lambda a: print("Clicked:", a.text()),
    stayOpen=False
)
```
<hr><br>



## `addSeparator` 📝 Функция для добавления разделителя в меню. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.menu.addSeparator()
```
<hr><br>



# `SystemTrayIcon` 📝 Класс отвечающий за создание и управление значком в системном трее. [[Назад](Main.md)]

### ⚙️ Параметры
- `iconPath`[str] - Путь к иконке.

### ⚙️ Дополнительные параметры класса
- `onLeftClick`[callable] - Какую функцию выполнить при клике левой кнопкой мыши.
- `onRightClick`[callable] - Какую функцию выполнить при клике правой кнопкой мыши.
- `onDoubleClick`[callable] - Какую функцию выполнить при двойном клике левой кнопкой мыши.
- `onMiddleClick`[callable] - Какую функцию выполнить при нажатии на колесико мыши.
- `menu`[class] - Класс Menu. По умолчанию используется DefaultMenu().
<hr><br>



## `show` 📝 Функция для отображения значка в системном трее. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.show()
```
<hr><br>



## `hide` 📝 Функция для скрытия значка в системном трее. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.hide()
```
<hr><br>



## `setIcon` 📝 Функция для изменения иконки значка в системном трее. [[Назад](Main.md)]

### ⚙️ Параметры
- `iconPath`[str] - Путь к файлу.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.setIcon(absPath("resources\\terminalBlack.ico"))
```
<hr><br>



## `setToolTip` 📝 Функция для изменения всплывающей подсказки значка в системном трее. [[Назад](Main.md)]

### ⚙️ Параметры
- `toolTip`[str] - Текст всплывающей подсказки.

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.setToolTip("BasicPythonProject")
```
<hr><br>



## `showMenu` 📝 Функция для вызова меню. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.PySideTray as PST

trayIcon = PST.SystemTrayIcon(absPath("resources\\terminalWhite.ico"))

trayIcon.showMenu()
```
<hr><br>