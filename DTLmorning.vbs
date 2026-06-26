Option Explicit

Dim shell
Dim scriptPath
Dim command

Set shell = CreateObject("WScript.Shell")
scriptPath = "D:\Documents\Mes sites Web\Secours catholique\outils\DTLmorning\DTLmorning.ps1"
command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File " & Chr(34) & scriptPath & Chr(34)

shell.Run command, 0, False
