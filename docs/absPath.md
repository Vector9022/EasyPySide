## `absPath` 📝 Функция возвращает абсолютный путь к файлу. [[Назад](Main.md)]

### ⚙️ Параметры
- `path`[str] - Относительный путь к файлу.
- `return`[str] - Абсолютный путь к файлу.

> ### 💡 Примечание
> `absPath` возвращает абсолютный путь относительно корня проекта (ищет папку с нужным подкаталогом вверх от скрипта) тогда как `os.path.abspath` возвращает абсолютный путь от текущей рабочей директории.

### 🔍 Пример использования
```python
from localLib.absPath import absPath

result = absPath("resources\\terminalWhite.ico")
print(result) > "C:\Files\Projects\BasicPythonProject\resources\terminalWhite.ico"
```
<hr><br>