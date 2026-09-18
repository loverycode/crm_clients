from datetime import date


def is_slot_available(
    meetings: list[dict],
    client_id: int,
    meeting_date: date,
) -> bool:
    target = str(meeting_date)
    for m in meetings:
        if m["client_id"] == client_id and m["meeting_date"] == target:
            return False
    return True


def create_meeting(
    meetings: list[dict],
    client_id: int,
    meeting_date: date,
    topic: str = "",
) -> dict:
    """Создать новую встречу с клиентом.

    Проверяет доступность клиента и добавляет словарь встречи
    в список meetings. Бросает ValueError, если клиент уже занят
    на указанную дату.
    """
    if not is_slot_available(meetings, client_id, meeting_date):
        raise ValueError("У клиента уже назначена встреча на эту дату")

    next_id = max((m["id"] for m in meetings), default=0) + 1
    meeting = {
        "id": next_id,
        "client_id": client_id,
        "meeting_date": str(meeting_date),
        "topic": topic,
    }
    meetings.append(meeting)
    return meeting


def cancel_meeting(meetings: list[dict], meeting_id: int) -> bool:
    for i, m in enumerate(meetings):
        if m["id"] == meeting_id:
            del meetings[i]
            return True
    return False


def get_meeting_status(is_available: bool) -> str:
    if is_available:
        return "Клиент свободен для встречи"
    return "Клиент уже занят в этот день"
