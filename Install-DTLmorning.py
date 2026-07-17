"""Installe l'application Python DTL Morning au démarrage de Windows.

L'installation et l'application matinale sont entièrement natives Python et
ne lancent jamais PowerShell.
"""

from __future__ import annotations

import ctypes
import json
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final


FALLBACK_DISPLAY_VERSION: Final = "v1.0-8"
WINDOW_TITLE: Final = "DTL Morning - Installation"
SHORTCUT_DESCRIPTION: Final = (
    "Lance DTL Morning au démarrage de la session Windows"
)


class Ansi:
    """Séquences ANSI utilisées par l'interface en mode console."""

    RESET = "\x1b[0m"
    BOLD_BRIGHT_WHITE = "\x1b[1;97m"
    GRAY = "\x1b[90m"
    GREEN = "\x1b[92m"
    CYAN = "\x1b[96m"
    YELLOW = "\x1b[93m"
    RED = "\x1b[91m"
    WHITE_ON_DARK_BLUE = "\x1b[37;44m"


@dataclass(frozen=True, slots=True)
class InstallerPaths:
    """Chemins employés par l'installateur."""

    install_dir: Path
    morning_application: Path
    readme: Path
    version_file: Path
    startup_folder: Path
    shortcut: Path


class InstallerError(RuntimeError):
    """Erreur fonctionnelle pouvant être présentée directement à l'utilisateur."""


