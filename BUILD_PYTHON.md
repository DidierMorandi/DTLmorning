# Compilation des applications Python

## Prérequis

- Windows ;
- Python 3.12 ;
- les dépendances de `requirements.txt`.

## Préparation

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Compilation en fichiers uniques

```bat
.venv\Scripts\pyinstaller.exe --clean DTLmorning.spec
.venv\Scripts\pyinstaller.exe --clean Install-DTLmorning.spec
```

Les fichiers `.spec` imposent déjà le mode one-file. PyInstaller refuse l'option `--onefile` quand un fichier `.spec` est fourni.

Les exécutables sont produits dans `dist` :

```text
dist\DTLmorning.exe
dist\Install-DTLmorning.exe
```

Pour constituer la distribution, placer ensemble :

```text
DTLmorning.exe
Install-DTLmorning.exe
Install-DTLmorning.cmd
README_Fr.md
.dtl_version
```

## Architecture

- `DTLmorning.py` utilise uniquement la bibliothèque standard Python et les API Windows natives via `ctypes`.
- `Install-DTLmorning.py` utilise `pywin32` pour créer le raccourci `.lnk`.
- Les commandes Git et XAMPP sont lancées directement avec `subprocess`, sans shell.
- Aucun composant ne lance ni ne nécessite PowerShell.
