from datetime import date

from clients import Client


class Meeting:
    def __init__(
        self,
        meeting_id: int,
        client: Client,
        meeting_date: str,
        topic: str = "",
        is_cancelled: bool = False,
    ) -> None:
        self.id = meeting_id
        self.client = client
        self.meeting_date = meeting_date
        self.topic = topic
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"ID: {self.id}, Клиент: {self.client.name}, "
            f"Дата: {self.meeting_date}, Тема: {self.topic}, "
            f"Статус: {status}"
        )


def is_slot_available(
    meetings: list[Meeting],
    client: Client,
    meeting_date: date,
) -> bool:
    target = str(meeting_date)
    for m in meetings:
        if (
            m.client.id == client.id
            and m.meeting_date == target
            and not m.is_cancelled
        ):
            return False
    return True


def create_meeting(
    meetings: list[Meeting],
    client: Client,
    meeting_date: date,
    topic: str = "",
) -> Meeting:
    if not is_slot_available(meetings, client, meeting_date):
        raise ValueError("У клиента уже назначена встреча на эту дату")

    next_id = max((m.id for m in meetings), default=0) + 1
    meeting = Meeting(
        meeting_id=next_id,
        client=client,
        meeting_date=str(meeting_date),
        topic=topic,
    )
    meetings.append(meeting)
    return meeting


def cancel_meeting(meetings: list[Meeting], meeting_id: int) -> bool:
    for m in meetings:
        if m.id == meeting_id:
            m.cancel()
            return True
    return False


def get_meeting_status(is_available: bool) -> str:
    if is_available:
        return "Клиент свободен для встречи"
    return "Клиент уже занят в этот день"
