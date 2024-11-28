import subprocess
import sys
from pathlib import Path
import json

BANNED_WORDS = ["os", "Engine", "open", "open(", "pathlib", "sys", "eval"]
NEEDED_WORDS_FOR_MAIN = ["class MyBot(Bot):"]
GROUPS = Path("groups")

RESULTS_FILE = Path("results.json")

def reset_results(groups: list[str]) -> None:
    with open(RESULTS_FILE, "w") as f:
        results = {group: {"total score": 0,"wins": 0, "losses": 0, "draws": 0} for group in groups}
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
    game_path = Path(f"{group1.name}-{group2.name}.py")
    with open(game_path, "w") as f:
        f.write("from cities_game.engine import Engine\n")
        f.write("from utils import reset_game\n")
        f.write("from utils import images_to_video_from_objects\n")
        f.write(f"import groups.{group1.name}.main as {group1.name}\n")
        f.write(f"import groups.{group2.name}.main as {group2.name}\n")
        f.write(f"from pathlib import Path\n")
        f.write(f"import json\n")
        f.write(f"\n")
        f.write(f"RESULTS_FILE = Path('results.json')\n")
        f.write(f"\n")
        f.write(f"if __name__ == '__main__':\n")
        f.write(f"\tp1, p2 = reset_game()\n")
        f.write(f"\te = Engine(p1,{group1.name}.MyBot(),'{group1.name}', p2,{group2.name}.MyBot(), '{group2.name}')\n")
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
        f.write(f"\tgame_file = 'games\{group1.name} vs {group2.name}-winner-' + winner + '.mp4'\n")
        f.write(f"\timages_to_video_from_objects(game, game_file)")
    subprocess.run([sys.executable, game_path])
    game_path.unlink()


def run_tournament():
    groups = [Path(file).name for file in GROUPS.glob("*")]
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

