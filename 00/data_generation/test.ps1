# 获取当前脚本的绝对路径
$SRC_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
# 项目根目录
$PROJECT_DIR = Split-Path -Parent $SRC_DIR

# Python 脚本路径
$PYTHON_SCRIPT = Join-Path $SRC_DIR "data_generation.py"

# 读取 iteration 和 experiment_index 模板
$PYTHON_CONTENT = Get-Content $PYTHON_SCRIPT -Raw

# 提取 iteration 数值
$ITERATION = [regex]::Match($PYTHON_CONTENT, 'iteration\s*=\s*(\d+)').Groups[1].Value

# 在 PowerShell 中重新生成 date（模拟 Python 中的逻辑）
$currentTime = Get-Date
$year = $currentTime.Year % 100
$month = $currentTime.Month
$day = $currentTime.Day
$date = "$year.$month.$day"

# 根据新的规则组装 experiment_index
$EXPERIMENT_INDEX = "${date}_${ITERATION}_iter"

# 构造实验目录路径
$EXPERIMENT_DIR = Join-Path (Join-Path $PROJECT_DIR "results") $EXPERIMENT_INDEX
New-Item -ItemType Directory -Force -Path $EXPERIMENT_DIR | Out-Null

# 日志文件和PID文件
$LOG_FILE = Join-Path $EXPERIMENT_DIR ("$EXPERIMENT_INDEX.log")
$PID_FILE = Join-Path $EXPERIMENT_DIR ("$EXPERIMENT_INDEX.pid")

# Conda环境相关
$TARGET_ENV = "inv"
$CURRENT_CONDA_ENV = $env:CONDA_DEFAULT_ENV

if ($CURRENT_CONDA_ENV -eq $TARGET_ENV) {

    Write-Output "EXPERIMENT INDEX: $EXPERIMENT_INDEX"
    Write-Output "SRC_DIR: $SRC_DIR"
    Write-Output "PROJECT_DIR: $PROJECT_DIR"
    Write-Output "ITERATION: $ITERATION"
    Write-Output "EXPERIMENT_DIR: $EXPERIMENT_DIR"
    Write-Output "LOG_FILE: $LOG_FILE"
    Write-Output "PID_FILE: $PID_FILE"


} else {
    $errorMessage = "ERROR: Current Conda Env isn't '$TARGET_ENV', but '$CURRENT_CONDA_ENV'"
    $errorMessage | Tee-Object -FilePath $LOG_FILE -Append
    "Please use 'conda activate $TARGET_ENV'" | Tee-Object -FilePath $LOG_FILE -Append
    exit 1
}
