# DTL Morning

**DTL Morning v1.0-8** est une application Python 3.12 native pour Windows. Elle vérifie les dépôts Git locaux et affiche un résumé matinal dans une boîte de dialogue Windows.

L'application indique ce qui demande une action :

- fichiers non suivis ou modifiés à enregistrer ;
- changements indexés à valider ;
- commits distants à récupérer ;
- commits locaux à publier.

Si tout est propre, elle confirme qu'aucune action n'est nécessaire. La même boîte de dialogue propose d'ouvrir le panneau XAMPP quand Apache ne semble pas démarré.

## Fichiers

- `DTLmorning.py` : application qui inspecte les dépôts et affiche le message ;
- `DTLmorning.exe` : version autonome compilée ;
- `Install-DTLmorning.py` : installateur Python du raccourci de démarrage ;
- `Install-DTLmorning.exe` : version autonome de l'installateur ;
- `Install-DTLmorning.cmd` : lanceur pratique de l'installateur ;
- `requirements.txt` et les fichiers `.spec` : dépendances et configuration de compilation.

DTL Morning n'utilise plus PowerShell ni VBScript. Le raccourci de démarrage lance directement `DTLmorning.exe`.

## Pourquoi installer DTL Morning ?

Installer DTL Morning permet d'obtenir automatiquement, à chaque ouverture de session Windows, un bilan matinal de vos dépôts Git locaux.

DTL Morning indique les fichiers modifiés ou non suivis à enregistrer, les changements préparés à valider, les mises à jour distantes à récupérer et les commits locaux à publier. Si tout est propre, il confirme qu'aucune action n'est nécessaire. Il peut également proposer d'ouvrir le panneau de contrôle XAMPP lorsque Apache ne semble pas démarré.

L'installation évite donc de lancer manuellement l'outil chaque matin et permet de repérer immédiatement les projets qui demandent votre attention.

## Prérequis

- Windows ;
- Git disponible en ligne de commande ;
- Python 3.12 et `pywin32` uniquement pour exécuter les sources ;
- XAMPP si l'ouverture du panneau Apache doit être utile.

Les exécutables compilés sont autonomes et ne nécessitent pas d'installation de Python.

## Utilisation

Lancer l'exécutable :

```bat
DTLmorning.exe
```

Ou lancer la source avec Python 3.12 :

```bat
py -3.12 DTLmorning.py
```

Par défaut, l'application analyse le dossier parent de son propre dossier et salue l'utilisateur Windows courant. Les paramètres peuvent être personnalisés :

```bat
DTLmorning.exe --root "C:\Path\To\Projects" --user-name "VotreNom" --xampp-path "C:\xampp"
```

Les anciens noms de paramètres `-Root`, `-UserName` et `-XamppPath` restent également acceptés.

## Installation au démarrage de session Windows

1. Placer `DTLmorning.exe` et `Install-DTLmorning.exe` dans le même dossier.
2. Double-cliquer sur `Install-DTLmorning.cmd` ou `Install-DTLmorning.exe`.
3. Répondre `O` pour confirmer, `N` pour annuler ou `?` pour afficher l'aide.
4. Appuyer sur `<Entrée>` pour fermer l'installateur.

Le raccourci `DTLmorning.lnk` est créé dans le dossier de démarrage de l'utilisateur courant et cible directement `DTLmorning.exe`.

## Raccourci de démarrage manuel

1. Appuyer sur `Win + R`.
2. Taper `shell:startup`, puis Entrée.
3. Créer un nouveau raccourci.
4. Sélectionner `DTLmorning.exe` comme cible.
5. Nommer le raccourci `DTLmorning`.

## Fonctionnement

L'application Python :

1. recherche les dépôts Git sous le dossier racine sélectionné ;
2. ignore `.git`, `build`, `dist`, `node_modules`, `logs`, `__pycache__` et les dossiers cachés ;
3. exécute directement `git status --porcelain --branch` sans interpréteur de commandes ;
4. construit une courte liste d'actions ;
5. affiche le résultat avec l'API Windows native ;
6. ouvre directement le panneau XAMPP si l'utilisateur répond oui.

## Désinstallation

Pour désactiver le message matinal :

1. Appuyer sur `Win + R`.
2. Taper `shell:startup`.
3. Appuyer sur Entrée.
4. Supprimer le raccourci `DTLmorning`.

## Mise à jour - 17 juillet 2026

DTL Morning et son installateur ont été intégralement réécrits en Python 3.12. Les scripts PowerShell ont été supprimés et les raccourcis ciblent désormais directement l'exécutable natif.
