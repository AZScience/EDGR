"""
Realtime IDS alert ingest (Suricata eve.json–style) for the Step-16 app.

No ML training: alerts are normalized to a CTI query string, then EDGR runs live.
"""

from __future__ import annotations

import json
import threading
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Any

_MAX_ALERTS = 200
_lock = threading.Lock()
_alerts: deque[dict[str, Any]] = deque(maxlen=_MAX_ALERTS)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_list(payload: Any) -> list[dict[str, Any]]:
    """Accept one object, a list, or NDJSON string-like structures."""
    if payload is None:
        return []
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        # Suricata bulk wrapper or single event
        if isinstance(payload.get("events"), list):
            return [x for x in payload["events"] if isinstance(x, dict)]
        if isinstance(payload.get("alerts"), list):
            return [x for x in payload["alerts"] if isinstance(x, dict)]
        return [payload]
    return []


def alert_to_query(raw: dict[str, Any]) -> str:
    """Map Suricata-style / generic alert JSON → analyst query for EDGR."""
    alert = raw.get("alert") if isinstance(raw.get("alert"), dict) else {}
    sig = (
        alert.get("signature")
        or raw.get("signature")
        or raw.get("msg")
        or raw.get("rule")
        or ""
    )
    category = alert.get("category") or raw.get("category") or ""
    severity = alert.get("severity") or raw.get("severity")
    proto = raw.get("proto") or raw.get("app_proto") or ""
    src = raw.get("src_ip") or raw.get("src") or raw.get("source_ip")
    dst = raw.get("dest_ip") or raw.get("dst") or raw.get("dest") or raw.get("destination_ip")
    sport = raw.get("src_port")
    dport = raw.get("dest_port") or raw.get("dst_port")

    meta = alert.get("metadata") if isinstance(alert.get("metadata"), dict) else {}
    tactics = meta.get("mitre_tactic_id") or meta.get("mitre_tactic") or []
    techniques = meta.get("mitre_technique_id") or meta.get("mitre_technique") or []
    if isinstance(tactics, str):
        tactics = [tactics]
    if isinstance(techniques, str):
        techniques = [techniques]

    # Also pull free-text fields often present in SOC tickets
    extra = raw.get("payload_printable") or raw.get("http") or ""
    if isinstance(extra, dict):
        extra = extra.get("url") or extra.get("hostname") or ""

    parts = [
        "IDS/NIDS alert triage:",
        f"signature={sig}" if sig else "signature=(unknown)",
    ]
    if category:
        parts.append(f"category={category}")
    if severity is not None:
        parts.append(f"severity={severity}")
    if proto:
        parts.append(f"proto={proto}")
    if src or dst:
        flow = f"{src or '?'}"
        if sport is not None:
            flow += f":{sport}"
        flow += f" -> {dst or '?'}"
        if dport is not None:
            flow += f":{dport}"
        parts.append(f"flow={flow}")
    if techniques:
        parts.append("ATT&CK techniques=" + ", ".join(str(x) for x in techniques))
    if tactics:
        parts.append("ATT&CK tactics=" + ", ".join(str(x) for x in tactics))
    if extra:
        parts.append(f"context={str(extra)[:200]}")

    parts.append(
        "Explain the likely intrusion behavior, map to ATT&CK/CVE when supported by evidence, "
        "and state what an analyst should verify next."
    )
    return " ".join(parts)


def normalize_alert(raw: dict[str, Any], *, source: str = "api") -> dict[str, Any]:
    alert = raw.get("alert") if isinstance(raw.get("alert"), dict) else {}
    aid = str(
        raw.get("id")
        or raw.get("alert_id")
        or f"alr_{uuid.uuid4().hex[:12]}"
    )
    query = alert_to_query(raw)
    return {
        "id": aid,
        "received_at": _now_iso(),
        "source": source,
        "event_type": raw.get("event_type") or "alert",
        "timestamp": raw.get("timestamp") or raw.get("time") or _now_iso(),
        "signature": alert.get("signature") or raw.get("signature") or raw.get("msg"),
        "severity": alert.get("severity") or raw.get("severity"),
        "category": alert.get("category") or raw.get("category"),
        "src_ip": raw.get("src_ip") or raw.get("src"),
        "dest_ip": raw.get("dest_ip") or raw.get("dst") or raw.get("dest"),
        "proto": raw.get("proto") or raw.get("app_proto"),
        "query": query,
        "raw": raw,
        "analyzed": False,
        "analysis_id": None,
    }


