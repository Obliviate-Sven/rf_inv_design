# 获取当前脚本的绝对路径
$SRC_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJECT_DIR = Split-Path -Parent $SRC_DIR
$ROOT_DIR = Split-Path -Parent $PROJECT_DIR

# Python 脚本路径
$PYTHON_SCRIPT = Join-Path $SRC_DIR "data_generation.py"

# 提取 experiment_index
$PYTHON_CONTENT = Get-Content $PYTHON_SCRIPT -Raw
$EXPERIMENT_INDEX = [regex]::Match($PYTHON_CONTENT, 'experiment_index\s*=\s*"([^"]+)"').Groups[1].Value

# 构建实验目录路径
$EXPERIMENT_DIR = Join-Path (Join-Path $PROJECT_DIR "results") $EXPERIMENT_INDEX

# 日志文件和 PID 文件路径
$LOG_FILE = Join-Path $EXPERIMENT_DIR "$EXPERIMENT_INDEX.log"
$PID_FILE = Join-Path $EXPERIMENT_DIR "$EXPERIMENT_INDEX.pid"

# 开始删除文件

# 删除 src 目录下的所有 .log 文件
Get-ChildItem -Path $SRC_DIR -Filter "*.log" -File -ErrorAction SilentlyContinue | Remove-Item -Force

# 删除项目目录下的 tmp 文件夹
$TMP_DIR = Join-Path $PROJECT_DIR "tmp"
if (Test-Path $TMP_DIR) {
    Remove-Item -Recurse -Force $TMP_DIR
}

# 删除类似于 PROJECT_DIR_EXPERIMENT_INDEX* 的目录
$pattern = "$PROJECT_DIR" + "_$EXPERIMENT_INDEX*"
Get-ChildItem -Path (Split-Path $PROJECT_DIR -Parent) -Filter ($(Split-Path $pattern -Leaf)) -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Recurse -Force $_.FullName
}

# 删除实验目录
if (Test-Path $EXPERIMENT_DIR) {
    Remove-Item -Recurse -Force $EXPERIMENT_DIR
}

Write-Host "✅ Cleanup completed for experiment index '$EXPERIMENT_INDEX'."
