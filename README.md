# DTL Morning

**DTL Morning v1.0-10** is a native Python 3.12 application for Windows. It checks local Git repositories and displays a morning summary in a Windows dialog box.

The application reports what needs attention:

- unstaged or untracked files to save;
- staged changes to commit;
- remote commits to pull;
- local commits to publish.

If everything is clean, it confirms that no action is required. The same dialog offers to open the XAMPP control panel when Apache does not seem to be running.

## Files

- `DTLmorning.py`: scans repositories and displays the message;
- `DTLmorning.exe`: compiled standalone application;
- `Install-DTLmorning.py`: Python startup-shortcut installer;
- `Install-DTLmorning.exe`: compiled standalone installer;
- `Install-DTLmorning.cmd`: convenient installer launcher;
- `requirements.txt` and the `.spec` files: dependencies and build configuration.

DTL Morning no longer uses PowerShell or VBScript. The startup shortcut launches `DTLmorning.exe` directly.

## Requirements

- Windows;
- Git available from the command line;
- Python 3.12 and `pywin32` only when running from source;
- XAMPP if the Apache control-panel option is useful.

The compiled executables are standalone and do not require Python to be installed.

## Usage

Run the executable:

```bat
DTLmorning.exe
```

Or run the source with Python 3.12:

```bat
py -3.12 DTLmorning.py
```

By default, the application scans the parent of its own folder and greets the current Windows user. Parameters can be customized:

```bat
DTLmorning.exe --root "C:\Path\To\Projects" --user-name "YourName" --xampp-path "D:\xampp"
```

The former parameter names `-Root`, `-UserName`, and `-XamppPath` are also accepted.

Without `--xampp-path`, DTL Morning automatically detects XAMPP through the
`XAMPP_HOME` and `XAMPP_PATH` environment variables, beside the application,
then in the `xampp` folder at the root of available drives and in the usual
Windows application folders.

## Install at Windows Sign-In

1. Put `DTLmorning.exe` and `Install-DTLmorning.exe` in the same folder.
2. Double-click `Install-DTLmorning.cmd` or `Install-DTLmorning.exe`.
3. Answer `O` to confirm, `N` to cancel, or `?` to display help.
4. Press `<Enter>` to close the installer.

The installer creates `DTLmorning.lnk` in the current user's Startup folder and targets `DTLmorning.exe` directly.

## Manual Startup Shortcut

1. Press `Win + R`.
2. Type `shell:startup` and press Enter.
3. Create a new shortcut.
4. Select `DTLmorning.exe` as the target.
5. Name the shortcut `DTLmorning`.

## How It Works

The Python application:

1. searches for Git repositories under the selected root folder;
2. ignores `.git`, `build`, `dist`, `node_modules`, `logs`, `__pycache__`, and hidden folders;
3. directly runs `git status --porcelain --branch` without a command shell;
4. builds a short task list;
5. displays the result through the native Windows API;
6. directly opens the XAMPP control panel when the user answers yes.

## Uninstall

1. Press `Win + R`.
2. Type `shell:startup` and press Enter.
3. Delete the `DTLmorning` shortcut.

## Update - 17 July 2026

DTL Morning and its installer were fully rewritten in Python 3.12. The PowerShell scripts were removed, and startup shortcuts now target the native executable directly.
