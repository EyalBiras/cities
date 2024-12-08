import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BANNED_WORDS = ["os", "Engine", "open", "open(", "pathlib", "sys", "eval", "TimeoutError"]
NEEDED_WORDS_FOR_MAIN = ["class MyBot(Bot):"]
GROUPS = Path("../groups")
TOURNAMENT_CODE_DIR = "tournament_code"
RESULTS_FILE = Path("../results.json")
EXCEPT_EXCEPTION_PATTERN = r"^\s*except\s+Exception\s*(?:as\s+\w+)?\s*:\s*$"


def is_python(file: Path) -> bool:
    if not file.is_file():
        return False
    return file.name.endswith(".py")


def reset_results(groups: list[str]) -> None:
    with open(RESULTS_FILE, "w") as f:
        results = {group: {"total score": 0, "wins": 0, "losses": 0, "draws": 0} for group in groups}
        json.dump(results, f, indent=2)


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

        lines = contents.splitlines()
        for line in lines:
            if re.match(EXCEPT_EXCEPTION_PATTERN, line):
                return False
    return True


def validate_group(group: Path) -> bool:
    files = [Path(file) for file in group.rglob("*") if is_python(file)]
    print(files)
    found_main = False
    for file in files:
        if file.name == "main.py":
            found_main = True
        if not validate_file(files[0]):
            return False
    return found_main


def battle(group: Path, enemy: Path, games_directory: str = "games") -> None:
    if not validate_group(group / "development_code") or not validate_group(enemy / TOURNAMENT_CODE_DIR):
        return

    game_path = Path(f"../{group.name}-{enemy.name}.py")
    with open(game_path, "w") as f:
        f.write("from cities_game.engine import Engine\n")
        f.write("from utils import reset_game\n")
        f.write("from utils import images_to_video\n")
        f.write(f"import groups.{group.name}.development_code.main as {group.name}\n")
        f.write(f"import groups.{enemy.name}.tournament_code.main as {enemy.name}\n")
        f.write(f"from pathlib import Path\n")
        f.write(f"\n")
        f.write(f"\n")
        f.write(f"if __name__ == '__main__':\n")
        f.write(f"\tp1, p2, neutral_player = reset_game()\n")
        f.write(
            f"\te = Engine(p1,{group.name}.MyBot(),'{group.name}', p2,{enemy.name}.MyBot(), '{enemy.name}', neutral_player)\n")
        f.write(f"\tgame, winner = e.play()\n")
        f.write(f"\n")
        f.write(f"\tgame_file = r'{games_directory}\\{group.name} vs {enemy.name}-winner-' + winner + '.mp4'\n")
        f.write(f"\timages_to_video(game, game_file)")
    subprocess.run([sys.executable, game_path])


def run_game(group1: Path, group2: Path, games_directory: str = "../games", code_directory: str = TOURNAMENT_CODE_DIR):
    game_path = Path(f"../{group1.name}-{group2.name}.py")
    with open(game_path, "w") as f:
        f.write("from cities_game.engine import Engine\n")
        f.write("from utils import reset_game\n")
        f.write("from utils import images_to_video\n")
        f.write(f"import groups.{group1.name}.{code_directory}.main as {group1.name}\n")
        f.write(f"import groups.{group2.name}.{code_directory}.main as {group2.name}\n")
        f.write(f"from pathlib import Path\n")
        f.write(f"import json\n")
        f.write(f"\n")
        f.write(f"RESULTS_FILE = Path('../results.json')\n")
        f.write(f"\n")
        f.write(f"if __name__ == '__main__':\n")
        f.write(f"\tp1, p2, neutral_player = reset_game()\n")
        f.write(
            f"\te = Engine(p1,{group1.name}.MyBot(),'{group1.name}', p2,{group2.name}.MyBot(), '{group2.name}', neutral_player)\n")
        f.write(f"\tgame, winner = e.play()\n")
        f.write(f"\twith open(RESULTS_FILE) as f:\n")
        f.write(f"\t\tresults = json.load(f)\n")
        f.write(f"\n")
        f.write(f"\tif winner == '{group1.name}':\n")
        f.write(f"\t\tresults['{group1.name}']['wins'] += 1\n")
        f.write(f"\t\tresults['{group2.name}']['losses'] += 1\n")
        f.write(f"\telif winner == '{group2.name}':\n")
        f.write(f"\t\tresults['{group2.name}']['wins'] += 1\n")
        f.write(f"\t\tresults['{group1.name}']['losses'] += 1\n")
        f.write(f"\telse:\n")
        f.write(f"\t\tresults['{group2.name}']['draws'] += 1\n")
        f.write(f"\t\tresults['{group1.name}']['draws'] += 1\n")
        f.write(f"\n")
        f.write(f"\twith open(RESULTS_FILE, 'w') as f:\n")
        f.write(f"\t\tjson.dump(results, f, indent=2)\n")
        f.write(f"\n")
        f.write(f"\tgame_file = '{games_directory}\\{group1.name} vs {group2.name}-winner-' + winner + '.mp4v'\n")
        f.write(f"\timages_to_video(game, game_file)")
    subprocess.run([sys.executable, game_path])
    game_path.unlink()


def move_development_to_tournament(group: str) -> None:
    shutil.copytree(Path(fr"..\groups\{group}\development_code"), fr"..\groups\{group}\{TOURNAMENT_CODE_DIR}",
                    dirs_exist_ok=True)


def run_tournament():
    t1 = time.perf_counter()
    groups = [Path(file).name for file in GROUPS.glob("*") if validate_group(Path(file / "development_code"))]
    for group in groups:
        move_development_to_tournament(group)
    reset_results(groups)
    for i, group in enumerate(groups):
        for group2 in groups[i + 1:]:
            print(f"{group} vs {group2}")
            run_game(Path(f"groups/{group}"), Path(f"groups/{group2}"))
    for group in groups:
        with open(RESULTS_FILE) as f:
            results = json.load(f)
        results[group]["total score"] = results[group]["wins"] + 0.5 * results[group]["draws"]
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    print(list(GROUPS.glob("*")))
    print(time.perf_counter() - t1)
