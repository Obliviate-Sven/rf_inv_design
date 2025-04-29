$endTime = Get-Date "2025-05-11 00:00:00"

while ((Get-Date) -lt $endTime) {

    Get-ChildItem -Path . -Recurse -Filter "*.log" | Select-String -Pattern "ERROR" -CaseSensitive:$false | ForEach-Object {
        Write-Output "$($_.Path):$($_.LineNumber): $($_.Line.Trim())"
    }

    $totalLines = (Get-ChildItem -Path . -Recurse -Filter "*data.csv" | Get-Content | Measure-Object -Line).Lines
    Write-Output "Total lines: $totalLines"

    Write-Output "--$(Get-Date -Format \"yyyy-MM-dd HH:mm:ss\")-- Check"

    Start-Sleep -Seconds 30
}