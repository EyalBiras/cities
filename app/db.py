from app.models import Group

users_db = {
    "Admin": {
        "username": "Admin",
        "group": None,
        "hashed_password": "$2b$12$LI728mCmmOOwQlK8uRDE2.U95kvtdIv/SSYWNfHI.bO5HOQ3ZnJ4K",
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