def application_directory() -> Path:
    """Retourne le dossier du script ou de l'exécutable PyInstaller."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def require_windows() -> None:
    """Refuse une exécution sur un système autre que Windows."""

    if os.name != "nt":
        raise InstallerError("Cet installateur fonctionne uniquement sous Windows.")


def startup_directory() -> Path:
    """Obtient le dossier de démarrage de l'utilisateur via l'API Windows."""

    try:
        from win32com.shell import shell, shellcon
    except ImportError as exc:
        raise InstallerError(
            "La dépendance pywin32 est absente. "
            "Installez-la avec : python -m pip install -r requirements.txt"
        ) from exc

    try:
        value = shell.SHGetFolderPath(0, shellcon.CSIDL_STARTUP, 0, 0)
    except Exception as exc:
        raise InstallerError(
            "Impossible de déterminer le dossier de démarrage Windows."
        ) from exc

    if not value:
        raise InstallerError("Le dossier de démarrage Windows est introuvable.")
    return Path(value)


def build_paths() -> InstallerPaths:
    """Construit et centralise tous les chemins nécessaires."""

    install_dir = application_directory()
    startup_folder = startup_directory()
    executable = install_dir / "DTLmorning.exe"
    morning_application = (
        executable if executable.is_file() else install_dir / "DTLmorning.py"
    )
    return InstallerPaths(
        install_dir=install_dir,
        morning_application=morning_application,
        readme=install_dir / "README_Fr.md",
        version_file=install_dir / ".dtl_version",
        startup_folder=startup_folder,
        shortcut=startup_folder / "DTLmorning.lnk",
    )


def configure_console() -> bool:
    """Configure UTF-8, le titre et les couleurs ANSI de la console Windows."""

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    if os.name != "nt":
        return bool(sys.stdout.isatty())

    kernel32 = ctypes.windll.kernel32
    try:
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleTitleW(WINDOW_TITLE)
    except OSError:
        pass

    if not sys.stdout.isatty():
        return False

    stdout_handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    mode = ctypes.c_uint32()
    if stdout_handle in (0, -1):
        return False
    if not kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode)):
        return False
    return bool(kernel32.SetConsoleMode(stdout_handle, mode.value | 0x0004))


def colorize(text: str, color: str | None, use_color: bool) -> str:
    """Ajoute une couleur ANSI uniquement si la console la prend en charge."""

    if color and use_color:
        return f"{color}{text}{Ansi.RESET}"
    return text


def write(
    text: str = "",
    *,
    color: str | None = None,
    end: str = "\n",
    use_color: bool,
) -> None:
    """Écrit un texte éventuellement coloré et le rend immédiatement visible."""

    print(colorize(text, color, use_color), end=end, flush=True)


def clear_console(use_color: bool) -> None:
    """Efface la console sans lancer de processus externe."""

    if use_color and sys.stdout.isatty():
        print("\x1b[2J\x1b[H", end="", flush=True)
    else:
        print("\n" * 3, end="", flush=True)


def get_display_version(version_file: Path) -> str:
    """Lit ``display_version`` dans .dtl_version, avec repli sûr."""

    if not version_file.is_file():
        return FALLBACK_DISPLAY_VERSION
    try:
        metadata = json.loads(version_file.read_text(encoding="utf-8-sig"))
        display_version = metadata.get("display_version")
        if isinstance(display_version, str) and display_version.strip():
            return display_version.strip()
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
        pass
    return FALLBACK_DISPLAY_VERSION


def show_brand_header(paths: InstallerPaths, use_color: bool) -> None:
    """Affiche l'en-tête NetDTL de l'installateur."""

    clear_console(use_color)
    terminal_width = shutil.get_terminal_size(fallback=(77, 24)).columns
    width = max(76, min(terminal_width - 1, 120))

    version = get_display_version(paths.version_file)
    title = f"DTL Morning {version}".rstrip()
    subtitle = "Un outil de la suite NetDTL"
    logo = ("┌─┬─┬─┬─┬─┬─┐", "│N│e│t│D│T│L│", "└─┴─┴─┴─┴─┴─┘")
    gap = 3
    left_width = width - len(logo[0]) - gap

    title_line = title.ljust(left_width) + (" " * gap)
    subtitle_line = subtitle.ljust(left_width) + (" " * gap)
    website_line = "www.netdtl.com".ljust(left_width) + (" " * gap)

    write(
        title_line,
        color=Ansi.BOLD_BRIGHT_WHITE,
        end="",
        use_color=use_color,
    )
    write(logo[0], color=Ansi.WHITE_ON_DARK_BLUE, use_color=use_color)
    write(subtitle_line, color=Ansi.GRAY, end="", use_color=use_color)
    write(logo[1], color=Ansi.WHITE_ON_DARK_BLUE, use_color=use_color)
    write(website_line, color=Ansi.GRAY, end="", use_color=use_color)
    write(logo[2], color=Ansi.WHITE_ON_DARK_BLUE, use_color=use_color)
    write(use_color=use_color)
    write("Procédure d'installation automatique", use_color=use_color)
    write(use_color=use_color)
    write("=" * width, use_color=use_color)
    write(use_color=use_color)


def extract_help_section(readme: Path) -> list[str]:
    """Extrait la section « Pourquoi installer DTL Morning ? » du README."""

    try:
        lines = readme.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError as exc:
        raise InstallerError(f"README_Fr.md est introuvable : {readme}") from exc
    except (OSError, UnicodeError) as exc:
        raise InstallerError(f"Impossible de lire README_Fr.md : {exc}") from exc

    help_lines: list[str] = []
    in_install_section = False
    for line in lines:
        if line.strip() == "## Pourquoi installer DTL Morning ?":
            in_install_section = True
            continue
        if in_install_section and line.startswith("## "):
            break
        if in_install_section and not line.startswith("```"):
            help_lines.append(line.replace("`", "").replace("**", ""))
    return help_lines


def show_readme_help(paths: InstallerPaths, use_color: bool) -> None:
    """Affiche l'aide extraite du README français."""

    show_brand_header(paths, use_color)
    write(
        "AIDE (texte extrait du fichier README_Fr.md)",
        color=Ansi.CYAN,
        use_color=use_color,
    )
    write(use_color=use_color)

    try:
        help_lines = extract_help_section(paths.readme)
    except InstallerError as exc:
        write(str(exc), color=Ansi.YELLOW, use_color=use_color)
        return

    if not help_lines:
        write(
            "La section d'aide est absente de README_Fr.md.",
            color=Ansi.YELLOW,
            use_color=use_color,
        )
        return

    for line in help_lines:
        write(line, use_color=use_color)


def read_french_prompt(message: str) -> str:
    """Affiche une invite avec l'espace précédant les deux-points en français."""

    return input(f"{message} : ")


def wait_for_exit(message: str = "Appuyez sur <Entrée> pour quitter") -> None:
    """Attend une validation de l'utilisateur avant de fermer la console."""

    print(flush=True)
    read_french_prompt(message)


def confirm_installation(paths: InstallerPaths, use_color: bool) -> bool:
    """Présente la confirmation et accepte les réponses historiques."""

    while True:
        show_brand_header(paths, use_color)
        write(
            "Cette installation va créer le raccourci suivant :",
            use_color=use_color,
        )
        write(f"  {paths.shortcut}", color=Ansi.GREEN, use_color=use_color)
        write(use_color=use_color)
        write("en exécutant l'application :", use_color=use_color)
        write(
            f"  {paths.morning_application}",
            color=Ansi.GREEN,
            use_color=use_color,
        )
        write(use_color=use_color)

        answer = read_french_prompt(
            "Continuer l'installation ? [O/N/? pour l'aide]"
        ).strip().upper()
        if answer in {"O", "OUI", "Y", "YES"}:
            return True
        if answer in {"N", "NON", "Q", "QUIT"}:
            return False
        if answer == "?":
            show_readme_help(paths, use_color)
            wait_for_exit("Appuyez sur <Entrée> pour revenir à la confirmation")
            continue

        write(
            "Réponse attendue : O, N ou ?.",
            color=Ansi.YELLOW,
            use_color=use_color,
        )
        time.sleep(0.9)


