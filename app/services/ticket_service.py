import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.utils.config import get_settings


class TicketService:
    def __init__(self, tickets_dir: Path | None = None):
        self.tickets_dir = tickets_dir or get_settings().tickets_dir
        self.tickets_dir.mkdir(parents=True, exist_ok=True)

    def save(self, payload: dict) -> str:
        ticket_id = f"ticket_{uuid4().hex[:10]}"
        payload = {"ticket_id": ticket_id, "created_at": datetime.now(timezone.utc).isoformat(), **payload}
        metadata_path = self.tickets_dir / f"{ticket_id}.json"
        response_path = self.tickets_dir / f"{ticket_id}.txt"
        metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        response_path.write_text(payload.get("response", ""), encoding="utf-8")
        return ticket_id
