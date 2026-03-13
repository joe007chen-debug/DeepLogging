# config/config.py
# 程序基础配置
APP_PATH = r"D:\Projects\DeepLogging_20260313\BIN\DeepLogging.exe"
BACKEND = "uia"  # UIA后端（适配你的控件属性）

# 超时配置
LAUNCH_TIMEOUT = 10  # 程序启动超时（秒）
CONTROL_TIMEOUT = 5   # 控件加载超时（秒）
WAIT_SHORT = 0.5      # 短等待（秒）
WAIT_LONG = 2         # 长等待（秒）
AAC_SHORTTIMEOUT = 20

# 窗口匹配规则（按实际窗口标题调整）
WINDOW_TITLE_PATTERN =r"DeepLogging"    #r"DeepLogging \[.*\.dlp\]"  r"DeepLogging AI"