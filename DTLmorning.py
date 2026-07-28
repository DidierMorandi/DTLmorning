"""Résumé matinal des dépôts Git locaux pour Windows.

Cette application est la réécriture native Python 3.12 de DTLmorning.ps1.
Elle ne lance ni PowerShell ni interpréteur de commandes.
"""

from __future__ import annotations

import argparse
import ctypes
import getpass
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Sequence


IGNORED_DIRECTORIES: Final = frozenset(
    {".git", "build", "dist", "__pycache__", "logs", "node_modules"}
)
DIALOG_TITLE: Final = "DTL Git du matin"
IDYES: Final = 6
MB_OK: Final = 0x00000000
MB_YESNO: Final = 0x00000004
MB_ICONQUESTION: Final = 0x00000020
MB_ICONWARNING: Final = 0x00000030
MB_SETFOREGROUND: Final = 0x00010000


@dataclass(frozen=True, slots=True)
class RepositoryAction:
    """Résumé des opérations nécessaires pour un dépôt."""

    name: str
    text: str
    ahead: int
    work_items: int


def application_directory() -> Path:
    """Retourne le dossier du script ou de l'exécutable PyInstaller."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def default_root() -> Path:
    """Retourne le dossier parent du dossier DTL Morning."""

    return application_directory().parent


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Lit les paramètres, avec des alias proches de l'ancien script."""

    parser = argparse.ArgumentParser(
        description="Affiche le bilan matinal des dépôts Git locaux."
    )
    parser.add_argument(
        "--root",
        "-Root",
        type=Path,
        default=default_root(),
        help="Dossier racine à analyser.",
    )
    parser.add_argument(
        "--user-name",
        "-UserName",
        default=os.environ.get("USERNAME") or getpass.getuser(),
        help="Nom affiché dans le message matinal.",
    )
    parser.add_argument(
        "--xampp-path",
        "-XamppPath",
        type=Path,
        default=None,
        help=(
            "Dossier contenant xampp-control.exe. Sans ce paramètre, "
            "DTL Morning recherche automatiquement XAMPP."
        ),
    )
    return parser.parse_args(argv)


def find_git_repositories(root: Path) -> list[Path]:
    """Découvre récursivement les dépôts Git sans parcourir les dossiers ignorés."""

    if not root.is_dir():
        return []

    repositories: list[Path] = []
    try:
        top_level = sorted(
            (entry for entry in root.iterdir() if entry.is_dir()),
            key=lambda path: path.name.casefold(),
        )
    except OSError:
        return repositories

    for directory in top_level:
        if directory.name.startswith(".") or directory.name in IGNORED_DIRECTORIES:
            continue
        _scan_directory(directory, repositories)
    return repositories


def _scan_directory(directory: Path, repositories: list[Path]) -> None:
    """Explore un sous-arbre et s'arrête à la racine de chaque dépôt trouvé."""

    try:
        if (directory / ".git").exists():
            repositories.append(directory)
            return

        children = sorted(
            (entry for entry in directory.iterdir() if entry.is_dir()),
            key=lambda path: path.name.casefold(),
        )
    except OSError:
        return

    for child in children:
        if child.name.startswith(".") or child.name in IGNORED_DIRECTORIES:
            continue
        _scan_directory(child, repositories)


def branch_ahead_behind(branch_line: str) -> tuple[int, int]:
    """Extrait les compteurs ahead/behind de la ligne de branche Git."""

    ahead_match = re.search(r"ahead\s+(\d+)", branch_line)
    behind_match = re.search(r"behind\s+(\d+)", branch_line)
    ahead = int(ahead_match.group(1)) if ahead_match else 0
    behind = int(behind_match.group(1)) if behind_match else 0
    return ahead, behind


def _hidden_process_options() -> dict[str, object]:
    """Empêche l'apparition d'une console pour les processus enfants Windows."""

    if os.name != "nt":
        return {}
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = 0
    return {"startupinfo": startup_info, "creationflags": 0x08000000}


