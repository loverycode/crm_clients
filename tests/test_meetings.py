from datetime import date

from clients import Client
from meetings import Meeting, cancel_meeting, create_meeting, is_slot_available


def test_meeting_creation():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meeting = Meeting(1, client, "2026-09-15", "Обсуждение договора")
    assert meeting.id == 1
    assert meeting.client is client
    assert meeting.booking_date if False else meeting.meeting_date == (
        "2026-09-15"
    )
    assert not meeting.is_cancelled


def test_meeting_cancel_method():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meeting = Meeting(1, client, "2026-09-15")
    meeting.cancel()
    assert meeting.is_cancelled


def test_is_slot_available_empty():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meetings = []
    assert is_slot_available(meetings, client, date(2026, 9, 15))


def test_duplicate_meeting_forbidden():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meetings = []
    create_meeting(meetings, client, date(2026, 9, 15), "Договор")
    assert not is_slot_available(meetings, client, date(2026, 9, 15))


def test_create_meeting_conflict_raises():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meetings = []
    create_meeting(meetings, client, date(2026, 9, 15))
    try:
        create_meeting(meetings, client, date(2026, 9, 15))
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_cancel_meeting_frees_slot():
    client = Client(1, "Иван Петров", "+7-999-123-45-67")
    meetings = []
    meeting = create_meeting(meetings, client, date(2026, 9, 15))

    assert cancel_meeting(meetings, meeting.id)
    assert meeting.is_cancelled
    assert meeting in meetings  # объект остался в коллекции
    assert is_slot_available(meetings, client, date(2026, 9, 15))
