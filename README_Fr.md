# DTL Morning

DTL Morning est un petit assistant de démarrage Windows qui vérifie les dépôts Git locaux et affiche un résumé matinal dans une boîte de dialogue Windows.

Après un court délai, le script parcourt un dossier racine, détecte les dépôts Git et indique ce qui demande une action :

- fichiers non suivis ou modifiés à enregistrer ;
- changements indexés à valider ;
- commits distants à récupérer ;
- commits locaux à publier.

Si tout est propre, il affiche un message calme indiquant qu'aucune action n'est nécessaire.

## Fichiers

- `DTLmorning.ps1` : script PowerShell qui inspecte les dépôts et affiche le message.
- `DTLmorning.vbs` : lanceur Windows Script Host optionnel pour exécuter le script PowerShell silencieusement, sans laisser de fenêtre ouverte.

## Prérequis

- Windows
- PowerShell
- Git disponible en ligne de commande
- Dépôts Git locaux sous le dossier à analyser

## Utilisation

Lancer le script manuellement depuis PowerShell :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

Par défaut, le script analyse le dossier où se trouve `DTLmorning.ps1` et salue `Didier`.

Le dossier racine et le nom affiché peuvent être personnalisés :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Path\To\DTLmorning.ps1" -Root "C:\Path\To\Projects" -UserName "YourName"
```

## Installation au démarrage de session Windows

La méthode la plus simple consiste à ajouter le lanceur VBS au dossier de démarrage Windows.

1. Ouvrir le dossier DTL Morning.
2. Modifier `DTLmorning.vbs`.
3. Vérifier que `scriptPath` pointe vers l'emplacement réel de `DTLmorning.ps1` :

```vbscript
scriptPath = "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

4. Appuyer sur `Win + R`.
5. Taper :

```text
shell:startup
```

6. Appuyer sur Entrée.
7. Copier `DTLmorning.vbs` dans le dossier de démarrage.

Le script s'exécutera automatiquement à chaque ouverture de session Windows. Il attend quelques secondes afin de laisser le bureau finir de charger.

## Variante : raccourci de démarrage

Il est aussi possible de créer un raccourci dans le dossier de démarrage :

1. Appuyer sur `Win + R`.
2. Taper `shell:startup` puis Entrée.
3. Clic droit dans le dossier, puis **Nouveau > Raccourci**.
4. Utiliser cette cible :

```text
wscript.exe "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.vbs"
```

5. Nommer le raccourci `DTL Morning`.

## Désinstallation

Pour désactiver le message matinal :

1. Appuyer sur `Win + R`.
2. Taper `shell:startup`.
3. Appuyer sur Entrée.
4. Supprimer `DTLmorning.vbs` ou le raccourci `DTL Morning`.

## Mise à jour - 14 juin 2026

`DTLmorning.ps1` analyse maintenant les dépôts Git avec une logique d'action priorisée.

Points confirmés :

- Découverte récursive des dépôts Git depuis le dossier racine configuré.
- Détection des fichiers modifiés, non suivis, indexés, des commits locaux à publier et des commits distants à récupérer.
- Estimation simple du temps nécessaire selon le nombre d'actions détectées.
- Résumé affiché dans une boîte de dialogue Windows.
- Paramètres principaux : `-Root`, `-UserName` et `-DelaySeconds`.
- Le script peut être lancé à l'ouverture de session Windows via un raccourci ou un lanceur VBS.
