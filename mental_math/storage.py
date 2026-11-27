"""Small, portable JSON storage for preferences and personal records."""

import json
import os
from pathlib import Path
import sys


DEFAULT_SETTINGS = {
    "language": "English",
    "shake_on_mistake": True,
    "music_enabled": False,
    "fsu_hints": True,
}


def data_directory() -> Path:
    """Return the conventional per-user data directory for this app."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    target = base / "MentalMathTrainer"
    target.mkdir(parents=True, exist_ok=True)
    return target


def _read_json(name: str, fallback: dict) -> dict:
    try:
        with (data_directory() / name).open("r", encoding="utf-8") as file:
            value = json.load(file)
        return value if isinstance(value, dict) else fallback.copy()
    except (OSError, json.JSONDecodeError):
        return fallback.copy()


def _write_json(name: str, value: dict) -> None:
    path = data_directory() / name
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_settings() -> dict:
    settings = DEFAULT_SETTINGS.copy()
    stored = _read_json("settings.json", {})
    settings.update({key: stored[key] for key in settings.keys() & stored.keys()})
    if settings["language"] not in {"English", "Russian", "Kazakh"}:
        settings["language"] = "English"
    settings["shake_on_mistake"] = bool(settings["shake_on_mistake"])
    settings["music_enabled"] = bool(settings["music_enabled"])
    return settings


def save_settings(settings: dict) -> None:
    _write_json("settings.json", {key: settings.get(key, default) for key, default in DEFAULT_SETTINGS.items()})


def load_stats() -> dict:
    stats = _read_json("records.json", {})
    bests = stats.get("best_scores", {})
    if not isinstance(bests, dict):
        bests = {}

    def nonnegative_int(value) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

    return {
        "best_scores": {str(key): nonnegative_int(value) for key, value in bests.items()},
        "games_played": nonnegative_int(stats.get("games_played", 0)),
        "correct_total": nonnegative_int(stats.get("correct_total", 0)),
        "curriculum_topic": str(stats.get("curriculum_topic", "bonds_10")),
        "mastered_topics": [str(item) for item in stats.get("mastered_topics", []) if isinstance(item, str)],
        "topic_records": stats.get("topic_records", {}) if isinstance(stats.get("topic_records", {}), dict) else {},
    }


def record_session(level: str, score: int) -> dict:
    stats = load_stats()
    score = max(0, int(score))
    bests = stats["best_scores"]
    bests[level] = max(score, bests.get(level, 0))
    stats["games_played"] += 1
    stats["correct_total"] += score
    _write_json("records.json", stats)
    return stats


def save_curriculum(topic_id: str, mastered_topics: list[str], topic_records: dict) -> dict:
    """Persist the learner's automatic curriculum position and mastery data."""
    stats = load_stats()
    stats["curriculum_topic"] = topic_id
    stats["mastered_topics"] = list(dict.fromkeys(mastered_topics))
    stats["topic_records"] = topic_records
    _write_json("records.json", stats)
    return load_stats()