def create_startup_shortcut(paths: InstallerPaths) -> None:
    """Crée le raccourci .lnk avec pywin32, sans lancer PowerShell."""

    try:
        import win32com.client
    except ImportError as exc:
        raise InstallerError(
            "La dépendance pywin32 est absente. "
            "Installez-la avec : python -m pip install -r requirements.txt"
        ) from exc

    if paths.morning_application.suffix.casefold() == ".exe":
        target = paths.morning_application
        arguments = ""
    else:
        pythonw = Path(sys.executable).with_name("pythonw.exe")
        if getattr(sys, "frozen", False) or not pythonw.is_file():
            raise InstallerError(
                "DTLmorning.exe est absent. Placez-le à côté de l'installateur."
            )
        target = pythonw
        arguments = f'"{paths.morning_application}"'

    try:
        wsh_shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = wsh_shell.CreateShortcut(str(paths.shortcut))
        shortcut.TargetPath = str(target)
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = str(paths.install_dir)
        shortcut.Description = SHORTCUT_DESCRIPTION
        shortcut.Save()
    except Exception as exc:
        raise InstallerError(
            f"Impossible de créer le raccourci {paths.shortcut} : {exc}"
        ) from exc

    if not paths.shortcut.is_file():
        raise InstallerError(
            f"Le raccourci n'a pas été créé correctement : {paths.shortcut}"
        )


def run_installer(paths: InstallerPaths, use_color: bool) -> int:
    """Exécute le scénario interactif complet de l'installateur."""

    if not paths.morning_application.is_file():
        raise InstallerError(
            "DTLmorning.exe ou DTLmorning.py est introuvable dans : "
            f"{paths.install_dir}"
        )

    if not confirm_installation(paths, use_color):
        show_brand_header(paths, use_color)
        write(
            "Installation annulée. Aucun changement n'a été effectué.",
            color=Ansi.YELLOW,
            use_color=use_color,
        )
        wait_for_exit()
        return 0

    show_brand_header(paths, use_color)
    write("Installation en cours...", use_color=use_color)
    write(use_color=use_color)
    create_startup_shortcut(paths)

    write(
        "Installation terminée avec succès.",
        color=Ansi.GREEN,
        use_color=use_color,
    )
    write(use_color=use_color)
    write("Raccourci créé :", use_color=use_color)
    write(f"  {paths.shortcut}", use_color=use_color)
    write(use_color=use_color)
    write(
        "DTL Morning sera lancé automatiquement à la prochaine ouverture de session.",
        use_color=use_color,
    )
    wait_for_exit()
    return 0


def main() -> int:
    """Point d'entrée de l'application."""

    use_color = configure_console()
    try:
        require_windows()
        paths = build_paths()
        return run_installer(paths, use_color)
    except (KeyboardInterrupt, EOFError):
        write(use_color=use_color)
        write("Installation interrompue.", color=Ansi.YELLOW, use_color=use_color)
        return 130
    except Exception as exc:
        install_dir = application_directory()
        try:
            fallback_startup = Path(
                os.environ.get("APPDATA", install_dir)
            ) / "Microsoft/Windows/Start Menu/Programs/Startup"
            error_paths = InstallerPaths(
                install_dir=install_dir,
                morning_application=install_dir / "DTLmorning.exe",
                readme=install_dir / "README_Fr.md",
                version_file=install_dir / ".dtl_version",
                startup_folder=fallback_startup,
                shortcut=fallback_startup / "DTLmorning.lnk",
            )
            show_brand_header(error_paths, use_color)
        except Exception:
            clear_console(use_color)

        write("ÉCHEC DE L'INSTALLATION", color=Ansi.RED, use_color=use_color)
        write(use_color=use_color)
        write(str(exc), color=Ansi.RED, use_color=use_color)
        write(use_color=use_color)
        write(
            "Aucun raccourci valide n'a pu être créé.",
            use_color=use_color,
        )
        try:
            wait_for_exit()
        except (KeyboardInterrupt, EOFError):
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
