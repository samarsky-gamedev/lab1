"""Консольное меню. Запуск: python main.py."""

from models import Course, Person, Student, Teacher
from university import University, UniversityError


def read_item(kind: str) -> Person | Course:
    name = input("Имя или название: ")
    if kind == "students":
        return Student(name, input("Группа: "))
    if kind == "teachers":
        return Teacher(name, input("Кафедра: "))
    hours = int(input("Количество часов: "))
    teacher_id = int(input("ID преподавателя: "))
    return Course(name, hours, teacher_id)


def main() -> None:
    university = University()
    sections = {"1": "students", "2": "teachers", "3": "courses"}
    print("Университет. Данные хранятся в памяти до завершения программы.")
    while True:
        try:
            print("\n1 — Студенты; 2 — Преподаватели; 3 — Курсы; 0 — Выход")
            choice = input("Раздел: ").strip()
            if choice == "0":
                break
            kind = sections[choice]
            print("1 — Список; 2 — Добавить; 3 — Изменить; 4 — Удалить")
            action = input("Действие: ").strip()
            if action == "1":
                records = university.list_records(kind)
                if not records:
                    print("Нет записей.")
                for record_id, item in records:
                    print(f"{record_id}: {item}")
            elif action in ("2", "3", "4"):
                record_id = int(input("ID: "))
                if action == "2":
                    university.add(kind, record_id, read_item(kind))
                elif action == "3":
                    university.get(kind, record_id)
                    university.update(kind, record_id, read_item(kind))
                else:
                    university.delete(kind, record_id)
                print("Готово.")
            else:
                print("Неизвестное действие.")
        except (UniversityError, ValueError, TypeError) as error:
            print(f"Ошибка: {error}")
        except KeyError:
            print("Неизвестный раздел.")
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена.")
            break


if __name__ == "__main__":
    main()
