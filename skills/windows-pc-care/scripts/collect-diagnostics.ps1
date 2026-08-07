# Windows PC Care - Read-only diagnostics for Windows 10/11.
# Does not modify configuration, delete files, or read personal file contents.
# Usage: powershell -NoProfile -File .\collect-diagnostics.ps1 -OutputPath .\pc-care-baseline.json

[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path (Get-Location) ("pc-care-baseline-{0}.json" -f (Get-Date -Format "yyyyMMdd-HHmmss")))
)

$ErrorActionPreference = "Continue"

function Get-SafeValue {
    param([scriptblock]$Action)
    try { & $Action } catch { $null }
}

function Convert-BytesToGB {
    param([Nullable[long]]$Bytes)
    if ($null -eq $Bytes) { return $null }
    return [math]::Round($Bytes / 1GB, 2)
}

function Get-DirectoryStats {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    try {
        $files = Get-ChildItem -LiteralPath $Path -Force -File -Recurse -ErrorAction SilentlyContinue
        $bytes = ($files | Measure-Object -Property Length -Sum).Sum
        return [PSCustomObject]@{
            Path = $Path
            FileCount = @($files).Count
            SizeGB = Convert-BytesToGB $bytes
        }
    } catch {
        return [PSCustomObject]@{ Path = $Path; FileCount = $null; SizeGB = $null; Error = $_.Exception.Message }
    }
}

$os = Get-SafeValue { Get-CimInstance -ClassName Win32_OperatingSystem }
$cpu = Get-SafeValue { Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1 }
$memoryModules = @(Get-SafeValue { Get-CimInstance -ClassName Win32_PhysicalMemory })
$logicalDisks = @(Get-SafeValue { Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" })
$startup = @(Get-SafeValue { Get-CimInstance -ClassName Win32_StartupCommand })

# Do not include the signed-in account name in the report. Machine name is retained only
# because it helps distinguish multiple baselines from the same device.

$ramBytes = ($memoryModules | Measure-Object -Property Capacity -Sum).Sum
$installedSoftware = @()
$uninstallPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
)
foreach ($path in $uninstallPaths) {
    try {
        $installedSoftware += Get-ItemProperty -Path $path -ErrorAction SilentlyContinue |
            Where-Object { $_.DisplayName } |
            Select-Object DisplayName, DisplayVersion, Publisher, InstallDate
    } catch {}
}
$installedSoftware = @($installedSoftware | Sort-Object DisplayName -Unique)

$systemDrive = if ($env:SystemDrive) { $env:SystemDrive } else { "C:" }
$tempPaths = @($env:TEMP, (Join-Path $env:WINDIR "Temp")) | Where-Object { $_ }
$defender = Get-SafeValue { Get-MpComputerStatus }
$bitLocker = Get-SafeValue { Get-BitLockerVolume -MountPoint $systemDrive }
$restore = Get-SafeValue { Get-ComputerRestorePoint | Sort-Object CreationTime -Descending | Select-Object -First 1 }
$updates = @(Get-SafeValue { Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 })

$result = [PSCustomObject]@{
    SchemaVersion = "1.0"
    CollectedAt = (Get-Date).ToString("o")
    Computer = [PSCustomObject]@{
        Name = $env:COMPUTERNAME
        SystemDrive = $systemDrive
    }
    OperatingSystem = [PSCustomObject]@{
        Caption = $os.Caption
        Version = $os.Version
        BuildNumber = $os.BuildNumber
        Architecture = $os.OSArchitecture
        LastBootUpTime = if ($os) { $os.LastBootUpTime.ToString("o") } else { $null }
    }
    Hardware = [PSCustomObject]@{
        CPU = $cpu.Name
        Cores = $cpu.NumberOfCores
        LogicalProcessors = $cpu.NumberOfLogicalProcessors
        MemoryTotalGB = Convert-BytesToGB $ramBytes
        MemoryModules = @($memoryModules | ForEach-Object {
            [PSCustomObject]@{
                CapacityGB = Convert-BytesToGB $_.Capacity
                SpeedMHz = $_.Speed
                Manufacturer = $_.Manufacturer
                PartNumber = ($_.PartNumber -replace "\s+$", "")
            }
        })
        MemoryFreeGB = if ($os) { [math]::Round(($os.FreePhysicalMemory * 1KB) / 1GB, 2) } else { $null }
    }
    Storage = @($logicalDisks | ForEach-Object {
        [PSCustomObject]@{
            Drive = $_.DeviceID
            VolumeName = $_.VolumeName
            FileSystem = $_.FileSystem
            SizeGB = Convert-BytesToGB $_.Size
            FreeGB = Convert-BytesToGB $_.FreeSpace
            FreePercent = if ($_.Size -gt 0) { [math]::Round(($_.FreeSpace / $_.Size) * 100, 1) } else { $null }
        }
    })
    Security = [PSCustomObject]@{
        DefenderAntivirusEnabled = $defender.AntivirusEnabled
        DefenderRealtimeProtectionEnabled = $defender.RealTimeProtectionEnabled
        BitLockerVolumeStatus = $bitLocker.VolumeStatus
        BitLockerProtectionStatus = $bitLocker.ProtectionStatus
        LatestRestorePoint = if ($restore) { $restore.CreationTime.ToString("o") } else { $null }
    }
    Maintenance = [PSCustomObject]@{
        RecentUpdates = @($updates | ForEach-Object {
            [PSCustomObject]@{ HotFixID = $_.HotFixID; InstalledOn = $_.InstalledOn; Description = $_.Description }
        })
        TemporaryDirectories = @($tempPaths | ForEach-Object { Get-DirectoryStats -Path $_ })
    }
    StartupItems = @($startup | Sort-Object Name | ForEach-Object {
        [PSCustomObject]@{ Name = $_.Name; Command = $_.Command; Location = $_.Location; User = $_.User }
    })
    InstalledSoftware = $installedSoftware
    TopMemoryProcesses = @(Get-Process -ErrorAction SilentlyContinue |
        Sort-Object WorkingSet64 -Descending |
        Select-Object -First 20 |
        ForEach-Object {
            [PSCustomObject]@{
                Name = $_.ProcessName
                Id = $_.Id
                WorkingSetMB = [math]::Round($_.WorkingSet64 / 1MB, 1)
                CPUSeconds = $_.CPU
            }
        })
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    throw "Output directory does not exist: $parent"
}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Output "Diagnostics saved: $OutputPath"
