# config.py
import platform

# 颜色常量
C_VOID = "#0A0A0A"
C_BG_DARK = "#0A0A0A"
C_BG_MEDIUM = "#1A1A1A"  # 确保这行存在
C_BG_LIGHT = "#252525"
C_GOLD = "#D4AF37"
C_GOLD_LIGHT = "#FFD700"
C_TEXT_DIM = "#777777"
C_BORDER = "#333333"
C_LOG_TEXT = "#E0E0E0"
C_DISABLED_TEXT = "#555555"
C_SUCCESS = "#00FF7F"
C_ERROR = "#FF3030"
C_GOLD_PRIME = "#D4AF37"  # 金色（与 C_GOLD 相同）
C_SUCCESS = "#00FF7F"  # 成功绿色
C_ERROR = "#FF3030"    # 错误红色


# 按钮颜色 - 黑金风格
BTN_RESET = "#1A1A1A"      # 重置按钮背景
BTN_IMPORT = "#1A1A1A"      # 导入按钮背景
BTN_START = "#1A1A1A"       # 启动按钮背景
BTN_HOVER = "#252525"       # 悬停背景

# 系统检测
IS_MAC = platform.system() == "Darwin"

# 字体配置
F_MAIN = ("微软雅黑", 12)
F_TITLE = ("微软雅黑", 15, "bold")
F_SUB = ("微软雅黑", 11)
F_BTN = ("微软雅黑", 11, "bold")
F_LOG = ("Consolas", 11)

# 应用信息
APP_TITLE = "数据治理平台 · 核心系统 v1.0"
APP_GEOMETRY = "850x700"

# 导航项
NAV_ITEMS = ["数据中心", "综合搜索", "检测合格", "设置选项"]

# 数据中心子界面
DATA_CENTER_SUBPAGES = ["表格筛选", "按键复制", "备用功能"]
