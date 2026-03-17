# pages/settings.py
import tkinter as tk
from tkinter import ttk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER, BTN_RESET, BTN_IMPORT, BTN_START, BTN_HOVER
from widgets.gold_combobox import GoldCombobox, ClearableEntry

class SettingsPage(tk.Frame):
    """设置选项页面 - 4个区域，2x2网格布局，等分大小"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.entries = {}
        self.lock_buttons = {}
        self.locked_states = {}
        self.create_widgets()
        
        # 绑定页面点击事件
        self.bind("<Button-1>", self.on_page_click)
    
    def on_page_click(self, event):
        """点击页面空白处释放焦点"""
        focused = self.focus_get()
        if focused and isinstance(focused, tk.Entry) and event.widget != focused:
            self.focus_set()
    
    def create_lock_button(self, parent, btn_name):
        """创建锁定/解锁按钮"""
        lock_btn = tk.Label(parent,
                           text="🔓",  # 解锁图标
                           font=("微软雅黑", 10, "bold"),
                           bg=BTN_RESET,
                           fg=C_GOLD,
                           padx=8, pady=3,
                           cursor="",
                           highlightthickness=1,
                           highlightbackground=C_GOLD,
                           highlightcolor=C_GOLD)
        
        def on_enter(e):
            lock_btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            lock_btn.config(bg=BTN_RESET, fg=C_GOLD)
        
        lock_btn.bind("<Enter>", on_enter)
        lock_btn.bind("<Leave>", on_leave)
        lock_btn.bind("<Button-1>", lambda e, name=btn_name: self.toggle_lock(name))
        
        return lock_btn
    
    def toggle_lock(self, btn_name):
        """切换锁定/解锁状态"""
        entry = self.entries.get(btn_name)
        lock_btn = self.lock_buttons.get(btn_name)
        
        if not entry or not lock_btn:
            return
        
        current_state = self.locked_states.get(btn_name, False)
        
        if current_state:
            # 解锁
            entry.enable()
            lock_btn.config(text="🔓")
            self.locked_states[btn_name] = False
            self.app.add_log("系统", "设置选项", f"解锁【{btn_name}】")
        else:
            # 锁定
            entry.set_readonly(True)
            lock_btn.config(text="🔒")
            self.locked_states[btn_name] = True
            self.app.add_log("系统", "设置选项", f"锁定【{btn_name}】")
        
        self.focus_set()
    
    # ===== 新增的事件处理方法 =====
    
    def on_browse_click(self):
        """浏览按钮点击事件"""
        # 这里可以添加文件夹选择逻辑
        self.app.add_log("系统", "设置选项", "浏览文件夹")
        print("浏览文件夹")
    
    def on_delete_all(self):
        """删除所有配置按钮点击事件"""
        self.app.add_log("系统", "设置选项", "删除所有配置")
        print("删除所有配置")
    
    def on_save_all(self):
        """保存所有配置按钮点击事件"""
        self.app.add_log("系统", "设置选项", "保存所有配置")
        print("保存所有配置")
    
    # ===== 界面创建方法 =====
    
    def create_widgets(self):
        """创建界面组件 - 2x2网格布局，4个区域等分"""
        # 主容器 - 使用网格布局
        main_frame = tk.Frame(self, bg=C_VOID)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.bind("<Button-1>", self.on_page_click)
        
        # 配置网格权重，让4个区域等分空间
        main_frame.grid_rowconfigure(0, weight=1, uniform="row")
        main_frame.grid_rowconfigure(1, weight=1, uniform="row")
        main_frame.grid_columnconfigure(0, weight=1, uniform="col")
        main_frame.grid_columnconfigure(1, weight=1, uniform="col")
        
        # ===== 区域1（左上）- 2个文本框和2个锁定按键 =====
        region1_container = tk.Frame(main_frame, bg=C_VOID,
                                     highlightthickness=2,
                                     highlightbackground=C_GOLD,
                                     highlightcolor=C_GOLD)
        region1_container.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        region1_container.bind("<Button-1>", self.on_page_click)
        region1_container.grid_propagate(False)  # 防止内容改变容器大小
        
        region1_frame = tk.Frame(region1_container, bg=C_VOID)
        region1_frame.pack(fill="both", expand=True, padx=10, pady=10)
        region1_frame.bind("<Button-1>", self.on_page_click)
        
        self.create_region1_content(region1_frame)
        
        # ===== 区域2（右上）- 空 =====
        region2_container = tk.Frame(main_frame, bg=C_VOID,
                                     highlightthickness=2,
                                     highlightbackground=C_GOLD,
                                     highlightcolor=C_GOLD)
        region2_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        region2_container.bind("<Button-1>", self.on_page_click)
        region2_container.grid_propagate(False)
        
        region2_frame = tk.Frame(region2_container, bg=C_VOID)
        region2_frame.pack(fill="both", expand=True)
        region2_frame.bind("<Button-1>", self.on_page_click)
        
        # 区域2内容（空，只显示区域标识）
        region2_content = tk.Frame(region2_frame, bg=C_VOID)
        region2_content.pack(expand=True, fill="both", padx=20, pady=20)
        region2_content.bind("<Button-1>", self.on_page_click)
        
        region2_label = tk.Label(region2_content,
                                text="区域2预留",
                                font=("微软雅黑", 14),
                                bg=C_VOID,
                                fg=C_TEXT_DIM)
        region2_label.pack(expand=True)
        region2_label.bind("<Button-1>", self.on_page_click)
        
        # ===== 区域3（左下）- 空 =====
        region3_container = tk.Frame(main_frame, bg=C_VOID,
                                     highlightthickness=2,
                                     highlightbackground=C_GOLD,
                                     highlightcolor=C_GOLD)
        region3_container.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        region3_container.bind("<Button-1>", self.on_page_click)
        region3_container.grid_propagate(False)
        
        region3_frame = tk.Frame(region3_container, bg=C_VOID)
        region3_frame.pack(fill="both", expand=True)
        region3_frame.bind("<Button-1>", self.on_page_click)
        
        # 区域3内容（空，只显示区域标识）
        region3_content = tk.Frame(region3_frame, bg=C_VOID)
        region3_content.pack(expand=True, fill="both", padx=20, pady=20)
        region3_content.bind("<Button-1>", self.on_page_click)
        
        region3_label = tk.Label(region3_content,
                                text="区域3预留",
                                font=("微软雅黑", 14),
                                bg=C_VOID,
                                fg=C_TEXT_DIM)
        region3_label.pack(expand=True)
        region3_label.bind("<Button-1>", self.on_page_click)
        
        # ===== 区域4（右下）- 空 =====
        region4_container = tk.Frame(main_frame, bg=C_VOID,
                                     highlightthickness=2,
                                     highlightbackground=C_GOLD,
                                     highlightcolor=C_GOLD)
        region4_container.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        region4_container.bind("<Button-1>", self.on_page_click)
        region4_container.grid_propagate(False)
        
        region4_frame = tk.Frame(region4_container, bg=C_VOID)
        region4_frame.pack(fill="both", expand=True)
        region4_frame.bind("<Button-1>", self.on_page_click)
        
        # 区域4内容（空，只显示区域标识）
        region4_content = tk.Frame(region4_frame, bg=C_VOID)
        region4_content.pack(expand=True, fill="both", padx=20, pady=20)
        region4_content.bind("<Button-1>", self.on_page_click)
        
        region4_label = tk.Label(region4_content,
                                text="区域4预留",
                                font=("微软雅黑", 14),
                                bg=C_VOID,
                                fg=C_TEXT_DIM)
        region4_label.pack(expand=True)
        region4_label.bind("<Button-1>", self.on_page_click)
    
    def create_region1_content(self, parent):
        """创建区域1内容 - 2个配置项 + 本地地址标签 + 选择本地文件按钮（居中）"""
        # 内容容器
        content_frame = tk.Frame(parent, bg=C_VOID)
        content_frame.pack(expand=True, fill="both")
        content_frame.bind("<Button-1>", self.on_page_click)
        
        # 标题
        title_label = tk.Label(content_frame,
                              text="配置选项",
                              font=("微软雅黑", 16, "bold"),
                              fg=C_GOLD,
                              bg=C_VOID,
                              anchor="w")
        title_label.pack(fill="x", pady=(0, 15))
        title_label.bind("<Button-1>", self.on_page_click)
        
        # ===== 第一个配置项 =====
        config1_row = tk.Frame(content_frame, bg=C_VOID)
        config1_row.pack(fill="x", pady=(0, 10))
        config1_row.bind("<Button-1>", self.on_page_click)
        
        # 配置标签
        tk.Label(config1_row,
                text="配置项1",
                font=("微软雅黑", 12),
                fg=C_TEXT_DIM,
                bg=C_VOID,
                width=8,
                anchor="w").pack(side="left")
        
        # 输入框 - 加宽
        entry1 = ClearableEntry(config1_row,
                               app=self.app,
                               width=18,
                               placeholder="请输入...")
        entry1.entry.config(font=("微软雅黑", 12))
        entry1.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        # 锁定按钮
        lock_btn1 = self.create_lock_button(config1_row, "配置项1")
        lock_btn1.pack(side="left")
        self.lock_buttons["配置项1"] = lock_btn1
        self.entries["配置项1"] = entry1
        self.locked_states["配置项1"] = False
        
        # ===== 第二个配置项 =====
        config2_row = tk.Frame(content_frame, bg=C_VOID)
        config2_row.pack(fill="x", pady=(0, 15))
        config2_row.bind("<Button-1>", self.on_page_click)
        
        tk.Label(config2_row,
                text="配置项2",
                font=("微软雅黑", 12),
                fg=C_TEXT_DIM,
                bg=C_VOID,
                width=8,
                anchor="w").pack(side="left")
        
        entry2 = ClearableEntry(config2_row,
                               app=self.app,
                               width=18,
                               placeholder="请输入...")
        entry2.entry.config(font=("微软雅黑", 12))
        entry2.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        lock_btn2 = self.create_lock_button(config2_row, "配置项2")
        lock_btn2.pack(side="left")
        self.lock_buttons["配置项2"] = lock_btn2
        self.entries["配置项2"] = entry2
        self.locked_states["配置项2"] = False
        
        # ===== 本地地址标签（居中） =====
        local_label_frame = tk.Frame(content_frame, bg=C_VOID)
        local_label_frame.pack(fill="x", pady=(0, 5))
        local_label_frame.bind("<Button-1>", self.on_page_click)
        
        # 创建一个容器来居中标签
        label_center = tk.Frame(local_label_frame, bg=C_VOID)
        label_center.pack(expand=True)
        
        tk.Label(label_center,
                text="本地地址",
                font=("微软雅黑", 14, "bold"),
                fg=C_GOLD,
                bg=C_VOID).pack()
        
        # ===== 选择本地文件按钮（居中，深紫色） =====
        button_frame = tk.Frame(content_frame, bg=C_VOID)
        button_frame.pack(fill="x", pady=(0, 20))
        button_frame.bind("<Button-1>", self.on_page_click)
        
        # 创建一个容器来居中按钮
        btn_center = tk.Frame(button_frame, bg=C_VOID)
        btn_center.pack(expand=True)
        
        # 选择本地文件按钮 - 深紫色
        browse_btn = tk.Label(btn_center,
                             text="选择本地文件",
                             font=("微软雅黑", 14, "bold"),
                             bg="#4B0082",  # 深紫色 (Indigo)
                             fg=C_GOLD,
                             padx=25, pady=8,
                             cursor="",
                             highlightthickness=1,
                             highlightbackground=C_GOLD,
                             highlightcolor=C_GOLD,
                             width=15)
        browse_btn.pack()
        
        def on_enter_browse(e):
            browse_btn.config(bg="#6A0DAD", fg=C_GOLD_LIGHT)  # 浅紫色悬停
        
        def on_leave_browse(e):
            browse_btn.config(bg="#4B0082", fg=C_GOLD)
        
        browse_btn.bind("<Enter>", on_enter_browse)
        browse_btn.bind("<Leave>", on_leave_browse)
        browse_btn.bind("<Button-1>", lambda e: self.on_browse_click())
        
        # ===== 操作按钮 =====
        button_row = tk.Frame(content_frame, bg=C_VOID)
        button_row.pack(fill="x", pady=(0, 0))
        button_row.bind("<Button-1>", self.on_page_click)
        
        # 删除所有配置按钮 - 深红色
        delete_btn = tk.Label(button_row,
                             text="删除所有配置",
                             font=("微软雅黑", 12, "bold"),
                             bg="#8B0000",  # 深红色 (DarkRed)
                             fg=C_GOLD,
                             padx=10, pady=8,
                             cursor="",
                             highlightthickness=1,
                             highlightbackground=C_GOLD,
                             highlightcolor=C_GOLD,
                             width=12)
        delete_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        def on_enter_delete(e):
            delete_btn.config(bg="#A52A2A", fg=C_GOLD_LIGHT)  # 棕色悬停
        
        def on_leave_delete(e):
            delete_btn.config(bg="#8B0000", fg=C_GOLD)
        
        delete_btn.bind("<Enter>", on_enter_delete)
        delete_btn.bind("<Leave>", on_leave_delete)
        delete_btn.bind("<Button-1>", lambda e: self.on_delete_all())
        
        # 保存所有配置按钮 - 金色
        save_btn = tk.Label(button_row,
                           text="保存所有配置",
                           font=("微软雅黑", 12, "bold"),
                           bg="#D4AF37",  # 金色 (Gold)
                           fg=C_VOID,  # 深色文字，与金色背景对比
                           padx=10, pady=8,
                           cursor="",
                           highlightthickness=1,
                           highlightbackground=C_GOLD,
                           highlightcolor=C_GOLD,
                           width=12)
        save_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        def on_enter_save(e):
            save_btn.config(bg="#FFD700", fg=C_VOID)  # 亮金色悬停
        
        def on_leave_save(e):
            save_btn.config(bg="#D4AF37", fg=C_VOID)
        
        save_btn.bind("<Enter>", on_enter_save)
        save_btn.bind("<Leave>", on_leave_save)
        save_btn.bind("<Button-1>", lambda e: self.on_save_all())
