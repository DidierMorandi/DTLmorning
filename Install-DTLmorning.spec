# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["Install-DTLmorning.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "pythoncom",
        "pywintypes",
        "win32com.client",
        "win32com.shell.shell",
        "win32com.shell.shellcon",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Install-DTLmorning",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    version="Install-DTLmorning.version.txt",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
