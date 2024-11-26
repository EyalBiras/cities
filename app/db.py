from app.models import Group

users_db = {
    "johndoe": {
        "username": "johndoe",
        "group": None,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False
    }
}

def set_user(username: str, hashed_password: str):
    users_db[username] = {
        "username": username,
        "group": None,
        "hashed_password": hashed_password,
        "disabled": False,
    }

def get_user(username: str):
    return users_db[username]

groups_db: list[Group] = []

def get_group_by_name(group_name):
    for group in groups_db:
        if group.name == group_name:
            return group