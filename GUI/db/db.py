import sqlite3 as sql

from GUI.db.group import Group
from GUI.db.hash_utils import hash_password
admin_username = "admin"
admin_password = "admin"

NO_GROUP = "none"
class DB:
    def __init__(self):
        self.connection = sql.connect("Users.db")
        self.connection.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, user_group TEXT, is_owner INTEGER, join_request TEXT)")
        self.connection.execute(f"INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES('{admin_username}', '{admin_password}', 'MegaKnight', '1', '{NO_GROUP}')")
        self.connection.execute(f"INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES('a1', 'b', '{NO_GROUP}', '0', '{NO_GROUP}')")
        self.connection.execute(f"INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES('a2', 'b', 'Castli', '1', '{NO_GROUP}')")

        self.connection.execute(f"INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES('a3', 'b', '{NO_GROUP}', '0', 'MegaKnight')")
        self.connection.execute(f"INSERT INTO users(username, password, user_group, is_owner, join_request) VALUES('a5', 'b', '{NO_GROUP}', '0', 'MegaKnight')")


        self.cursor = self.connection.cursor()
        print(self.cursor.execute("SELECT * FROM users").fetchall())

    def validate_user(self, username: str, password: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password =?", (username, hash_password(password)))
        if not self.cursor.fetchone(): 
            return False
        else:
            return True

    def signup_user(self, username: str, password: str) -> bool:
        self.cursor.execute("SELECT username FROM users WHERE username=?", (username, ))
        if self.cursor.fetchone() is not None:
            return False

        self.cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?)", (username, hash_password(password), NO_GROUP, 0, NO_GROUP))
        self.connection.commit()
        return True

    def create_group(self, username: str, group_name: str) -> None:
        self.cursor.execute(f"""
            UPDATE users 
            SET user_group = '{group_name}', is_owner = 1, join_request = '{NO_GROUP}'
            WHERE username = '{username}'
        """)

    def is_in_group(self, username: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        print(f"{user=}")
        if user is None:
            return False
        if user[2] == NO_GROUP:
            return False
        return True

    def is_group_owner(self, username: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user is None:
            return False
        if user[3]:
            return True
        return False

    def leave_group(self, username: str) -> None:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user is None:
            return
        self.cursor.execute(f"""
                    UPDATE users 
                    SET user_group = '{NO_GROUP}', is_owner = 0, join_request = '{NO_GROUP}'
                    WHERE username = '{username}'
                """)

    def get_groups(self) -> list[Group]:
        groups_dict = {}
        for user in self.cursor.execute("SELECT * FROM users").fetchall():
            if user[2] != NO_GROUP:
                if user[2] in groups_dict:
                    groups_dict[user[2]][0].append(user[0])
                else:
                    groups_dict[user[2]] = [[user[0]], None]
                if user[3]:
                    groups_dict[user[2]][1] = user[0]
        groups = []
        for group, members_owner in groups_dict.items():
            members, owner = members_owner[0], members_owner[1]
            groups.append(Group(group, members, owner))
        return list(groups)

    def ask_for_join_request(self, username: str, group_name: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE user_group=?", (group_name,))
        if self.cursor.fetchone() is None:
            return False
        self.cursor.execute(f"""
                    UPDATE users 
                    SET join_request = '{group_name}'
                    WHERE username = '{username}'
                """)
        return True

    def get_join_requests(self, username: str) -> list[str]:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        owner = self.cursor.fetchone()
        if owner is  None:
            return []
        if not owner[3]:
            return []
        join_requests = []
        for user in self.cursor.execute("SELECT * FROM users").fetchall():
            if user[4] == owner[2]:
                join_requests.append(user[0])
        return join_requests

    def accept_join_request(self, username: str, accepted_user: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (accepted_user,))
        user_joiner = self.cursor.fetchone()
        if user_joiner is None:
            return False
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        owner = self.cursor.fetchone()
        if not owner[3]:
            return False
        if user_joiner[4] != owner[2]:
            return False
        self.cursor.execute(f"""
                            UPDATE users 
                            SET join_request = '{NO_GROUP}', user_group = '{owner[2]}'
                            WHERE username = '{accepted_user}'
                        """)
        return True


    def get_group(self, username) -> Group:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_ = self.cursor.fetchone()
        if user_ is None:
            return
        if user_[2] == NO_GROUP:
            return Group(NO_GROUP, [], "")
        members = []
        owner = ""
        for user in self.cursor.execute("SELECT * FROM users").fetchall():
            if user[2] == user_[2]:
                members.append(user[0])
                if user[3]:
                    owner = user[0]
        return Group(user_[2], members, owner)

    def is_asking_for_join_request(self, requester:str, username: str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user is None:
            return False
        if not user[3]:
            return False
        if not user[2]:
            return False
        self.cursor.execute("SELECT * FROM users WHERE username=?", (requester,))
        request = self.cursor.fetchone()
        if request is None:
            return False
        if request[4] == user[2]:
            return True
        return False
