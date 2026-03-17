# pages/data_center_subpages/copy_subpage.py
import tkinter as tk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER, BTN_RESET, BTN_IMPORT, BTN_START, BTN_HOVER
from widgets.gold_combobox import ClearableEntry  # 导入ClearableEntry组件

class TextControlPanel(tk.Frame):
    """文本控制面板 - 包含5个切换界面和所有按钮"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.current_text_subpage = 0
        self.text_subpages = {}
        self.tab_buttons = []
        self.create_widgets()
        
        # 绑定点击事件到整个框架，用于取消焦点
        self.bind("<Button-1>", self.on_frame_click)
    
    def on_frame_click(self, event):
        """点击框架时取消所有输入框的焦点"""
        focused = self.focus_get()
        if focused and isinstance(focused, tk.Entry):
            self.focus_set()
    
    def create_button(self, parent, text, command, btn_type="default", small=False):
        """创建黑金风格按钮"""
        bg_color = {
            "reset": BTN_RESET,
            "import": BTN_IMPORT,
            "start": BTN_START
        }.get(btn_type, BTN_RESET)
        
        if small:
            padx_val = 6
            pady_val = 7
            font_size = 11
        else:
            padx_val = 8
            pady_val = 4
            font_size = 10
        
        btn = tk.Label(parent,
                      text=text,
                      font=("微软雅黑", font_size, "bold"),
                      bg=bg_color,
                      fg=C_GOLD,
                      padx=padx_val, pady=pady_val,
                      cursor="",
                      highlightthickness=1,
                      highlightbackground=C_GOLD,
                      highlightcolor=C_GOLD)
        btn.pack(side="left", fill="x", expand=True, padx=1)
        
        def on_enter(e):
            btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            btn.config(bg=bg_color, fg=C_GOLD)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e: command())
        
        return btn
    
    def create_widgets(self):
        """创建文本控制区域的所有组件"""
        # 标题行
        title_frame = tk.Frame(self, bg=C_VOID, height=30)
        title_frame.pack(fill="x", pady=(0, 5))
        title_frame.pack_propagate(False)
        title_frame.bind("<Button-1>", self.on_frame_click)
        
        tk.Label(title_frame,
                text="📝 文本控制",
                font=("微软雅黑", 11, "bold"),
                bg=C_VOID,
                fg=C_GOLD).pack(side="left")
        
        # 切换按钮
        tab_frame = tk.Frame(title_frame, bg=C_VOID)
        tab_frame.pack(side="right")
        tab_frame.bind("<Button-1>", self.on_frame_click)
        
        tab_names = ["ACD", "B表", "周X", "周3", "备用"]
        
        for i, name in enumerate(tab_names):
            btn = tk.Label(tab_frame,
                          text=name,
                          font=("微软雅黑", 13, "bold"),
                          bg=BTN_RESET,
                          fg=C_GOLD if i == 0 else C_TEXT_DIM,
                          padx=8, pady=2,
                          cursor="",
                          highlightthickness=1,
                          highlightbackground=C_GOLD if i == 0 else C_BG_MEDIUM,
                          highlightcolor=C_GOLD)
            btn.pack(side="left", padx=1)
            btn.bind("<Button-1>", lambda e, idx=i: self.switch_subpage(idx))
            
            btn.bind("<Enter>", lambda e, b=btn, idx=i: b.config(
                fg=C_GOLD_LIGHT,
                highlightbackground=C_GOLD_LIGHT))
            btn.bind("<Leave>", lambda e, b=btn, idx=i: b.config(
                fg=C_GOLD if idx == self.current_text_subpage else C_TEXT_DIM,
                highlightbackground=C_GOLD if idx == self.current_text_subpage else C_BG_MEDIUM))
            
            self.tab_buttons.append(btn)
        
        # 子界面容器
        self.subpage_container = tk.Frame(self, bg=C_VOID)
        self.subpage_container.pack(fill="both", expand=True, padx=2, pady=2)
        self.subpage_container.bind("<Button-1>", self.on_frame_click)
        
        # 创建所有子界面（带具体按键）
        self.create_subpages()
        
        # 默认显示第一个
        self.text_subpages[0].lift()
    
    def create_subpages(self):
        """创建5个子界面（带具体按键）"""
        self.text_subpages = {}
        
        # 界面0 - ACD界面
        page0 = tk.Frame(self.subpage_container, bg=C_VOID)
        page0.bind("<Button-1>", self.on_frame_click)
        self.create_acd_page_content(page0)
        page0.place(x=0, y=0, relwidth=1, relheight=1)
        self.text_subpages[0] = page0
        
        # 界面1 - B表界面
        page1 = tk.Frame(self.subpage_container, bg=C_VOID)
        page1.bind("<Button-1>", self.on_frame_click)
        self.create_bbiao_page_content(page1)
        page1.place(x=0, y=0, relwidth=1, relheight=1)
        page1.lower()
        self.text_subpages[1] = page1
        
        # 界面2 - 周X界面
        page2 = tk.Frame(self.subpage_container, bg=C_VOID)
        page2.bind("<Button-1>", self.on_frame_click)
        self.create_zhoux_page_content(page2)
        page2.place(x=0, y=0, relwidth=1, relheight=1)
        page2.lower()
        self.text_subpages[2] = page2
        
        # 界面3 - 周三界面
        page3 = tk.Frame(self.subpage_container, bg=C_VOID)
        page3.bind("<Button-1>", self.on_frame_click)
        self.create_zhou3_page_content(page3)
        page3.place(x=0, y=0, relwidth=1, relheight=1)
        page3.lower()
        self.text_subpages[3] = page3
        
        # 界面4 - 备用界面
        page4 = tk.Frame(self.subpage_container, bg=C_VOID)
        page4.bind("<Button-1>", self.on_frame_click)
        self.create_beiyong_page_content(page4)
        page4.place(x=0, y=0, relwidth=1, relheight=1)
        page4.lower()
        self.text_subpages[4] = page4
    
    def create_acd_page_content(self, parent):
        """创建ACD界面内容"""
        center_frame = tk.Frame(parent, bg=C_VOID)
        center_frame.bind("<Button-1>", self.on_frame_click)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # 第一排：APP任务，APP标题，APP内容
        row1 = tk.Frame(center_frame, bg=C_VOID)
        row1.pack(fill="x", pady=3)
        row1.bind("<Button-1>", self.on_frame_click)
        self.create_button(row1, "APP任务", lambda: self.on_btn_click("ACD", "APP任务"), "import", small=True)
        self.create_button(row1, "APP标题", lambda: self.on_btn_click("ACD", "APP标题"), "import", small=True)
        self.create_button(row1, "APP内容", lambda: self.on_btn_click("ACD", "APP内容"), "import", small=True)
        
        # 第二排：未提任务，未提标题，未提内容
        row2 = tk.Frame(center_frame, bg=C_VOID)
        row2.pack(fill="x", pady=3)
        row2.bind("<Button-1>", self.on_frame_click)
        self.create_button(row2, "未提任务", lambda: self.on_btn_click("ACD", "未提任务"), "start", small=True)
        self.create_button(row2, "未提标题", lambda: self.on_btn_click("ACD", "未提标题"), "start", small=True)
        self.create_button(row2, "未提内容", lambda: self.on_btn_click("ACD", "未提内容"), "start", small=True)
        
        # 第三排：30任务，100任务，1000任务，钱包标题，钱包内容
        row3 = tk.Frame(center_frame, bg=C_VOID)
        row3.pack(fill="x", pady=3)
        row3.bind("<Button-1>", self.on_frame_click)
        self.create_button(row3, "30任务", lambda: self.on_btn_click("ACD", "30任务"), "reset", small=True)
        self.create_button(row3, "100任务", lambda: self.on_btn_click("ACD", "100任务"), "reset", small=True)
        self.create_button(row3, "1000任务", lambda: self.on_btn_click("ACD", "1000任务"), "reset", small=True)
        self.create_button(row3, "钱包标题", lambda: self.on_btn_click("ACD", "钱包标题"), "reset", small=True)
        self.create_button(row3, "钱包内容", lambda: self.on_btn_click("ACD", "钱包内容"), "reset", small=True)
    
    def create_bbiao_page_content(self, parent):
        """创建B表界面内容"""
        center_frame = tk.Frame(parent, bg=C_VOID)
        center_frame.bind("<Button-1>", self.on_frame_click)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # 第一排：50任务，300任务
        row1 = tk.Frame(center_frame, bg=C_VOID)
        row1.pack(fill="x", pady=3)
        row1.bind("<Button-1>", self.on_frame_click)
        self.create_button(row1, "50任务", lambda: self.on_btn_click("B表", "50任务"), "import", small=True)
        self.create_button(row1, "300任务", lambda: self.on_btn_click("B表", "300任务"), "import", small=True)
        
        # 第二排：任务内容
        row2 = tk.Frame(center_frame, bg=C_VOID)
        row2.pack(fill="x", pady=3)
        row2.bind("<Button-1>", self.on_frame_click)
        task_content_btn = tk.Label(row2,
                                   text="任务内容",
                                   font=("微软雅黑", 11, "bold"),
                                   bg=BTN_START,
                                   fg=C_GOLD,
                                   padx=6, pady=7,
                                   cursor="",
                                   highlightthickness=1,
                                   highlightbackground=C_GOLD,
                                   highlightcolor=C_GOLD)
        task_content_btn.pack(side="left", fill="x", expand=True, padx=1)
        
        def on_enter(e):
            task_content_btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            task_content_btn.config(bg=BTN_START, fg=C_GOLD)
        
        task_content_btn.bind("<Enter>", on_enter)
        task_content_btn.bind("<Leave>", on_leave)
        task_content_btn.bind("<Button-1>", lambda e: self.on_btn_click("B表", "任务内容"))
        
        # 第三排：站内标题，站内任务
        row3 = tk.Frame(center_frame, bg=C_VOID)
        row3.pack(fill="x", pady=3)
        row3.bind("<Button-1>", self.on_frame_click)
        self.create_button(row3, "站内标题", lambda: self.on_btn_click("B表", "站内标题"), "reset", small=True)
        self.create_button(row3, "站内任务", lambda: self.on_btn_click("B表", "站内任务"), "reset", small=True)
    
    def create_zhoux_page_content(self, parent):
        """创建周X界面内容"""
        center_frame = tk.Frame(parent, bg=C_VOID)
        center_frame.bind("<Button-1>", self.on_frame_click)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # 第一排：任务标题
        row1 = tk.Frame(center_frame, bg=C_VOID)
        row1.pack(fill="x", pady=3)
        row1.bind("<Button-1>", self.on_frame_click)
        task_title_btn = tk.Label(row1,
                                 text="任务标题",
                                 font=("微软雅黑", 11, "bold"),
                                 bg=BTN_IMPORT,
                                 fg=C_GOLD,
                                 padx=6, pady=7,
                                 cursor="",
                                 highlightthickness=1,
                                 highlightbackground=C_GOLD,
                                 highlightcolor=C_GOLD)
        task_title_btn.pack(side="left", fill="x", expand=True, padx=1)
        
        def on_enter(e):
            task_title_btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            task_title_btn.config(bg=BTN_IMPORT, fg=C_GOLD)
        
        task_title_btn.bind("<Enter>", on_enter)
        task_title_btn.bind("<Leave>", on_leave)
        task_title_btn.bind("<Button-1>", lambda e: self.on_btn_click("周X", "任务标题"))
        
        # 第二排：站内标题，站内内容
        row2 = tk.Frame(center_frame, bg=C_VOID)
        row2.pack(fill="x", pady=3)
        row2.bind("<Button-1>", self.on_frame_click)
        self.create_button(row2, "站内标题", lambda: self.on_btn_click("周X", "站内标题"), "start", small=True)
        self.create_button(row2, "站内内容", lambda: self.on_btn_click("周X", "站内内容"), "start", small=True)
    
    def create_zhou3_page_content(self, parent):
        """创建周三界面内容"""
        center_frame = tk.Frame(parent, bg=C_VOID)
        center_frame.bind("<Button-1>", self.on_frame_click)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # 第一排：神秘彩金，神秘标题，神秘内容
        row1 = tk.Frame(center_frame, bg=C_VOID)
        row1.pack(fill="x", pady=3)
        row1.bind("<Button-1>", self.on_frame_click)
        self.create_button(row1, "神秘彩金", lambda: self.on_btn_click("周三", "神秘彩金"), "import", small=True)
        self.create_button(row1, "神秘标题", lambda: self.on_btn_click("周三", "神秘标题"), "import", small=True)
        self.create_button(row1, "神秘内容", lambda: self.on_btn_click("周三", "神秘内容"), "import", small=True)
        
        # 第二排：幸运彩金，幸运标题，幸运内容
        row2 = tk.Frame(center_frame, bg=C_VOID)
        row2.pack(fill="x", pady=3)
        row2.bind("<Button-1>", self.on_frame_click)
        self.create_button(row2, "幸运彩金", lambda: self.on_btn_click("周三", "幸运彩金"), "start", small=True)
        self.create_button(row2, "幸运标题", lambda: self.on_btn_click("周三", "幸运标题"), "start", small=True)
        self.create_button(row2, "幸运内容", lambda: self.on_btn_click("周三", "幸运内容"), "start", small=True)
    
    def create_beiyong_page_content(self, parent):
        """创建备用界面内容"""
        center_frame = tk.Frame(parent, bg=C_VOID)
        center_frame.bind("<Button-1>", self.on_frame_click)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # 第一排：周末标题，周末内容
        row1 = tk.Frame(center_frame, bg=C_VOID)
        row1.pack(fill="x", pady=3)
        row1.bind("<Button-1>", self.on_frame_click)
        self.create_button(row1, "周末标题", lambda: self.on_btn_click("备用", "周末标题"), "import", small=True)
        self.create_button(row1, "周末内容", lambda: self.on_btn_click("备用", "周末内容"), "import", small=True)
        
        # 第二排：红包标题，红包内容
        row2 = tk.Frame(center_frame, bg=C_VOID)
        row2.pack(fill="x", pady=3)
        row2.bind("<Button-1>", self.on_frame_click)
        self.create_button(row2, "红包标题", lambda: self.on_btn_click("备用", "红包标题"), "start", small=True)
        self.create_button(row2, "红包内容", lambda: self.on_btn_click("备用", "红包内容"), "start", small=True)
    
    def switch_subpage(self, index):
        """切换子界面"""
        self.current_text_subpage = index
        tab_names = ["ACD", "B表", "周X", "周3", "备用"]
        
        for i, btn in enumerate(self.tab_buttons):
            if i == index:
                btn.config(fg=C_GOLD, highlightbackground=C_GOLD)
            else:
                btn.config(fg=C_TEXT_DIM, highlightbackground=C_BG_MEDIUM)
        
        if index in self.text_subpages:
            self.text_subpages[index].lift()
            #self.app.add_log("系统", "文本控制", f"切换到【{tab_names[index]}】")
    
    def on_btn_click(self, page, btn_name):
        """按钮点击事件 - 复制对应输入框的内容"""
        # 构建输入框的键名
        entry_key = btn_name
        
        # 从CopySubpage中获取输入框引用
        if hasattr(self.app, 'current_page') and self.app.current_page == "数据中心":
            # 查找CopySubpage实例
            for page in self.app.pages.values():
                if hasattr(page, 'subpages'):
                    for subpage in page.subpages.values():
                        if hasattr(subpage, 'entries') and entry_key in subpage.entries:
                            entry = subpage.entries[entry_key]
                            content = entry.get()
                            if content:
                                self.app.clipboard_clear()
                                self.app.clipboard_append(content)
                                self.app.add_log("成功", "文本控制", f"已复制【{btn_name}】内容")
                            else:
                                self.app.add_log("警告", "文本控制", f"【{btn_name}】内容为空")
                            return
        
        self.app.add_log("系统", "文本控制", f"{page} - {btn_name} 被点击")
        print(f"{page} - {btn_name} 被点击")


class CopySubpage(tk.Frame):
    """按键复制子界面 - 3个区域布局"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.entries = {}
        self.lock_buttons = {}
        self.locked_states = {}  # 记录每个输入框的锁定状态
        self.create_widgets()
        
        # 绑定点击事件到整个框架，用于取消焦点
        self.bind("<Button-1>", self.on_frame_click)
    
    def on_frame_click(self, event):
        """点击框架时取消所有输入框的焦点"""
        # 获取当前拥有焦点的控件
        focused = self.focus_get()
        # 如果焦点在输入框上，移除焦点
        if focused and isinstance(focused, tk.Entry):
            self.focus_set()
    
    def create_widgets(self):
        """创建界面组件 - 3个区域布局"""
        # 主容器 - 使用PanedWindow实现左右可调分区
        main_paned = tk.PanedWindow(self, bg=C_VOID, sashwidth=4, sashrelief="flat",
                                    sashpad=0, showhandle=False, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 绑定点击事件到PanedWindow
        main_paned.bind("<Button-1>", self.on_frame_click)
        
        # ===== 3个区域等宽分布 =====
        # 区域1 (左侧)
        region1_container = tk.Frame(main_paned, bg=C_VOID)
        main_paned.add(region1_container, width=260, minsize=220)
        region1_container.bind("<Button-1>", self.on_frame_click)
        
        # 区域2 (中间)
        region2_container = tk.Frame(main_paned, bg=C_VOID)
        main_paned.add(region2_container, width=260, minsize=220)
        region2_container.bind("<Button-1>", self.on_frame_click)
        
        # 区域3 (右侧)
        region3_container = tk.Frame(main_paned, bg=C_VOID)
        main_paned.add(region3_container, width=260, minsize=220)
        region3_container.bind("<Button-1>", self.on_frame_click)
        
        # 为每个区域创建可滚动的内容区域
        self.create_region(region1_container, "1", [
            "APP任务", "APP标题", "APP内容",
            "未提任务", "未提标题", "未提内容",
            "30任务", "100任务", "1000任务", "钱包标题"
        ])
        
        self.create_region(region2_container, "2", [
            "钱包内容", "50任务", "300任务", "任务内容",
            "站内标题", "站内任务", "任务标题", "站内内容", "神秘彩金"
        ])
        
        self.create_region(region3_container, "3", [
            "神秘标题", "神秘内容", "幸运彩金",
            "幸运标题", "幸运内容", "周末标题",
            "周末内容", "红包标题", "红包内容"
        ])
    
    def create_region(self, parent, region_num, buttons):
        """创建单个区域 - 带滚动条的标签+输入框列表"""
        # 创建画布和滚动条
        canvas = tk.Canvas(parent, bg=C_VOID, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=C_VOID)
        
        # 绑定点击事件到画布和滚动区域
        canvas.bind("<Button-1>", self.on_frame_click)
        scrollbar.bind("<Button-1>", self.on_frame_click)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加区域序号标识（小数字）
        region_label = tk.Label(scrollable_frame,
                               text=f"区域 {region_num}",
                               font=("微软雅黑", 10),
                               bg=C_VOID,
                               fg=C_TEXT_DIM)
        region_label.pack(anchor="w", pady=(0, 8))
        region_label.bind("<Button-1>", self.on_frame_click)
        
        # 创建该区域的所有按钮行
        for btn_name in buttons:
            self.create_button_row(scrollable_frame, btn_name)
    
    def create_button_row(self, parent, btn_name):
        """创建一行：标签 + 输入框 + 锁定按钮"""
        row_frame = tk.Frame(parent, bg=C_VOID)
        row_frame.pack(fill="x", pady=3)
        row_frame.bind("<Button-1>", self.on_frame_click)
        
        # 标签
        label = tk.Label(row_frame,
                        text=btn_name,
                        font=("微软雅黑", 11),
                        bg=C_VOID,
                        fg=C_GOLD,
                        width=10,
                        anchor="w")
        label.pack(side="left", padx=(0, 8))
        label.bind("<Button-1>", self.on_frame_click)
        
        # 使用ClearableEntry组件替代普通Entry
        entry = ClearableEntry(row_frame, 
                              width=12,
                              bg_color=C_BG_MEDIUM,
                              text_color=C_GOLD)
        entry.pack(side="left", padx=(0, 8))
        
        # 存储输入框引用
        self.entries[btn_name] = entry
        self.locked_states[btn_name] = False  # 初始为未锁定
        
        # 锁定按钮 - 初始为解锁状态（锁图标）
        lock_btn = tk.Label(row_frame,
                           text="🔓",  # 解锁图标
                           font=("微软雅黑", 10, "bold"),
                           bg=BTN_RESET,
                           fg=C_GOLD,
                           padx=6, pady=3,
                           cursor="",
                           highlightthickness=1,
                           highlightbackground=C_GOLD,
                           highlightcolor=C_GOLD)
        lock_btn.pack(side="left")
        
        # 存储按钮引用
        self.lock_buttons[btn_name] = lock_btn
        
        # 按钮悬停效果
        def on_enter(e, btn=lock_btn):
            btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e, btn=lock_btn):
            btn.config(bg=BTN_RESET, fg=C_GOLD)
        
        lock_btn.bind("<Enter>", on_enter)
        lock_btn.bind("<Leave>", on_leave)
        lock_btn.bind("<Button-1>", lambda e, name=btn_name: self.toggle_lock(name))
    
    def toggle_lock(self, btn_name):
        """切换锁定/解锁状态"""
        entry = self.entries.get(btn_name)
        lock_btn = self.lock_buttons.get(btn_name)
        
        if not entry or not lock_btn:
            return
        
        current_state = self.locked_states.get(btn_name, False)
        
        if current_state:
            # 当前是锁定状态 -> 解锁
            entry.enable()  # ClearableEntry的enable方法
            lock_btn.config(text="🔓")  # 解锁图标
            self.locked_states[btn_name] = False
            self.app.add_log("系统", "按键复制", f"解锁【{btn_name}】")
            print(f"解锁 {btn_name}")
        else:
            # 当前是解锁状态 -> 锁定
            entry.set_readonly(True)  # ClearableEntry的set_readonly方法
            lock_btn.config(text="🔒")  # 锁定图标
            self.locked_states[btn_name] = True
            self.app.add_log("系统", "按键复制", f"锁定【{btn_name}】")
            print(f"锁定 {btn_name}")
        
        # 点击锁定按钮后移除焦点
        self.focus_set()
