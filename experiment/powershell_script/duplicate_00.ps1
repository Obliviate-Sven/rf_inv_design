# 源文件夹
$sourceFolder = "..\..\00"

# 获取当前脚本所在目录
$currentScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 获取上一级目录
$parentPath = Split-Path -Parent $currentScriptPath

# 生成当前日期作为新文件夹名字（格式：yyyy-MM-dd）
$dateFolderName = Get-Date -Format "yyyy-MM-dd"

# 最终目标目录
$targetRoot = Join-Path $parentPath $dateFolderName

# 如果目标目录不存在，创建它
if (!(Test-Path $targetRoot)) {
    New-Item -ItemType Directory -Path $targetRoot
}

# 将当前目录下的 run_all.ps1 复制到 $targetRoot 目录中
$runAllScript = Join-Path $currentScriptPath "run_all.ps1"
if (Test-Path $runAllScript) {
    Copy-Item -Force $runAllScript -Destination $targetRoot
} else {
    Write-Host "Warning: run_all.ps1 not found in $currentScriptPath"
}

$killAllScript = Join-Path $currentScriptPath "kill_all.ps1"
if (Test-Path $killAllScript) {
    Copy-Item -Force $killAllScript -Destination $targetRoot
} else {
    Write-Host "Warning: kill_all.ps1 not found in $currentScriptPath"
}

$errCheckScript = Join-Path $currentScriptPath "err_data_check.ps1"
if (Test-Path $errCheckScript) {
    Copy-Item -Force $errCheckScript -Destination $targetRoot
} else {
    Write-Host "Warning: err_data_check.ps1 not found in $currentScriptPath"
}

# copy00 ~ copy09
for ($i = 0; $i -le 0; $i++) {
    $destFolder = Join-Path $targetRoot ("copy0$i")
    Copy-Item -Recurse -Force $sourceFolder $destFolder
}

# copy10 ~ copy19
# for ($i = 0; $i -le 9; $i++) {
#     $destFolder = Join-Path $targetRoot ("copy1$i")
#     Copy-Item -Recurse -Force $sourceFolder $destFolder
# }
