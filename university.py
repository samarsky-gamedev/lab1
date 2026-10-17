"""Общие CRUD-операции над студентами, преподавателями и курсами."""

from models import Course, Person, Student, Teacher, check_number

TYPES = {"students": Student, "teachers": Teacher, "courses": Course}


class University:
    def __init__(self) -> None:
        self._records: dict[str, dict[int, Person | Course]] = {
            kind: {} for kind in TYPES
        }

    def add(self, kind: str, record_id: int, item: Person | Course) -> None:
        check_number(record_id)
        if not isinstance(item, TYPES[kind]):
            raise TypeError("Тип объекта не соответствует разделу.")
        if record_id in self._records[kind]:
            raise ValueError("Этот ID уже занят.")
        self._records[kind][record_id] = item

    def get(self, kind: str, record_id: int) -> Person | Course:
        return self._records[kind][record_id]

    def list_records(self, kind: str) -> list[tuple[int, Person | Course]]:
        return list(self._records[kind].items())

    def update(self, kind: str, record_id: int,
               item: Person | Course) -> None:
        self.get(kind, record_id)
        if not isinstance(item, TYPES[kind]):
            raise TypeError("Тип объекта не соответствует разделу.")
        self._records[kind][record_id] = item

    def delete(self, kind: str, record_id: int) -> None:
        del self._records[kind][record_id]
