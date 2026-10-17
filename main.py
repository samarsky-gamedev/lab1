"""ЛР 1, вариант 12: университет. Запуск: python main.py (Python 3.10+)."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def text(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Текстовое поле не должно быть пустым.")
    return value.strip()


def number(value: int) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError("Нужно целое положительное число.")
    return value


class Person:
    def __init__(self, name: str) -> None:
        self.name = text(name)


class Student(Person):
    def __init__(self, name: str, group: str) -> None:
        super().__init__(name)
        self.group = text(group)

    def __str__(self) -> str:
        return f"{self.name}, группа {self.group}"


class Teacher(Person):
    def __init__(self, name: str, department: str) -> None:
        super().__init__(name)
        self.department = text(department)

    def __str__(self) -> str:
        return f"{self.name}, кафедра {self.department}"


class Course:
    def __init__(self, name: str, hours: int, teacher_id: int) -> None:
        self.name = text(name)
        self.hours = number(hours)
        self.teacher_id = number(teacher_id)

    def __str__(self) -> str:
        return f"{self.name}, {self.hours} ч., преподаватель {self.teacher_id}"


class UniversityError(Exception):
    """Неверный ID, связь или структура данных."""


TYPES = {"students": Student, "teachers": Teacher, "courses": Course}


class University:
    def __init__(self) -> None:
        self._records: dict[str, dict[int, Person | Course]] = {
            kind: {} for kind in TYPES
        }

    def list_records(self, kind: str) -> list[tuple[int, Person | Course]]:
        return list(self._records[kind].items())

    def get(self, kind: str, record_id: int) -> Person | Course:
        if number(record_id) not in self._records[kind]:
            raise UniversityError("Запись с таким ID не найдена.")
        return self._records[kind][record_id]

    def put(self, kind: str, record_id: int, item: Person | Course,
            replace: bool = False) -> None:
        """Добавление; при replace=True — изменение существующей записи."""
        exists = number(record_id) in self._records[kind]
        if exists != replace:
            raise UniversityError("ID занят." if exists else "ID не найден.")
        if type(item) is not TYPES[kind]:
            raise TypeError("Тип объекта не соответствует разделу.")
        if isinstance(item, Course):
            self.get("teachers", item.teacher_id)
        self._records[kind][record_id] = item

    def delete(self, kind: str, record_id: int) -> None:
        self.get(kind, record_id)
        if kind == "teachers" and any(c.teacher_id == record_id
                                     for _, c in self.list_records("courses")):
            raise UniversityError("Сначала удалите или измените курсы.")
        del self._records[kind][record_id]

    def save(self, path: str) -> None:
        data = {kind: [{"id": i, **vars(item)} for i, item in rows.items()]
                for kind, rows in self._records.items()}
        if Path(path).suffix.lower() == ".json":
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        elif Path(path).suffix.lower() == ".xml":
            root = ET.Element("university")
            for kind, rows in data.items():
                section = ET.SubElement(root, kind)
                for row in rows:
                    record = ET.SubElement(section, "record")
                    for key, value in row.items():
                        ET.SubElement(record, key).text = str(value)
            ET.indent(root)
            ET.ElementTree(root).write(path, encoding="utf-8",
                                       xml_declaration=True)
        else:
            raise ValueError("Нужно расширение .json или .xml.")

    def load(self, path: str) -> None:
        if Path(path).suffix.lower() == ".json":
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        elif Path(path).suffix.lower() == ".xml":
            root = ET.parse(path).getroot()
            if root.tag != "university" or len(root) != 3:
                raise UniversityError("Неверная структура XML.")
            data = {}
            for section in root:
                data[section.tag] = []
                for record in section:
                    row = {f.tag: f.text or "" for f in record}
                    if (record.tag != "record" or len(row) != len(record)
                            or any(len(f) for f in record)):
                        raise UniversityError("Неверная запись XML.")
                    for key in ("id", "hours", "teacher_id"):
                        if key in row:
                            row[key] = int(row[key])
                    data[section.tag].append(row)
        else:
            raise ValueError("Нужно расширение .json или .xml.")
        if not isinstance(data, dict) or set(data) != set(TYPES):
            raise UniversityError("Нужны students, teachers и courses.")
        loaded = University()  # Замена данных только после полной проверки.
        for kind in ("teachers", "students", "courses"):
            if not isinstance(data[kind], list):
                raise UniversityError("Раздел должен быть списком.")
            for row in data[kind]:
                if not isinstance(row, dict) or "id" not in row:
                    raise UniversityError("У записи должен быть ID.")
                fields = row.copy()
                record_id = fields.pop("id")
                loaded.put(kind, record_id, TYPES[kind](**fields))
        self._records = loaded._records


def read_item(kind: str) -> Person | Course:
    name = input("Имя или название: ")
    if kind == "students":
        return Student(name, input("Группа: "))
    if kind == "teachers":
        return Teacher(name, input("Кафедра: "))
    return Course(name, int(input("Часы: ")), int(input("ID преподавателя: ")))


def main() -> None:
    university = University()
    sections = {"1": "students", "2": "teachers", "3": "courses"}
    print("Университет. Перед выходом сохраните данные (пункт 5).")
    while True:
        try:
            print("\n1 Список; 2 Добавить; 3 Изменить; 4 Удалить")
            action = input("5 Сохранить; 6 Загрузить; 0 Выход: ").strip()
            if action == "0":
                break
            if action in ("5", "6"):
                path = input("Файл .json/.xml (загрузка с заменой): ").strip()
                if action == "5":
                    university.save(path)
                else:
                    university.load(path)
            elif action in ("1", "2", "3", "4"):
                key = input("1 Студенты; 2 Преподаватели; 3 Курсы: ").strip()
                kind = sections[key]
                if action == "1":
                    rows = university.list_records(kind)
                    print("\n".join(f"{i}: {obj}" for i, obj in rows)
                          or "Нет записей.")
                    continue
                record_id = int(input("ID: "))
                if action == "4":
                    university.delete(kind, record_id)
                else:
                    university.put(kind, record_id, read_item(kind),
                                   replace=action == "3")
            else:
                raise ValueError("Неизвестное действие.")
            print("Готово.")
        except (UniversityError, ValueError, TypeError, KeyError,
                OSError, ET.ParseError) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена.")
            break


if __name__ == "__main__":
    main()
