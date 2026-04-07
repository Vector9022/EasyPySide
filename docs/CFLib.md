## `File.Exists` 📝 Функция для проверки существует ли файл. [[Назад](Main.md)]

### ⚙️ Параметры
- `return`[bool] - Возвращает значение True если файл существует или False если его нет.

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

isExists = cfg.File.Exists()
```
<hr><br>



## `File.Create` 📝 Функция создает файл если ево нет. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

cfg.File.Create()
```
<hr><br>



## `File.Delete` 📝 Функция удаляет файл если он есть. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

cfg.File.Delete()
```
<hr><br>



## `File.Update` 📝 Функция обновляет содержимое файла если он есть. [[Назад](Main.md)]

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

cfg.File.Update()
```
<hr><br>



## `Params.Set` 📝 Функция создает или изменяет значения параметров. [[Назад](Main.md)]

### ⚙️ Параметры
- `key`[str] - Имя параметра.
- `Value`[str] - Новое значение.
- `preComment`[str] - Новый комментарий.
- `postComment`[str] - Новый комментарий.
- `Tags`[str] - Новые теги.

> ### 💡 Примечание
> Если не указать новое значение для `Value`, `preComment`, `postComment`, `Tags` их значения не изменятся.

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

cfg.Params.Set("test") # Создает параметр если его нету
cfg.Params.Set("test", Value="Hello") # Обновляет значение по ключу если переменная еще не создана она создается с указанным значением.
```
<hr><br>



## `Params.Delete` 📝 Функция удаляет параметр если он есть. [[Назад](Main.md)]

### ⚙️ Параметры
- `key`[str] - Имя параметра.

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

cfg.Params.Delete("test")
```
<hr><br>



## `Params.Exists` 📝 Функция для проверки существует ли параметр. [[Назад](Main.md)]

### ⚙️ Параметры
- `key`[str] - Имя параметра.
- `return`[bool] - Возвращает значение True если параметр существует или False если его нет.

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

isExists = cfg.Params.Exists("test")
```
<hr><br>



## `Params.Get` 📝 Функция для получения параметра по ключу. [[Назад](Main.md)]

### ⚙️ Параметры
- `key`[str] - Имя параметра.
- `return`[dict or None] - Возвращает dict если параметр существует или None если его нет.

### 🔍 Пример использования
```python
import localLib.CFLib as CFLib

cfg = CFLib.Config("config.cfg")

testParam = cfg.Params.Get("test")
```
<hr><br>