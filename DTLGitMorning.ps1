param(
    [string]$Root = $PSScriptRoot,
    [string]$UserName = "Didier"
)

Start-Sleep -Seconds 8

$ErrorActionPreference = "SilentlyContinue"
$ignoredDirs = @(".git", "build", "dist", "__pycache__", "logs", "node_modules")

function Find-GitRepositories {
    param([string]$RootPath)

    $repositories = New-Object System.Collections.Generic.List[string]
    if (-not (Test-Path -LiteralPath $RootPath)) {
        return $repositories
    }

    Get-ChildItem -LiteralPath $RootPath -Directory -Force | Sort-Object Name | ForEach-Object {
        if ($_.Name.StartsWith(".") -or $ignoredDirs -contains $_.Name) {
            return
        }

        if (Test-Path -LiteralPath (Join-Path $_.FullName ".git")) {
            $repositories.Add($_.FullName)
            return
        }

        Get-ChildItem -LiteralPath $_.FullName -Directory -Recurse -Force | Where-Object {
            -not $_.Name.StartsWith(".") -and $ignoredDirs -notcontains $_.Name
        } | ForEach-Object {
            if (Test-Path -LiteralPath (Join-Path $_.FullName ".git")) {
                $repositories.Add($_.FullName)
            }
        }
    }

    return $repositories
}

function Get-BranchAheadBehind {
    param([string]$BranchLine)

    $ahead = 0
    $behind = 0

    if ($BranchLine -match "ahead\s+(\d+)") {
        $ahead = [int]$Matches[1]
    }
    if ($BranchLine -match "behind\s+(\d+)") {
        $behind = [int]$Matches[1]
    }

    return @{ Ahead = $ahead; Behind = $behind }
}

function Get-RepositoryAction {
    param([string]$Repository)

    $statusOutput = & git -C $Repository status --porcelain --branch 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $statusOutput) {
        return $null
    }

    $branchLine = ($statusOutput | Where-Object { $_ -like "## *" } | Select-Object -First 1)
    $changes = @($statusOutput | Where-Object { $_ -notlike "## *" -and $_.Trim() })
    $aheadBehind = Get-BranchAheadBehind -BranchLine $branchLine

    $untracked = @($changes | Where-Object { $_.StartsWith("??") }).Count
    $staged = @($changes | Where-Object { -not $_.StartsWith("??") -and $_[0] -ne " " }).Count
    $unstaged = @($changes | Where-Object { -not $_.StartsWith("??") -and $_.Length -gt 1 -and $_[1] -ne " " }).Count

    $name = Split-Path -Leaf $Repository
    $parts = New-Object System.Collections.Generic.List[string]

    if ($untracked -gt 0 -or $unstaged -gt 0) {
        $count = $untracked + $unstaged
        $label = if ($count -eq 1) { "1 modification" } else { "$count modifications" }
        $parts.Add("enregistrer $label")
    }

    if ($staged -gt 0) {
        $label = if ($staged -eq 1) { "1 changement prêt à valider" } else { "$staged changements prêts à valider" }
        $parts.Add("valider $label")
    }

    if ($aheadBehind.Behind -gt 0) {
        $label = if ($aheadBehind.Behind -eq 1) { "1 commit distant" } else { "$($aheadBehind.Behind) commits distants" }
        $parts.Add("synchroniser $label")
    }

    if ($aheadBehind.Ahead -gt 0) {
        $label = if ($aheadBehind.Ahead -eq 1) { "1 commit sur GitHub" } else { "$($aheadBehind.Ahead) commits sur GitHub" }
        $parts.Add("publier $label")
    }

    if ($parts.Count -eq 0) {
        return $null
    }

    return @{
        Name = $name
        Text = "- ${name} : " + ($parts -join ", ")
        Ahead = $aheadBehind.Ahead
        WorkItems = $parts.Count
    }
}

function Get-EstimatedTime {
    param([int]$ActionCount)

    if ($ActionCount -eq 0) {
        return "0 minute"
    }
    if ($ActionCount -le 3) {
        return "moins de 5 minutes"
    }
    if ($ActionCount -le 6) {
        return "environ 10 minutes"
    }
    return "un petit quart d'heure"
}

$repositories = Find-GitRepositories -RootPath $Root
$actions = New-Object System.Collections.Generic.List[object]

foreach ($repository in $repositories) {
    $action = Get-RepositoryAction -Repository $repository
    if ($null -ne $action) {
        $actions.Add($action)
    }
}

$lines = New-Object System.Collections.Generic.List[string]
$rooster = [char]::ConvertFromUtf32(0x1F414)
$lines.Add("$rooster Bonjour $UserName !")
$lines.Add("")
$lines.Add("J'ai vérifié tes dépôts Git pendant que tu prenais ton café.")
$lines.Add("")

if ($actions.Count -eq 0) {
    $lines.Add("Tout est calme côté Git.")
    $lines.Add("")
    $lines.Add("Aucune action requise aujourd'hui.")
} else {
    $lines.Add("À faire aujourd'hui :")
    $lines.Add("")
    foreach ($action in $actions) {
        $lines.Add([string]$action.Text)
    }
    $lines.Add("")
    $lines.Add("Temps estimé : " + (Get-EstimatedTime -ActionCount $actions.Count))
}

$lines.Add("")
$lines.Add("Bonne journée !")

Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show(($lines -join [Environment]::NewLine), "DTL Git du matin", "OK", "Information") | Out-Null