def git_status(repository: Path) -> list[str] | None:
    """Exécute git status et retourne ses lignes, ou None en cas d'échec."""

    try:
        completed = subprocess.run(
            ["git", "-C", str(repository), "status", "--porcelain", "--branch"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            **_hidden_process_options(),
        )
    except OSError:
        return None
    if completed.returncode != 0 or not completed.stdout:
        return None
    return completed.stdout.splitlines()


def repository_action(repository: Path) -> RepositoryAction | None:
    """Construit le résumé d'action d'un dépôt Git."""

    status_lines = git_status(repository)
    if not status_lines:
        return None

    branch_line = next((line for line in status_lines if line.startswith("## ")), "")
    changes = [
        line for line in status_lines if not line.startswith("## ") and line.strip()
    ]
    ahead, behind = branch_ahead_behind(branch_line)

    untracked = sum(line.startswith("??") for line in changes)
    staged = sum(
        not line.startswith("??") and len(line) > 0 and line[0] != " "
        for line in changes
    )
    unstaged = sum(
        not line.startswith("??") and len(line) > 1 and line[1] != " "
        for line in changes
    )

    parts: list[str] = []
    if untracked or unstaged:
        count = untracked + unstaged
        label = "1 modification" if count == 1 else f"{count} modifications"
        parts.append(f"enregistrer {label}")
    if staged:
        label = (
            "1 changement prêt à valider"
            if staged == 1
            else f"{staged} changements prêts à valider"
        )
        parts.append(f"valider {label}")
    if behind:
        label = "1 commit distant" if behind == 1 else f"{behind} commits distants"
        parts.append(f"synchroniser {label}")
    if ahead:
        label = "1 commit sur GitHub" if ahead == 1 else f"{ahead} commits sur GitHub"
        parts.append(f"publier {label}")

    if not parts:
        return None
    name = repository.name
    return RepositoryAction(
        name=name,
        text=f"- {name} : {', '.join(parts)}",
        ahead=ahead,
        work_items=len(parts),
    )


def estimated_time(action_count: int) -> str:
    """Retourne l'estimation historique fondée sur le nombre de dépôts actifs."""

    if action_count == 0:
        return "0 minute"
    if action_count <= 3:
        return "moins de 5 minutes"
    if action_count <= 6:
        return "environ 10 minutes"
    return "un petit quart d'heure"


def build_message(user_name: str, actions: Sequence[RepositoryAction]) -> str:
    """Construit le texte de la boîte de dialogue matinale."""

    lines = [
        f"🐔 Bonjour {user_name} !",
        "",
        "J'ai vérifié tes dépôts Git pendant que tu prenais ton café.",
        "",
    ]
    if not actions:
        lines.extend(
            ["Tout est calme côté Git.", "", "Aucune action requise aujourd'hui."]
        )
    else:
        lines.extend(["À faire aujourd'hui :", ""])
        lines.extend(action.text for action in actions)
        lines.extend(["", f"Temps estimé : {estimated_time(len(actions))}"])

    lines.extend(
        [
            "",
            "Bonne journée !",
            "",
            "Apache ne semble pas démarré. Ouvrir le panneau XAMPP ?",
        ]
    )
    return os.linesep.join(lines)


def message_box(message: str, flags: int) -> int:
    """Affiche une boîte de dialogue Windows native."""

    if os.name != "nt":
        print(message)
        return 0
    return int(
        ctypes.windll.user32.MessageBoxW(
            None, message, DIALOG_TITLE, flags | MB_SETFOREGROUND
        )
    )


def logical_drive_roots() -> list[Path]:
    """Retourne les racines des lecteurs Windows actuellement disponibles."""

    if os.name != "nt":
        return []
    drive_mask = int(ctypes.windll.kernel32.GetLogicalDrives())
    return [
        Path(f"{chr(ord('A') + index)}:\\")
        for index in range(26)
        if drive_mask & (1 << index)
    ]


def xampp_candidate_directories(xampp_path: Path | None = None) -> list[Path]:
    """Construit la liste ordonnée et sans doublon des dossiers XAMPP possibles."""

    candidates: list[Path] = []
    if xampp_path is not None:
        candidates.append(xampp_path)

    for variable in ("XAMPP_HOME", "XAMPP_PATH"):
        if value := os.environ.get(variable):
            candidates.append(Path(value))

    app_directory = application_directory()
    candidates.extend((app_directory / "xampp", app_directory.parent / "xampp"))
    candidates.extend(root / "xampp" for root in logical_drive_roots())

    for variable in ("ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
        if value := os.environ.get(variable):
            candidates.append(Path(value) / "xampp")

    unique_candidates: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = os.path.normcase(os.path.abspath(candidate))
        if normalized not in seen:
            seen.add(normalized)
            unique_candidates.append(candidate)
    return unique_candidates


def find_xampp_directory(xampp_path: Path | None = None) -> Path | None:
    """Détecte le premier dossier contenant le panneau de contrôle XAMPP."""

    for candidate in xampp_candidate_directories(xampp_path):
        if (candidate / "xampp-control.exe").is_file():
            return candidate.resolve()
    return None


def open_xampp(xampp_path: Path | None = None) -> None:
    """Détecte et ouvre le panneau XAMPP, ou signale son absence."""

    detected_path = find_xampp_directory(xampp_path)
    if detected_path is None:
        searched_paths = os.linesep.join(
            f"- {candidate}" for candidate in xampp_candidate_directories(xampp_path)
        )
        message_box(
            "Impossible de trouver xampp-control.exe."
            f"{os.linesep}{os.linesep}Dossiers vérifiés :{os.linesep}{searched_paths}",
            MB_OK | MB_ICONWARNING,
        )
        return

    control_panel = detected_path / "xampp-control.exe"
    try:
        subprocess.Popen(
            [str(control_panel)],
            cwd=detected_path,
            close_fds=True,
        )
    except OSError as exc:
        message_box(
            f"Impossible d'ouvrir le panneau XAMPP : {exc}",
            MB_OK | MB_ICONWARNING,
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Analyse les dépôts, affiche le bilan et traite la réponse XAMPP."""

    arguments = parse_arguments(argv)
    repositories = find_git_repositories(arguments.root.resolve())
    actions = [
        action
        for repository in repositories
        if (action := repository_action(repository)) is not None
    ]
    answer = message_box(
        build_message(arguments.user_name, actions), MB_YESNO | MB_ICONQUESTION
    )
    if answer == IDYES:
        open_xampp(arguments.xampp_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
