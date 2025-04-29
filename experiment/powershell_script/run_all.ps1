Get-ChildItem -Path . -Recurse -Filter "run.ps1" | ForEach-Object {
    $absolutePath = $_.FullName
    $workingDir = Split-Path $absolutePath
    Write-Host "Launching: $absolutePath"

    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -NoProfile -File `"$absolutePath`"" -WorkingDirectory $workingDir -WindowStyle Hidden
}