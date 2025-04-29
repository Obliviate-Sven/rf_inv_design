Get-Process | Where-Object { $_.ProcessName -like "*python*" } | ForEach-Object { $_.Kill() }

Get-Process | Where-Object { $_.ProcessName -like "*ansysedt*" } | ForEach-Object { $_.Kill() }