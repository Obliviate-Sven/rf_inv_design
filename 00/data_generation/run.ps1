# 获取当前脚本的绝对路径
$SRC_DIR     = Split-Path -Parent $MyInvocation.MyCommand.Definition
# 项目根目录
$PROJECT_DIR = Split-Path -Parent $SRC_DIR

# Python 脚本路径
$PYTHON_SCRIPT = Join-Path $SRC_DIR "data_generation.py"

# 读取 iteration 和 experiment_index 模板
$PYTHON_CONTENT = Get-Content $PYTHON_SCRIPT -Raw

# 提取 iteration 数值
$ITERATION = [regex]::Match($PYTHON_CONTENT, 'iteration\s*=\s*(\d+)').Groups[1].Value

# 生成 date（模拟 Python 中的逻辑）
$currentTime = Get-Date
$year        = $currentTime.Year % 100
$month       = $currentTime.Month
$day         = $currentTime.Day
$date        = "$year.$month.$day"

# 组装 experiment_index
$EXPERIMENT_INDEX = "${date}_${ITERATION}_iter"

# 创建实验目录
$EXPERIMENT_DIR = Join-Path (Join-Path $PROJECT_DIR "results") $EXPERIMENT_INDEX
New-Item -ItemType Directory -Force -Path $EXPERIMENT_DIR | Out-Null

# 日志文件和 PID 文件路径
$LOG_FILE = Join-Path $EXPERIMENT_DIR ("$EXPERIMENT_INDEX.log")
$PID_FILE = Join-Path $EXPERIMENT_DIR ("$EXPERIMENT_INDEX.pid")

# Conda 环境检查
$TARGET_ENV        = "inv"
$CURRENT_CONDA_ENV = $env:CONDA_DEFAULT_ENV

if ($CURRENT_CONDA_ENV -eq $TARGET_ENV) {
    # 构造 cmd.exe 内部重定向命令
    # stdout 重定向到 $LOG_FILE，stderr 也重定向到同一个文件
    $innerCmd = "python `"$PYTHON_SCRIPT`" > `"$LOG_FILE`" 2>&1"

    # 启动 cmd.exe 执行上述命令，隐藏窗口，并返回 Process 对象
    $proc = Start-Process -FilePath "cmd.exe" `
        -ArgumentList "/c", $innerCmd `
        -WindowStyle Hidden `
        -PassThru

    # 记录运行时间和 PID
    "RUN TIME: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - PID: $($proc.Id) - EXPERIMENT INDEX: $EXPERIMENT_INDEX" |
        Out-File -FilePath $PID_FILE -Encoding UTF8

    # 等待 Python 脚本退出
    $proc.WaitForExit()
}
else {
    # 错误处理：不是期望的 Conda 环境
    $errorMessage = "ERROR: Current Conda Env isn't '$TARGET_ENV', but '$CURRENT_CONDA_ENV'"
    $errorMessage | Tee-Object -FilePath $LOG_FILE -Append
    "Please use 'conda activate $TARGET_ENV'" | Tee-Object -FilePath $LOG_FILE -Append
    exit 1
}