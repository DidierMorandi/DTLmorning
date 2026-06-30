# DTL Morning

DTL Morning est un petit assistant de démarrage Windows qui vérifie les dépôts Git locaux et affiche un résumé matinal dans une boîte de dialogue Windows.

Le script parcourt un dossier racine, détecte les dépôts Git et indique ce qui demande une action :

- fichiers non suivis ou modifiés à enregistrer ;
- changements indexés à valider ;
- commits distants à récupérer ;
- commits locaux à publier.

Si tout est propre, il affiche un message calme indiquant qu'aucune action n'est nécessaire. La même boîte de dialogue propose aussi d'ouvrir le panneau XAMPP quand Apache ne semble pas démarré.

## Fichiers

- `DTLmorning.ps1` : script PowerShell qui inspecte les dépôts et affiche le message.
- `Install-DTLmorning.cmd` : lanceur simple de l'installation.
- `Install-DTLmorning.ps1` : script qui crée le raccourci de démarrage Windows.

DTL Morning n'utilise plus de lanceur VBScript. Le raccourci de démarrage lance directement `DTLmorning.ps1` avec PowerShell.

## Prérequis

- Windows
- PowerShell
- Git disponible en ligne de commande
- Dépôts Git locaux sous le dossier à analyser
- XAMPP, si l'ouverture du panneau Apache doit être utile

## Utilisation

Lancer le script manuellement depuis PowerShell :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

Par défaut, le script analyse le dossier parent du dossier DTL Morning et salue l'utilisateur Windows courant.

Le dossier racine, le nom affiché et le dossier XAMPP peuvent être personnalisés :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Path\To\DTLmorning.ps1" -Root "C:\Path\To\Projects" -UserName "VotreNom" -XamppPath "C:\xampp"
```

## Installation au démarrage de session Windows

La méthode la plus simple consiste à lancer l'installateur :

1. Ouvrir le dossier DTL Morning.
2. Double-cliquer sur `Install-DTLmorning.cmd`.
3. Laisser l'installateur créer le raccourci `DTL Morning` dans le dossier de démarrage Windows.

Le raccourci est créé dans le dossier de démarrage de l'utilisateur courant et lance :

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "...\DTLmorning.ps1"
```

DTL Morning s'exécutera automatiquement à chaque ouverture de session Windows.

## Raccourci de démarrage manuel

Si vous préférez créer le raccourci de démarrage manuellement :

1. Appuyer sur `Win + R`.
2. Taper `shell:startup` puis Entrée.
3. Clic droit dans le dossier, puis **Nouveau > Raccourci**.
4. Utiliser cette cible, adaptée à votre chemin local :

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

5. Nommer le raccourci `DTL Morning`.

## Fonctionnement

Le script PowerShell :

1. recherche les dépôts Git sous le dossier racine sélectionné ;
2. ignore les dossiers générés courants comme `.git`, `build`, `dist`, `node_modules`, `logs` et `__pycache__` ;
3. exécute `git status --porcelain --branch` dans chaque dépôt ;
4. construit une courte liste d'actions ;
5. affiche le résultat dans une boîte de dialogue Windows ;
6. ouvre le panneau XAMPP si vous répondez oui à la question sur Apache.

## Désinstallation

Pour désactiver le message matinal :

1. Appuyer sur `Win + R`.
2. Taper `shell:startup`.
3. Appuyer sur Entrée.
4. Supprimer le raccourci `DTL Morning`.

## Mise à jour - 30 juin 2026

DTL Morning s'installe maintenant au démarrage de session Windows via un raccourci créé par PowerShell, sans lanceur VBScript.

Points confirmés :

- Découverte récursive des dépôts Git depuis le dossier racine configuré.
- Détection des fichiers modifiés, non suivis, indexés, des commits locaux à publier et des commits distants à récupérer.
- Estimation simple du temps nécessaire selon le nombre d'actions détectées.
- Résumé affiché dans une boîte de dialogue Windows.
- Paramètres principaux : `-Root`, `-UserName` et `-XamppPath`.
- L'installateur crée un raccourci `DTL Morning` dans le dossier de démarrage de l'utilisateur courant.
- Le raccourci de démarrage lance directement PowerShell avec `-WindowStyle Hidden`.
