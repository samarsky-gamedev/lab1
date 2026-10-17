"""Люди и учебные курсы университета."""


def check_text(value: str) -> str:
    """Убирает крайние пробелы и проверяет обязательное поле."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Текстовое поле не должно быть пустым.")
    return value.strip()


def check_number(value: int) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError("Нужно целое положительное число.")
    return value


class Person:
    def __init__(self, name: str) -> None:
        self.name = check_text(name)

    def __str__(self) -> str:
        return self.name


class Student(Person):
    def __init__(self, name: str, group: str) -> None:
        super().__init__(name)
        self.group = check_text(group)

    def __str__(self) -> str:
        return f"{self.name}, группа {self.group}"


class Teacher(Person):
    def __init__(self, name: str, department: str) -> None:
        super().__init__(name)
        self.department = check_text(department)

    def __str__(self) -> str:
        return f"{self.name}, кафедра {self.department}"


class Course:
    def __init__(self, name: str, hours: int, teacher_id: int) -> None:
        self.name = check_text(name)
        self.hours = check_number(hours)
        self.teacher_id = check_number(teacher_id)

    def __str__(self) -> str:
        return (f"{self.name}, {self.hours} ч., "
                f"ID преподавателя: {self.teacher_id}")
