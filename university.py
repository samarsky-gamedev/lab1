"""Общие CRUD-операции над студентами, преподавателями и курсами."""

from models import Course, Person, Student, Teacher, check_number

TYPES = {"students": Student, "teachers": Teacher, "courses": Course}


class UniversityError(Exception):
    """Нарушение правил работы с записями университета."""


class University:
    def __init__(self) -> None:
        self._records: dict[str, dict[int, Person | Course]] = {
            kind: {} for kind in TYPES
        }

    def add(self, kind: str, record_id: int, item: Person | Course) -> None:
        check_number(record_id)
        self._check_item(kind, item)
        if record_id in self._records[kind]:
            raise UniversityError("Этот ID уже занят.")
        self._records[kind][record_id] = item

    def _check_item(self, kind: str, item: Person | Course) -> None:
        if type(item) is not TYPES[kind]:
            raise TypeError("Тип объекта не соответствует разделу.")
        if isinstance(item, Course):
            self.get("teachers", item.teacher_id)

    def get(self, kind: str, record_id: int) -> Person | Course:
        check_number(record_id)
        if record_id not in self._records[kind]:
            raise UniversityError(f"В разделе {kind} нет ID {record_id}.")
        return self._records[kind][record_id]

    def list_records(self, kind: str) -> list[tuple[int, Person | Course]]:
        return list(self._records[kind].items())

    def update(self, kind: str, record_id: int,
               item: Person | Course) -> None:
        self.get(kind, record_id)
        self._check_item(kind, item)
        self._records[kind][record_id] = item

    def delete(self, kind: str, record_id: int) -> None:
        self.get(kind, record_id)
        if kind == "teachers":
            for course in self._records["courses"].values():
                if course.teacher_id == record_id:
                    raise UniversityError("Сначала удалите или измените курсы.")
        del self._records[kind][record_id]
