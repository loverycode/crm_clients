from datetime import date

from meetings import cancel_meeting, create_meeting, is_slot_available


def test_is_slot_available_empty():
    meetings = []
    assert is_slot_available(meetings, 1, date(2026, 9, 15))


def test_duplicate_meeting_forbidden():
    meetings = []
    create_meeting(meetings, 1, date(2026, 9, 15), "Обсуждение договора")
    assert not is_slot_available(meetings, 1, date(2026, 9, 15))


def test_create_meeting_conflict_raises():
    meetings = []
    create_meeting(meetings, 1, date(2026, 9, 15))
    try:
        create_meeting(meetings, 1, date(2026, 9, 15))
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_cancel_meeting():
    meetings = []
    meeting = create_meeting(meetings, 1, date(2026, 9, 15))
    assert cancel_meeting(meetings, meeting["id"])
    assert meetings == []
