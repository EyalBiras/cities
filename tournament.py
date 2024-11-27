import subprocess
import sys
from pathlib import Path
from tokenize import group

import numpy as np

from cities_game.capital_city import Capital
from cities_game.city import City
from cities_game.engine import Engine
from cities_game.player import Player

BANNED_WORDS = ["os", "Engine", "open", "open(", "pathlib", "sys"]
NEEDED_WORDS_FOR_MAIN = ["class MyBot(Bot):"]
GROUPS = Path("groups")




def validate_file(file: Path) -> bool:
    if file.name == "main.py":
        with open(file, "r") as f:
            contents = f.read()
            for word in NEEDED_WORDS_FOR_MAIN:
                if word not in contents:
                    return False

    with open(file, "r") as f:
        contents = f.read()
        for word in BANNED_WORDS:
            if word in contents:
                return False
    return True

def validate_group(group: Path) -> bool:
    print(list(group.rglob("*")))
    print(Path(list(group.rglob("*"))[0]).name)
    files = [Path(file).name for file in group.rglob("*")]
    for file in files:
        if not validate_file(group / files[0]):
            return False
    return True

def run_game(group1: Path, group2: Path):
    with open(f"{group1.name}-{group2.name}.py", "w") as f:
        f.write("from cities_game.engine import Engine\n")
        f.write("from utils import reset_game\n")
        f.write("from utils import images_to_video_from_objects\n")
        f.write(f"import groups.{group1.name}.main as {group1.name}\n")
        f.write(f"import groups.{group2.name}.main as {group2.name}\n")
        f.write(f"\n")
        f.write(f"p1, p2 = reset_game()\n")
        f.write(f"e = Engine(p1,{group1.name}.MyBot(),'{group1.name}', p2,{group2.name}.MyBot(), '{group2.name}')\n")
        f.write(f"game = e.play()\n")
        f.write(f"print('hello')\n")
        f.write(f"images_to_video_from_objects(game, r'games\{group1.name} vs {group2.name}.mp4')")
    subprocess.run([sys.executable, f"{group1.name}-{group2.name}.py"])

def run_tournament():
    groups = [Path(file).name for file in GROUPS.glob("*")]
    for i, group in enumerate(groups):
        for group2 in groups[i+1:]:
            print(f"{group} vs {group2}")
            run_game(Path(f"groups/{group}"), Path(f"groups/{group2}"))

    print(list(GROUPS.glob("*")))

if __name__ == '__main__':
    run_tournament()
