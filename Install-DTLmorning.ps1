<#
.SYNOPSIS
    Installe DTL Morning au démarrage de la session Windows.

.DESCRIPTION
    Ce script crée un raccourci "DTL Morning" dans le dossier de démarrage
    de l'utilisateur courant. Le raccourci lance directement DTLmorning.ps1
    avec PowerShell, sans utiliser VBScript.

.NOTES
    Auteur : Didier DTL Morandi / www.netdtl.com
	30 juin 2026
#>

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "DTL Morning - Installation au démarrage d'une session Windows"
Write-Host "============================================================="
Write-Host ""

# Dossier où se trouve ce script d'installation
$InstallDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MorningScript = Join-Path $InstallDir "DTLmorning.ps1"

if (-not (Test-Path $MorningScript)) {
    Write-Host "ERREUR : DTLmorning.ps1 introuvable dans :" -ForegroundColor Red
    Write-Host "  $InstallDir"
    Write-Host ""
    Write-Host "Placez Install-DTLmorning.ps1 dans le même dossier que DTLmorning.ps1."
    exit 1
}

# Dossier de démarrage de l'utilisateur courant
$StartupFolder = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupFolder "DTL Morning.lnk"

# Commande PowerShell cible
$PowerShellExe = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$MorningScript`""

# Création du raccourci
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PowerShellExe
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "Lance DTL Morning au démarrage de la session Windows"
$Shortcut.Save()

Write-Host "Installation terminée avec succès." -ForegroundColor Green
Write-Host ""
Write-Host "Raccourci créé :"
Write-Host "  $ShortcutPath"
Write-Host ""
Write-Host "Script lancé au démarrage :"
Write-Host "  $MorningScript"
Write-Host ""
Write-Host "DTL Morning sera lancé automatiquement à la prochaine ouverture de session."
Write-Host ""