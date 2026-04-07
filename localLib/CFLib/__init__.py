import os
import re

class Config:
    def __init__(self, filePath: str):
        self._filePath = filePath

        self.File = self._File(self)
        self.Params = self._Params(self)

        self._variables: dict[str, dict] = self._parseToVariables()

    class _File:
        def __init__(self, cfg: "Config"):
            self._cfg = cfg

        def Exists(self) -> bool:
            return os.path.exists(self._cfg._filePath)

        def Create(self) -> None:
            if not self.Exists():
                content = self._cfg._buildFromVariables()
                with open(self._cfg._filePath, "w", encoding="utf-8") as f:
                    f.write(content)

        def Delete(self) -> None:
            if self.Exists():
                os.remove(self._cfg._filePath)

        def Update(self) -> None:
            """Пересобирает и сохраняет файл"""
            content = self._cfg._buildFromVariables()

            if self.Exists():
                with open(self._cfg._filePath, "w", encoding="utf-8") as f:
                    f.write(content)

    class _Params:
        def __init__(self, cfg: "Config"):
            self._cfg = cfg

        def Set(self, key: str, Value=None, preComment=None, postComment=None, Tags=None) -> None:
            """Создаёт или обновляет параметр"""

            vars = self._cfg._variables

            if key not in vars:
                vars[key] = {
                    "Value": "",
                    "preComment": "",
                    "postComment": "",
                    "Tags": "-formatSingleline",
                }

            if Value is not None:
                vars[key]["Value"] = Value

            if preComment is not None:
                vars[key]["preComment"] = preComment

            if postComment is not None:
                vars[key]["postComment"] = postComment

            if Tags is not None:
                vars[key]["Tags"] = Tags

        def Delete(self, key: str) -> None:
            if key in self._cfg._variables:
                del self._cfg._variables[key]

        def Exists(self, key: str) -> bool:
            return key in self._cfg._variables

        def Get(self, key: str) -> dict | None:
            return self._cfg._variables.get(key, None)

    def _parseToVariables(self) -> dict[str, dict]:
        """Парсит текст файла в variables"""

        if not self.File.Exists():
            return {}

        with open(self._filePath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        variables = {}

        currentComment = ""
        lastEmpty = False

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # пустая строка
            if not line:
                lastEmpty = True
                i += 1
                continue

            # комментарий
            if line.startswith("#"):
                currentComment = line[1:].strip()
                i += 1
                continue

            # ключ = значение
            match = re.match(r'"(.+?)"\s*=\s*(.+)', line)
            if not match:
                i += 1
                continue

            key, rest = match.groups()

            valueLines, postComment = self._readValue(lines, i, rest)
            rawValue = "\n".join(valueLines).strip()

            tag = self._detectFormatTag(rawValue)
            cleanValue = self._normalizeValue(rawValue)

            if lastEmpty and not currentComment:
                tag += " -gapBefore"

            variables[key] = {
                "Value": cleanValue,
                "preComment": currentComment,
                "postComment": postComment,
                "Tags": tag,
            }

            currentComment = ""
            lastEmpty = False
            i += len(valueLines)

        return variables

    def _readValue(self, lines, i, firstLine):
        """Читает значение"""
        valueLines = []
        postComment = ""

        if ";" in firstLine:
            value, *_ = firstLine.split(";")
            valueLines.append(value.strip())

            if "#" in firstLine:
                postComment = firstLine.split("#", 1)[1].strip()

        else:
            valueLines.append(firstLine)
            i += 1

            while i < len(lines):
                line = lines[i]

                if ";" in line:
                    value, *_ = line.split(";")
                    valueLines.append(value)

                    if "#" in line:
                        postComment = line.split("#", 1)[1].strip()
                    break

                valueLines.append(line)
                i += 1

        return valueLines, postComment

    def _detectFormatTag(self, val: str) -> str:
        """Определяет тип форматирования"""
        val = val.strip()

        if not (val.startswith("{") or val.startswith("[")):
            return "-formatSingleline"

        if "\n" not in val:
            return "-formatSingleline"

        if "{" in val[1:] or "[" in val[1:]:
            return "-formatExpanded"

        return "-formatMultiline"

    def _normalizeValue(self, raw: str) -> str:
        """Очищает значение"""
        val = " ".join(line.strip() for line in raw.splitlines())

        val = re.sub(r"\{\s+", "{", val)
        val = re.sub(r"\[\s+", "[", val)
        val = re.sub(r"\s+\}", "}", val)
        val = re.sub(r"\s+\]", "]", val)

        return val

    def _buildFromVariables(self) -> None:
        """Собирает _variables → текст файла"""

        lines = []

        for key, data in self._variables.items():
            value = self._formatValue(data["Value"], data["Tags"])

            # пустая строка перед блоком
            if lines and (data["preComment"] or "-gapBefore" in data["Tags"]):
                lines.append("")

            if data["preComment"]:
                lines.append(f"# {data['preComment']}")

            line = f'"{key}" = {value};'

            if data["postComment"]:
                line += f" # {data['postComment']}"

            lines.append(line)

        return "\n".join(lines).strip()

    def _formatValue(self, val: str, tag: str) -> str:
        """Форматирует значение по тегам"""
    
        if "-formatSingleline" in tag:
            return val
    
        def formatRecursive(v: str, indent: int = 2) -> str:
            """Рекурсивное форматирование значений"""
    
            v = v.strip()
    
            isObj = v.startswith("{") and v.endswith("}")
            isArr = v.startswith("[") and v.endswith("]")
    
            if not (isObj or isArr):
                return v
    
            inner = v[1:-1].strip()
            parts = self._smartSplit(inner) if inner else []
    
            indentStr = " " * indent
            nextIndentStr = " " * (indent + 2)
    
            formattedParts = []
    
            for p in parts:
                if isObj and ":" in p:
                    k, subV = p.split(":", 1)
                    subV = subV.strip()
    
                    formattedSub = formatRecursive(subV, indent + 2)
    
                    # если вложенный блок — переносим на новую строку
                    if formattedSub.startswith("{") or formattedSub.startswith("["):
                        formattedParts.append(
                            f"{k.strip()}: {formattedSub}"
                        )
                    else:
                        formattedParts.append(f"{k.strip()}: {formattedSub}")
                else:
                    formattedParts.append(formatRecursive(p, indent + 2))
    
            openBr = "{" if isObj else "["
            closeBr = "}" if isObj else "]"
    
            return (
                openBr + "\n"
                + nextIndentStr
                + (",\n" + nextIndentStr).join(formattedParts)
                + "\n"
                + indentStr
                + closeBr
            )
    
        # --- Multiline ---
        if "-formatMultiline" in tag:
            isObj = val.startswith("{") and val.endswith("}")
            isArr = val.startswith("[") and val.endswith("]")
    
            if not (isObj or isArr):
                return val
    
            inner = val[1:-1].strip()
            parts = self._smartSplit(inner) if inner else []
    
            openBr = "{" if isObj else "["
            closeBr = "}" if isObj else "]"
    
            return openBr + "\n  " + ",\n  ".join(parts) + "\n" + closeBr
    
        # --- Expanded (рекурсивный) ---
        if "-formatExpanded" in tag:
            return formatRecursive(val, 0)
    
        return val

    def _smartSplit(self, s: str):
        """Разбивает строку с учётом вложенности"""
        parts, current, depth = [], "", 0

        for ch in s:
            if ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1

            if ch == "," and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += ch

        if current.strip():
            parts.append(current.strip())

        return parts