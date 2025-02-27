import sqlite3 as sql
import threading
from GUI.db.group import Group
from GUI.db.hash_utils import hash_password

admin_username = "admin"
admin_password = "admin"

NO_GROUP = "none"


class DB:
    def __init__(self):
        self.lock = threading.Lock()
        self.connection = sql.connect("Users.db", check_same_thread=False)
        with self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, user_group TEXT, is_owner INTEGER, join_request TEXT)")
            self.connection.execute(
                "INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES(?, ?, ?, ?, ?)",
                (admin_username, admin_password, 'MegaKnight', 1, NO_GROUP))
            self.connection.execute(
                "INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES(?, ?, ?, ?, ?)",
                ('a1', 'b', NO_GROUP, 0, NO_GROUP))
            self.connection.execute(
                "INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES(?, ?, ?, ?, ?)",
                ('a2', 'b', 'Castli', 1, NO_GROUP))
            self.connection.execute(
                "INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES(?, ?, ?, ?, ?)",
                ('a3', 'b', NO_GROUP, 0, 'MegaKnight'))
            self.connection.execute(
                "INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES(?, ?, ?, ?, ?)",
                ('a5', 'b', NO_GROUP, 0, 'MegaKnight'))

    def execute_query(self, query: str, params: tuple = ()):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor

    def validate_user(self, username: str, password: str) -> bool:
        hashed_password = hash_password(password)
        cursor = self.execute_query("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        return cursor.fetchone() is not None

    def signup_user(self, username: str, password: str) -> bool:
        cursor = self.execute_query("SELECT username FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            return False
        self.execute_query("INSERT INTO users VALUES(?, ?, ?, ?, ?)",
                           (username, hash_password(password), NO_GROUP, 0, NO_GROUP))
        return True

    def create_group(self, username: str, group_name: str) -> None:
        self.execute_query("UPDATE users SET user_group = ?, is_owner = 1, join_request = ? WHERE username = ?",
                           (group_name, NO_GROUP, username))

    def is_in_group(self, username: str) -> bool:
        cursor = self.execute_query("SELECT user_group FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        return user is not None and user[0] != NO_GROUP

    def is_group_owner(self, username: str) -> bool:
        cursor = self.execute_query("SELECT is_owner FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        return user is not None and bool(user[0])

    def leave_group(self, username: str) -> None:
        self.execute_query("UPDATE users SET user_group = ?, is_owner = 0, join_request = ? WHERE username = ?",
                           (NO_GROUP, NO_GROUP, username))

    def get_groups(self) -> list[Group]:
        cursor = self.execute_query("SELECT username, user_group, is_owner FROM users")
        groups_dict = {}
        for user, group, is_owner in cursor.fetchall():
            if group != NO_GROUP:
                if group not in groups_dict:
                    groups_dict[group] = ([], None)
                groups_dict[group][0].append(user)
                if is_owner:
                    groups_dict[group] = (groups_dict[group][0], user)

        return [Group(name, members, owner) for name, (members, owner) in groups_dict.items()]

    def ask_for_join_request(self, username: str, group_name: str) -> bool:
        cursor = self.execute_query("SELECT 1 FROM users WHERE user_group=?", (group_name,))
        if cursor.fetchone() is None:
            return False
        self.execute_query("UPDATE users SET join_request = ? WHERE username = ?", (group_name, username))
        return True

    def get_join_requests(self, username: str) -> list[str]:
        cursor = self.execute_query("SELECT user_group, is_owner FROM users WHERE username=?", (username,))
        owner = cursor.fetchone()
        if not owner or not owner[1]:
            return []

        cursor = self.execute_query("SELECT username FROM users WHERE join_request=?", (owner[0],))
        return [user[0] for user in cursor.fetchall()]

    def accept_join_request(self, username: str, accepted_user: str) -> bool:
        cursor = self.execute_query("SELECT user_group FROM users WHERE username=?", (username,))
        owner = cursor.fetchone()
        if not owner:
            return False

        cursor = self.execute_query("SELECT join_request FROM users WHERE username=?", (accepted_user,))
        user_joiner = cursor.fetchone()
        if not user_joiner or user_joiner[0] != owner[0]:
            return False

        self.execute_query("UPDATE users SET join_request = ?, user_group = ? WHERE username = ?",
                           (NO_GROUP, owner[0], accepted_user))
        return True

    def get_group(self, username: str) -> Group:
        cursor = self.execute_query("SELECT user_group FROM users WHERE username=?", (username,))
        user_group = cursor.fetchone()
        if not user_group or user_group[0] == NO_GROUP:
            return Group(NO_GROUP, [], "")

        cursor = self.execute_query("SELECT username, is_owner FROM users WHERE user_group=?", (user_group[0],))
        members = []
        owner = ""
        for user, is_owner in cursor.fetchall():
            members.append(user)
            if is_owner:
                owner = user

        return Group(user_group[0], members, owner)

    def is_asking_for_join_request(self, requester: str, username: str) -> bool:
        cursor = self.execute_query("SELECT user_group, is_owner FROM users WHERE username=?", (username,))
        owner = cursor.fetchone()
        if not owner or not owner[1]:
            return False

        cursor = self.execute_query("SELECT join_request FROM users WHERE username=?", (requester,))
        request = cursor.fetchone()
        return request is not None and request[0] == owner[0]