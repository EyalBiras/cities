import json
from pathlib import Path
from typing import Any

from models import Group
BASE_PATH = Path("../groups")
GROUPS_DB_SAVE_FILE = Path("../dbs/groups_db.json")
USERS_DB_SAVE_FILE = Path("../dbs/users_db.json")


def load_users_db() -> dict[str, dict[str, Any]]:
    with open(USERS_DB_SAVE_FILE) as f:
        return json.load(f)


def load_groups_db() -> list[Group]:
    with open(GROUPS_DB_SAVE_FILE) as f:
        groups = json.load(f)
    return [Group(**group) for group in groups]


users_db = load_users_db()

def set_user(username: str, hashed_password: str):
    users_db[username] = {
        "username": username,
        "group": None,
        "hashed_password": hashed_password,
        "disabled": False,
    }

def get_user(username: str):
    return users_db[username]

groups_db: list[Group] = load_groups_db()

def get_group_by_name(group_name):
    for group in groups_db:
        if group.name == group_name:
            return group


def save_users_db() -> None:
    with open(USERS_DB_SAVE_FILE, 'w') as f:
        json.dump(users_db, f, indent=2)


def save_groups_db() -> None:
    groups = [group.model_dump(mode="json") for group in groups_db]
    with open(GROUPS_DB_SAVE_FILE, 'w') as f:
        json.dump(groups, f, indent=2)

def get_group_directory(group: str) -> Path:
    return BASE_PATH / Path(group)