# app.py
import tkinter as tk
import os
import sys
from datetime import datetime

# 调试信息
print("当前路径:", os.path.abspath('.'))
print("sys.path:", sys.path)
print("utils 是否存在:", os.path.exists('utils'))
print("utils/__init__.py 是否存在:", os.path.exists('utils/__init__.py'))
print("utils/file_importer.py 是否存在:", os.path.exists('utils/file_importer.py'))

from config import *
from pages.data_center import DataCenterPage
from pages.search import SearchPage
from pages.inspection import InspectionPage
from pages.settings import SettingsPage
from utils import FileImporter, PopupManager
from core.core_engine import CoreEngine  # 👈 添加这行导入


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.resizable(False, False)
        self.configure(bg=C_VOID)
        
        # 同步状态
        self.is_syncing = False
        self.current_page = "数据中心"
        
        # ========== 数据存储属性 ==========
        self.data_vault = {}      # 存储导入的DataFrame
        self.M1_data_storage = {} # 存储文件路径
        
        # ========== 1. 顶部导航栏 ==========
        self.create_top_bar()
        
        # ========== 2. 内容容器 ==========
        self.content_frame = tk.Frame(self, bg=C_VOID)
        self.content_frame.pack(fill="both", expand=True)
        
        # ========== 3. 创建所有页面 ==========
        self.create_pages()
        
        # ========== 4. 日志区域 ==========
        self.create_log_area()
        
        # ========== 5. 状态栏（始终在最底部） ==========
        self.create_status_bar()
        
        # 初始化工具类
        self.file_importer = FileImporter(self)
        self.popup_manager = PopupManager(self)
        self.core_engine = CoreEngine(self)
        
        # 显示默认页面
        self.switch_page("数据中心")
        
        # 添加系统启动日志
        self.add_log("系统", "核心系统", "程序启动完成")
    
    def create_top_bar(self):
        """创建顶部导航栏"""
        self.top_bar = tk.Frame(self, height=50, bg=C_BG_MEDIUM)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)
        
        # 左侧区域：核心系统 + 子导航标签
        left_frame = tk.Frame(self.top_bar, bg=C_BG_MEDIUM)
        left_frame.pack(side="left", padx=(15, 0))
        
        # 核心系统文字
        core_label = tk.Label(left_frame, 
                             text="⚙️ 核心系统", 
                             font=F_TITLE,
                             bg=C_BG_MEDIUM,
                             fg=C_GOLD)
        core_label.pack(side="left")
        
        # 子导航标签容器（动态显示）
        self.subnav_container = tk.Frame(left_frame, bg=C_BG_MEDIUM)
        self.subnav_container.pack(side="left", padx=(20, 0))
        
        # 右侧：导航按钮
        nav_frame = tk.Frame(self.top_bar, bg=C_BG_MEDIUM)
        nav_frame.pack(side="right", padx=(0, 15))
        
        self.nav_buttons = {}
        
        for text in NAV_ITEMS:
            btn = tk.Label(nav_frame, 
                          text=text,
                          font=F_MAIN,
                          bg=C_BG_MEDIUM,
                          fg=C_TEXT_DIM,
                          padx=8, pady=6)
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, name=text: self.switch_page(name))
            self.nav_buttons[text] = btn
        
        # 默认选中数据中心
        self.nav_buttons["数据中心"].config(fg=C_GOLD)
        
        # 金色下划线
        self.indicator = tk.Frame(self.top_bar, height=3, bg=C_GOLD)
        self.after(100, self.place_indicator)
    
    def create_log_area(self):
        """创建日志区域"""
        self.log_frame = tk.Frame(self, height=220, bg=C_BG_MEDIUM)
        
        # 日志标题栏
        title_frame = tk.Frame(self.log_frame, bg=C_BG_MEDIUM)
        title_frame.pack(fill="x", padx=15, pady=(12, 10))
        
        log_title = tk.Label(title_frame,
                            text="📋 运行日志",
                            font=("微软雅黑", 13, "bold"),
                            bg=C_BG_MEDIUM,
                            fg=C_GOLD)
        log_title.pack(side="left")
        
        # 日志内容
        log_container = tk.Frame(self.log_frame, bg=C_BG_DARK)
        log_container.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        
        self.log_text = tk.Text(log_container,
                               bg=C_BG_DARK,
                               fg=C_LOG_TEXT,
                               font=F_LOG,
                               bd=0,
                               highlightthickness=0,
                               wrap=tk.WORD,
                               height=8)
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(log_container, bg=C_BG_MEDIUM)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # 配置日志标签样式
        self.log_text.tag_config("time", foreground="#FFA500")
        self.log_text.tag_config("success", foreground="#00FF7F", font=(F_LOG[0], F_LOG[1], "bold"))
        self.log_text.tag_config("error", foreground="#FF4444", font=(F_LOG[0], F_LOG[1], "bold"))
        self.log_text.tag_config("warning", foreground="#FFD700", font=(F_LOG[0], F_LOG[1], "bold"))
        self.log_text.tag_config("system", foreground="#00CED1")
        self.log_text.tag_config("execute", foreground="#9B59B6", font=(F_LOG[0], F_LOG[1], "bold"))
        self.log_text.tag_config("module", foreground="#87CEEB")
        self.log_text.tag_config("normal", foreground="#E0E0E0")
        
        self.log_text.config(state="disabled")
    
    def create_status_bar(self):
        """创建状态栏（始终在最底部）"""
        self.status_bar = tk.Frame(self, height=25, bg=C_BG_DARK)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)
        
        # 左侧：当前页面名称
        self.page_status = tk.Label(self.status_bar,
                                   text="数据中心",
                                   font=("微软雅黑", 9),
                                   bg=C_BG_DARK,
                                   fg=C_GOLD)
        self.page_status.pack(side="left", padx=10)
        
        # 右侧：时间
        self.time_label = tk.Label(self.status_bar,
                                  text="",
                                  font=("微软雅黑", 9),
                                  bg=C_BG_DARK,
                                  fg=C_TEXT_DIM)
        self.time_label.pack(side="right", padx=10)
        
        # 更新时间
        self.update_time()
    
    def update_time(self):
        """更新时间显示（每秒更新）"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"🕐 {now}")
        self.after(1000, self.update_time)
    
    def show_log(self):
        """显示日志区域（在状态栏上方）"""
        # 先确保状态栏在底部
        self.status_bar.pack(fill="x", side="bottom")
        # 然后在状态栏上方插入日志区域
        self.log_frame.pack(fill="x", side="bottom", before=self.status_bar)
    
    def hide_log(self):
        """隐藏日志区域"""
        self.log_frame.pack_forget()
        # 确保状态栏仍然在底部
        self.status_bar.pack(fill="x", side="bottom")
    
    def create_pages(self):
        """创建所有页面"""
        self.pages = {}
        
        # 数据中心
        data_center = DataCenterPage(self.content_frame, self)
        data_center.place(x=0, y=0, relwidth=1, relheight=1)
        data_center.lower()
        self.pages["数据中心"] = data_center
        
        # 综合搜索
        search = SearchPage(self.content_frame, self)
        search.place(x=0, y=0, relwidth=1, relheight=1)
        search.lower()
        self.pages["综合搜索"] = search
        
        # 检测合格
        inspection = InspectionPage(self.content_frame, self)
        inspection.place(x=0, y=0, relwidth=1, relheight=1)
        inspection.lower()
        self.pages["检测合格"] = inspection
        
        # 设置选项
        settings = SettingsPage(self.content_frame, self)
        settings.place(x=0, y=0, relwidth=1, relheight=1)
        settings.lower()
        self.pages["设置选项"] = settings
    
    def place_indicator(self):
        """放置金色指示器"""
        current_btn = self.nav_buttons[self.current_page]
        x = current_btn.winfo_rootx() - self.winfo_rootx()
        width = current_btn.winfo_width()
        self.indicator.place(x=x, y=47, width=width)
    
    def switch_page(self, page_name):
        """切换主页面"""
        if self.is_syncing:
            self.add_log("警告", "系统", "同步中，无法切换页面")
            return
        
        self.current_page = page_name
        
        # 更新状态栏左侧的页面名称
        self.page_status.config(text=page_name)
        
        # 更新导航按钮颜色
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.config(fg=C_GOLD)
            else:
                btn.config(fg=C_TEXT_DIM)
        
        # 移动指示器
        self.place_indicator()
        
        # 清空子导航容器
        for widget in self.subnav_container.winfo_children():
            widget.destroy()
        
        # 显示选中的页面
        for name, page in self.pages.items():
            if name == page_name:
                page.lift()
                
                # 根据页面类型显示不同的子导航
                if name == "数据中心":
                    # 显示数据中心子界面标签
                    data_center = self.pages["数据中心"]
                    data_center.show_subnav(self.subnav_container)
                    self.show_log()
                elif name == "综合搜索":
                    # 显示同步按钮
                    sync_button = tk.Label(self.subnav_container,
                                          text="同步数据",
                                          font=F_SUB,
                                          bg=C_BG_MEDIUM,
                                          fg=C_GOLD,
                                          padx=20, pady=5)
                    sync_button.bind("<Button-1>", lambda e: self.on_sync_click())
                    sync_button.pack(side="left")
                    self.show_log()
                else:
                    # 其他页面不显示日志
                    self.hide_log()
            else:
                page.lower()
        
        # 注释掉的页面切换日志
        # self.add_log("系统", "页面导航", f"切换到【{page_name}】")
    
    def on_sync_click(self):
        """同步数据按钮点击事件"""
        if self.is_syncing:
            return
        
        self.is_syncing = True
        
        # 获取当前显示的同步按钮
        current_sync_button = None
        for widget in self.subnav_container.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "同步数据":
                current_sync_button = widget
                break
        
        if current_sync_button and current_sync_button.winfo_exists():
            current_sync_button.config(text="同步中", fg=C_DISABLED_TEXT)
        
        # 禁用所有可点击组件
        self.set_widgets_state("disabled")
        
        self.add_log("系统", "同步数据", "开始同步...")
        
        # 模拟同步过程
        self.after(2000, self.on_sync_complete)
    
    def on_sync_complete(self):
        """同步完成"""
        self.is_syncing = False
        
        # 获取当前显示的同步按钮
        current_sync_button = None
        for widget in self.subnav_container.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "同步中":
                current_sync_button = widget
                break
        
        if current_sync_button and current_sync_button.winfo_exists():
            current_sync_button.config(text="同步数据", fg=C_GOLD)
        
        # 启用所有可点击组件
        self.set_widgets_state("normal")
        
        self.add_log("成功", "同步数据", "同步完成")
    
    def set_widgets_state(self, state):
        """设置所有可点击组件的状态（添加存在性检查）"""
        if state == "disabled":
            # 禁用导航按钮
            for btn in self.nav_buttons.values():
                if btn.winfo_exists():
                    btn.config(fg=C_DISABLED_TEXT)
            
            # 禁用数据中心子界面标签
            data_center = self.pages["数据中心"]
            if hasattr(data_center, 'subpage_labels'):
                for label in data_center.subpage_labels:
                    if label.winfo_exists():
                        label.config(fg=C_DISABLED_TEXT)
            
            # 禁用同步按钮
            for widget in self.subnav_container.winfo_children():
                if isinstance(widget, tk.Label) and widget.winfo_exists():
                    if widget.cget("text") in ["同步数据", "同步中"]:
                        widget.config(fg=C_DISABLED_TEXT)
        else:
            # 恢复导航按钮颜色
            for name, btn in self.nav_buttons.items():
                if btn.winfo_exists():
                    if name == self.current_page:
                        btn.config(fg=C_GOLD)
                    else:
                        btn.config(fg=C_TEXT_DIM)
            
            # 恢复数据中心子界面标签颜色
            data_center = self.pages["数据中心"]
            if hasattr(data_center, 'subpage_labels'):
                for i, label in enumerate(data_center.subpage_labels):
                    if label.winfo_exists():
                        if i == data_center.current_subpage:
                            label.config(fg=C_GOLD)
                        else:
                            label.config(fg=C_TEXT_DIM)
            
            # 恢复同步按钮颜色
            if self.current_page == "综合搜索":
                for widget in self.subnav_container.winfo_children():
                    if isinstance(widget, tk.Label) and widget.winfo_exists():
                        if widget.cget("text") == "同步数据":
                            widget.config(fg=C_GOLD)
                        elif widget.cget("text") == "同步中":
                            widget.config(text="同步数据", fg=C_GOLD)
    
    def add_log(self, log_type, module, message):
        """添加自定义日志"""
        self.log_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 日志类型映射到标签
        tag_map = {
            "成功": "success",
            "失败": "error",
            "警告": "warning",
            "系统": "system",
            "执行": "execute"
        }
        tag = tag_map.get(log_type, "normal")
        
        # 模块颜色映射
        module_tag = "normal"
        if module == "数据中心":
            module_tag = "data_center"
        elif module == "综合搜索":
            module_tag = "search"
        
        # 按照新格式插入日志：时间：类型：模块：消息
        self.log_text.insert(tk.END, f"{timestamp}：", "time")
        self.log_text.insert(tk.END, f"{log_type}：", tag)
        self.log_text.insert(tk.END, f"{module}：", module_tag)
        self.log_text.insert(tk.END, f"{message}\n", "normal")
        
        self.log_text.see(tk.END)
        
        # 限制日志行数
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 100:
            self.log_text.delete("1.0", "2.0")
        
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
