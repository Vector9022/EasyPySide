import os

def _findRootDir(target_folder: str) -> str:
    """
    Ищет вверх от текущего файла директорию,
    внутри которой есть подкаталог target_folder.
    Возвращает путь к найденной директории.
    """
    
    cur = os.path.dirname(os.path.abspath(__file__))

    while True:
        candidate = os.path.join(cur, target_folder)
        if os.path.isdir(candidate):
            return cur  # нашли папку, где есть нужный подкаталог

        parent = os.path.dirname(cur)
        if parent == cur:
            raise RuntimeError(f"Не удалось найти папку {target_folder!r} выше {__file__}") # дошли до корня файловой системы и так и не нашли

        cur = parent

def absPath(path: str) -> str:
    """ Вернуть абсолютный путь. """
    
    norm = path.replace("/", os.sep).replace("\\", os.sep).strip() # Нормализуем слэши под текущую ОС

    # Если путь уже абсолютный — просто нормализуем и вернём
    if os.path.isabs(norm):
        return os.path.abspath(norm)

    norm = norm.lstrip(os.sep) # Убираем ведущий слэш, чтобы os.path.join не выкинул базовую папку
    parts = norm.split(os.sep, 1) # Первая "папка" в относительном пути — наша целевая

    if len(parts) == 1:
        base_dir = os.path.dirname(os.path.abspath(__file__)) # Нет папок, только имя файла: считаем путь относительно папки с этим файлом
    else:
        target_folder = parts[0]
        base_dir = _findRootDir(target_folder)

    return os.path.join(base_dir, norm)