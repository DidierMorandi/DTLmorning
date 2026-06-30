# DTL Morning

DTL Morning is a small Windows startup helper that checks local Git repositories and shows a morning summary in a Windows message box.

The script scans a root folder for Git repositories, checks their status, and tells you what needs attention:

- unstaged or untracked files to save
- staged changes to commit
- remote commits to synchronize
- local commits to publish

If everything is clean, it displays a calm "no action required" message. The same dialog also offers to open the XAMPP control panel when Apache does not seem to be running.

## Files

- `DTLmorning.ps1`: the PowerShell script that scans repositories and displays the message.
- `Install-DTLmorning.cmd`: a simple launcher for the installer.
- `Install-DTLmorning.ps1`: creates the Windows startup shortcut.

DTL Morning no longer uses a VBScript launcher. The startup shortcut launches `DTLmorning.ps1` directly with PowerShell.

## Requirements

- Windows
- PowerShell
- Git available from the command line
- Local Git repositories under the folder you want to scan
- XAMPP, if you want the Apache panel shortcut to be useful

## Usage

Run the script manually from PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

By default, the script scans the parent folder of the DTL Morning folder and greets the current Windows user.

You can customize the scanned root folder, displayed name, and XAMPP folder:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Path\To\DTLmorning.ps1" -Root "C:\Path\To\Projects" -UserName "YourName" -XamppPath "C:\xampp"
```

## Install at Windows Sign-In

The easiest way to show the message every time you open a Windows session is to run the installer:

1. Open the DTL Morning folder.
2. Double-click `Install-DTLmorning.cmd`.
3. Let the installer create the `DTL Morning` shortcut in the Windows Startup folder.

The shortcut is created in the current user's Startup folder and launches:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "...\DTLmorning.ps1"
```

DTL Morning will now run automatically each time you sign in to Windows.

## Manual Startup Shortcut

If you prefer to create the startup shortcut manually:

1. Press `Win + R`.
2. Type `shell:startup` and press Enter.
3. Right-click inside the folder and choose **New > Shortcut**.
4. Use this target, adapted to your local path:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\Utilisateur\Documents\outils\DTLmorning\DTLmorning.ps1"
```

5. Name the shortcut `DTL Morning`.

## How It Works

The PowerShell script:

1. searches for Git repositories under the selected root folder
2. ignores common generated folders such as `.git`, `build`, `dist`, `node_modules`, `logs`, and `__pycache__`
3. runs `git status --porcelain --branch` in each repository
4. builds a short task list
5. displays the result in a Windows message box
6. opens the XAMPP control panel when you answer yes to the Apache prompt

## Uninstall

To disable the morning message:

1. Press `Win + R`.
2. Type `shell:startup`.
3. Press Enter.
4. Delete the `DTL Morning` shortcut from the Startup folder.

## Update - 30 June 2026

DTL Morning now installs itself at Windows sign-in through a PowerShell-created shortcut instead of a VBScript launcher.

Confirmed points:

- Recursive Git repository discovery from the configured root folder.
- Detection of modified, untracked, staged files, local commits to publish, and remote commits to pull.
- Simple time estimate based on the number of detected actions.
- Summary displayed in a Windows message box.
- Main parameters: `-Root`, `-UserName`, and `-XamppPath`.
- The installer creates a `DTL Morning` shortcut in the current user's Startup folder.
- The startup shortcut launches PowerShell directly with `-WindowStyle Hidden`.
