# Windows PC Care - Opt-in cache cleanup for Windows 10/11.
# Default mode is preview only. -Apply is required to make changes.
# This script intentionally excludes Prefetch, Recycle Bin, browsers, Downloads,
# Windows Update cache, OneDrive, and all personal folders.
# Usage:
#   powershell -NoProfile -File .\safe-cache-cleanup.ps1
#   powershell -NoProfile -File .\safe-cache-cleanup.ps1 -Targets UserTemp,WindowsTemp -Apply

[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [ValidateSet("UserTemp", "WindowsTemp")]
    [string[]]$Targets = @("UserTemp"),
    [switch]$Apply,
    [string]$ReportPath = (Join-Path (Get-Location) ("pc-care-cache-preview-{0}.json" -f (Get-Date -Format "yyyyMMdd-HHmmss")))
)

$ErrorActionPreference = "Continue"

$targetMap = @{
    UserTemp = $env:TEMP
    WindowsTemp = (Join-Path $env:WINDIR "Temp")
}

function Get-Preview {
    param([string]$Name, [string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) {
        return [PSCustomObject]@{ Target = $Name; Path = $Path; Exists = $false; FileCount = 0; SizeMB = 0; Errors = @() }
    }

    $errors = @()
    $files = @()
    try {
        $files = @(Get-ChildItem -LiteralPath $Path -Force -File -Recurse -ErrorAction SilentlyContinue)
    } catch {
        $errors += $_.Exception.Message
    }
    $bytes = ($files | Measure-Object -Property Length -Sum).Sum
    return [PSCustomObject]@{
        Target = $Name
        Path = $Path
        Exists = $true
        FileCount = $files.Count
        SizeMB = [math]::Round(($bytes / 1MB), 1)
        Errors = $errors
    }
}

$previews = @()
foreach ($target in $Targets) {
    $previews += Get-Preview -Name $target -Path $targetMap[$target]
}

$report = [PSCustomObject]@{
    GeneratedAt = (Get-Date).ToString("o")
    Mode = if ($Apply) { "Apply" } else { "Preview" }
    Scope = $Targets
    Exclusions = @(
        "Prefetch", "Recycle Bin", "Downloads", "Desktop", "Documents", "Pictures", "Videos",
        "Browser profiles", "OneDrive", "Windows Update cache", "Program Files", "Windows system files"
    )
    Candidates = $previews
}
$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ReportPath -Encoding UTF8

Write-Output "Mode: $(if ($Apply) { "APPLY" } else { "PREVIEW ONLY" })"
foreach ($preview in $previews) {
    Write-Output ("{0}: {1} files, {2} MB, {3}" -f $preview.Target, $preview.FileCount, $preview.SizeMB, $preview.Path)
}
Write-Output "Report saved: $ReportPath"

if (-not $Apply) {
    Write-Output "No files were changed. Review the report and obtain explicit approval before re-running with -Apply."
    return
}

foreach ($target in $Targets) {
    $path = $targetMap[$target]
    if (-not $path -or -not (Test-Path -LiteralPath $path)) { continue }
    if (-not $PSCmdlet.ShouldProcess($path, "Delete temporary files under the confirmed target")) { continue }

    $removed = 0
    $failed = 0
    Get-ChildItem -LiteralPath $path -Force -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
            $removed++
        } catch {
            $failed++
        }
    }
    Write-Output ("{0}: removed {1} files; skipped {2} locked or protected files." -f $target, $removed, $failed)
}

Write-Output "Cleanup completed. Re-run collect-diagnostics.ps1 to verify reclaimed space."