def ingest_alerts(
    payload: Any,
    *,
    source: str = "api",
) -> dict[str, Any]:
    rows = _as_list(payload)
    if not rows:
        raise ValueError(
            "Expected Suricata-style alert JSON object, list of events, or {alerts:[…]}"
        )
    accepted: list[dict[str, Any]] = []
    with _lock:
        for raw in rows:
            # Skip non-alert flow records unless they carry signature text
            et = str(raw.get("event_type") or "alert").lower()
            if et not in {"alert", "anomaly", "firewall", ""} and not (
                isinstance(raw.get("alert"), dict) or raw.get("signature") or raw.get("msg")
            ):
                continue
            item = normalize_alert(raw, source=source)
            _alerts.appendleft(item)
            accepted.append(item)
    if not accepted:
        raise ValueError("No alert-like events found in payload")
    return {
        "ok": True,
        "accepted": len(accepted),
        "alerts": [
            {k: v for k, v in a.items() if k != "raw"}
            for a in accepted
        ],
        "queue_size": len(_alerts),
        "note_vi": (
            "Alert đã vào hàng đợi realtime. Gọi analyze trên alert_id để chạy EDGR — không cần huấn luyện ML."
        ),
        "note_en": (
            "Alert queued in realtime. Call analyze on alert_id to run EDGR — no ML training required."
        ),
    }


def list_alerts(limit: int = 50) -> dict[str, Any]:
    limit = max(1, min(int(limit), _MAX_ALERTS))
    with _lock:
        items = list(_alerts)[:limit]
    return {
        "count": len(items),
        "queue_size": len(_alerts),
        "alerts": [{k: v for k, v in a.items() if k != "raw"} for a in items],
    }


def get_alert(alert_id: str) -> dict[str, Any] | None:
    with _lock:
        for a in _alerts:
            if a["id"] == alert_id:
                return a
    return None


def mark_analyzed(alert_id: str, analysis_ref: str | None = None) -> None:
    with _lock:
        for a in _alerts:
            if a["id"] == alert_id:
                a["analyzed"] = True
                a["analysis_id"] = analysis_ref or a["id"]
                a["analyzed_at"] = _now_iso()
                break


SAMPLE_SURICATA_ALERT: dict[str, Any] = {
    "timestamp": "2024-11-18T08:14:22.551221+0000",
    "event_type": "alert",
    "src_ip": "10.20.30.40",
    "src_port": 49152,
    "dest_ip": "10.20.30.55",
    "dest_port": 445,
    "proto": "TCP",
    "app_proto": "smb",
    "alert": {
        "action": "allowed",
        "gid": 1,
        "signature_id": 2100498,
        "rev": 5,
        "signature": "ET SCAN Possible SMB Lateral Movement",
        "category": "Potentially Bad Traffic",
        "severity": 2,
        "metadata": {
            "mitre_tactic_id": ["TA0008"],
            "mitre_technique_id": ["T1021.002"],
        },
    },
}


def sample_alert_payload() -> dict[str, Any]:
    return {
        "description_vi": "Mẫu Suricata eve.json (alert) — POST vào /api/app/alerts",
        "description_en": "Sample Suricata eve.json alert — POST to /api/app/alerts",
        "alert": SAMPLE_SURICATA_ALERT,
        "curl_example": (
            'curl -s -X POST http://127.0.0.1:8015/api/app/alerts '
            '-H "Content-Type: application/json" '
            f"-d '{json.dumps(SAMPLE_SURICATA_ALERT)}'"
        ),
    }
