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
    # 后台启动Python脚本并同步写日志
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "python"
    $startInfo.Arguments = "`"$PYTHON_SCRIPT`""
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $startInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    $process.Start() | Out-Null

    # 同步读取并写日志
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()

    $stdout | Out-File -FilePath $LOG_FILE -Append
    $stderr | Out-File -FilePath $LOG_FILE -Append

    $process.WaitForExit()

    # 记录PID和时间
    $CURRENT_TIME = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "RUN TIME: $CURRENT_TIME - PID: $($process.Id) - EXPERIMENT INDEX: $EXPERIMENT_INDEX" | Out-File $PID_FILE -Encoding UTF8

} else {
    $errorMessage = "ERROR: Current Conda Env isn't '$TARGET_ENV', but '$CURRENT_CONDA_ENV'"
    $errorMessage | Tee-Object -FilePath $LOG_FILE -Append
    "Please use 'conda activate $TARGET_ENV'" | Tee-Object -FilePath $LOG_FILE -Append
    exit 1
}