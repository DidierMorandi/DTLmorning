# DTL Morning

DTL Morning is a small Windows startup helper that checks local Git repositories and shows a morning summary in a Windows message box.

After a short delay, the script scans a root folder for Git repositories, checks their status, and tells you what needs attention:

- unstaged or untracked files to save
- staged changes to commit
- remote commits to synchronize
- local commits to publish

If everything is clean, it displays a calm "no action required" message.

## Files

- `DTLmorning.ps1`: the PowerShell script that scans repositories and displays the message.
- `DTLmorning.vbs`: an optional Windows Script Host launcher that can run the PowerShell script silently, without leaving a PowerShell window open.

## Requirements

- Windows
- PowerShell
- Git available from the command line
- Local Git repositories under the folder you want to scan

## Usage

Run the script manually from PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

By default, the script scans the folder where `DTLmorning.ps1` is located and greets `Didier`.

You can customize the scanned root folder and displayed name:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Path\To\DTLmorning.ps1" -Root "C:\Path\To\Projects" -UserName "YourName"
```

## Install at Windows Sign-In

The easiest way to show the message every time you open a Windows session is to add the VBS launcher to the Windows Startup folder.

1. Open the DTL Morning folder.
2. Edit `DTLmorning.vbs`.
3. Make sure `scriptPath` points to the real location of `DTLmorning.ps1`:

```vbscript
scriptPath = "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

4. Press `Win + R`.
5. Type:

```text
shell:startup
```

6. Press Enter.
7. Copy `DTLmorning.vbs` into the Startup folder.

The script will now run automatically each time you sign in to Windows. It waits a few seconds before checking repositories, so the desktop has time to finish loading.

## Alternative: Create a Startup Shortcut

Instead of copying the VBS file itself, you can create a shortcut in the Startup folder:

1. Press `Win + R`.
2. Type `shell:startup` and press Enter.
3. Right-click inside the folder and choose **New > Shortcut**.
4. Use this target:

```text
wscript.exe "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.vbs"
```

5. Name the shortcut `DTL Morning`.

## How It Works

The PowerShell script:

1. waits 8 seconds
2. searches for Git repositories under the selected root folder
3. ignores common generated folders such as `.git`, `build`, `dist`, `node_modules`, `logs`, and `__pycache__`
4. runs `git status --porcelain --branch` in each repository
5. builds a short task list
6. displays the result in a Windows message box

## Uninstall

To disable the morning message:

1. Press `Win + R`.
2. Type `shell:startup`.
3. Press Enter.
4. Delete `DTLmorning.vbs` or the `DTL Morning` shortcut from the Startup folder.
