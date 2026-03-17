# pages/search.py
import tkinter as tk
from tkinter import ttk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER, BTN_RESET, BTN_IMPORT, BTN_START, BTN_HOVER
from widgets.gold_combobox import GoldCombobox, ClearableEntry
from pages.search_logic import SearchLogic

class SearchPage(tk.Frame):
    """综合搜索页面 - 只负责GUI布局"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.logic = SearchLogic(app)  # 业务逻辑统一入口
        self.entries = {}
        self.win_combo2 = None
        self.create_widgets()
        
        # 绑定页面点击事件
        self.bind("<Button-1>", self.on_page_click)
    
    def on_page_click(self, event):
        """点击页面空白处释放焦点"""
        focused = self.focus_get()
        if focused and isinstance(focused, tk.Entry) and event.widget != focused:
            self.focus_set()
    
    def create_button(self, parent, text, command, btn_type="default", width=None):
        """创建黑金风格按钮"""
        bg_color = {
            "reset": BTN_RESET,
            "import": BTN_IMPORT,
            "start": BTN_START,
            "query": C_GOLD,
            "red": "#8B0000",
            "upload": BTN_IMPORT
        }.get(btn_type, BTN_RESET)
        
        if btn_type == "query":
            fg_color = C_VOID
        elif btn_type == "red":
            fg_color = C_GOLD
        elif btn_type == "upload":
            fg_color = C_GOLD
        else:
            fg_color = C_GOLD
        
        btn = tk.Label(parent,
                      text=text,
                      font=("微软雅黑", 12, "bold"),
                      bg=bg_color,
                      fg=fg_color,
                      padx=5, pady=5,
                      cursor="",
                      highlightthickness=1,
                      highlightbackground=C_GOLD,
                      highlightcolor=C_GOLD,
                      width=width)
        btn.pack(side="left")
        
        def on_enter(e):
            if btn_type == "query":
                btn.config(bg=C_GOLD_LIGHT, fg=C_VOID)
            elif btn_type == "red":
                btn.config(bg="#A52A2A", fg=C_GOLD_LIGHT)
            else:
                btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            btn.config(bg=bg_color, fg=fg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e: command())
        
        return btn
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = tk.Frame(self, bg=C_VOID)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.bind("<Button-1>", self.on_page_click)
        
        # 创建三个区域容器
        region1_container = tk.Frame(main_frame, bg=C_VOID, width=270)
        region1_container.pack(side="left", fill="both", expand=True, padx=(0, 5))
        region1_container.pack_propagate(False)
        region1_container.bind("<Button-1>", self.on_page_click)
        
        region2_container = tk.Frame(main_frame, bg=C_VOID, width=270)
        region2_container.pack(side="left", fill="both", expand=True, padx=5)
        region2_container.pack_propagate(False)
        region2_container.bind("<Button-1>", self.on_page_click)
        
        region3_container = tk.Frame(main_frame, bg=C_VOID, width=270)
        region3_container.pack(side="left", fill="both", expand=True, padx=(5, 0))
        region3_container.pack_propagate(False)
        region3_container.bind("<Button-1>", self.on_page_click)
        
        # 区域1内容
        region1_frame = tk.Frame(region1_container, bg=C_VOID)
        region1_frame.pack(fill="both", expand=True)
        region1_frame.bind("<Button-1>", self.on_page_click)
        self.create_region1_content(region1_frame)
        
        # 区域2内容
        region2_frame = tk.Frame(region2_container, bg=C_VOID)
        region2_frame.pack(fill="both", expand=True)
        region2_frame.bind("<Button-1>", self.on_page_click)
        self.create_region2_content(region2_frame)
        
        # 区域3内容
        region3_frame = tk.Frame(region3_container, bg=C_VOID)
        region3_frame.pack(fill="both", expand=True)
        region3_frame.bind("<Button-1>", self.on_page_click)
        self.create_region3_content(region3_frame)
    
    def create_region1_content(self, parent):
        """区域1：午夜充值 + 电话回访 + 活跃VIP + 连赢查询"""
        content_frame = tk.Frame(parent, bg=C_VOID)
        content_frame.pack(expand=True, fill="both", padx=15, pady=15)
        content_frame.bind("<Button-1>", self.on_page_click)
        
        # 午夜充值
        midnight_row1 = tk.Frame(content_frame, bg=C_VOID)
        midnight_row1.pack(fill="x", pady=(0, 8))
        midnight_row1.bind("<Button-1>", self.on_page_click)
        tk.Label(midnight_row1, text="午夜充值", font=("微软雅黑", 14, "bold"), 
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        midnight_row2 = tk.Frame(content_frame, bg=C_VOID)
        midnight_row2.pack(fill="x", pady=(0, 20))
        midnight_row2.bind("<Button-1>", self.on_page_click)
        
        self.midnight_entry = ClearableEntry(midnight_row2, app=self.app, width=16,
                                            placeholder="请输入账号...")
        self.midnight_entry.entry.config(font=("微软雅黑", 12))
        self.midnight_entry.pack(side="left", padx=(0, 8))
        self.create_button(midnight_row2, "点击查询", self.on_midnight_query, "query", width=7)
        
        # 电话回访
        phone_row1 = tk.Frame(content_frame, bg=C_VOID)
        phone_row1.pack(fill="x", pady=(0, 8))
        phone_row1.bind("<Button-1>", self.on_page_click)
        tk.Label(phone_row1, text="电话回访", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        phone_row2 = tk.Frame(content_frame, bg=C_VOID)
        phone_row2.pack(fill="x", pady=(0, 20))
        phone_row2.bind("<Button-1>", self.on_page_click)
        
        self.phone_entry = ClearableEntry(phone_row2, app=self.app, width=16,
                                         placeholder="请输入电话号码...")
        self.phone_entry.entry.config(font=("微软雅黑", 12))
        self.phone_entry.pack(side="left", padx=(0, 8))
        self.create_button(phone_row2, "点击查询", self.on_phone_query, "query", width=7)
        
        # 活跃VIP
        vip_row1 = tk.Frame(content_frame, bg=C_VOID)
        vip_row1.pack(fill="x", pady=(0, 8))
        vip_row1.bind("<Button-1>", self.on_page_click)
        tk.Label(vip_row1, text="活跃VIP", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        vip_row2 = tk.Frame(content_frame, bg=C_VOID)
        vip_row2.pack(fill="x", pady=(0, 8))
        vip_row2.bind("<Button-1>", self.on_page_click)
        
        self.vip_entry = ClearableEntry(vip_row2, app=self.app, width=16,
                                       placeholder="请输入VIP等级...")
        self.vip_entry.entry.config(font=("微软雅黑", 12))
        self.vip_entry.pack(side="left", padx=(0, 8))
        self.create_button(vip_row2, "点击查询", self.on_vip_query, "query", width=7)
        
        vip_row3 = tk.Frame(content_frame, bg=C_VOID)
        vip_row3.pack(fill="x", pady=(8, 20))
        vip_row3.bind("<Button-1>", self.on_page_click)
        
        btn_15 = self.create_button(vip_row3, "15天", lambda: self.on_vip_days(15), "start")
        btn_15.config(padx=0)
        btn_15.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_30 = self.create_button(vip_row3, "30天", lambda: self.on_vip_days(30), "start")
        btn_30.config(padx=0)
        btn_30.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_60 = self.create_button(vip_row3, "60天", lambda: self.on_vip_days(60), "start")
        btn_60.config(padx=0)
        btn_60.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # 连赢查询
        win_row1 = tk.Frame(content_frame, bg=C_VOID)
        win_row1.pack(fill="x", pady=(0, 8))
        win_row1.bind("<Button-1>", self.on_page_click)
        tk.Label(win_row1, text="连赢查询", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        win_row2 = tk.Frame(content_frame, bg=C_VOID)
        win_row2.pack(fill="x", pady=(0, 8))
        win_row2.bind("<Button-1>", self.on_page_click)
        
        self.win_entry = ClearableEntry(win_row2, app=self.app, width=16,
                                       placeholder="请输入订单号...")
        self.win_entry.entry.config(font=("微软雅黑", 12))
        self.win_entry.pack(side="left", padx=(0, 8))
        self.create_button(win_row2, "点击查询", self.on_win_query, "query", width=7)
        
        win_row3 = tk.Frame(content_frame, bg=C_VOID)
        win_row3.pack(fill="x")
        win_row3.bind("<Button-1>", self.on_page_click)
        
        self.win_combo1 = GoldCombobox(win_row3, values=["棋牌", "真人"], width=5, default="棋牌")
        self.win_combo1.pack(side="left", padx=(0, 5))
        self.win_combo2 = GoldCombobox(win_row3, values=[], width=5, default="")
        self.win_combo1.bind("<<ComboboxSelected>>", self.on_win_combo1_select)
        
        # 存储输入框引用
        self.entries.update({
            "midnight": self.midnight_entry,
            "phone": self.phone_entry,
            "vip": self.vip_entry,
            "win": self.win_entry
        })
    
    def create_region2_content(self, parent):
        """区域2：PG1计算 + 迎新活动"""
        content_frame = tk.Frame(parent, bg=C_VOID)
        content_frame.pack(expand=True, fill="both", padx=15, pady=15)
        content_frame.bind("<Button-1>", self.on_page_click)
        
        # PG1计算
        pg_title = tk.Frame(content_frame, bg=C_VOID)
        pg_title.pack(fill="x", pady=(0, 15))
        pg_title.bind("<Button-1>", self.on_page_click)
        tk.Label(pg_title, text="PG1计算", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        account_row = tk.Frame(content_frame, bg=C_VOID)
        account_row.pack(fill="x", pady=(0, 10))
        account_row.bind("<Button-1>", self.on_page_click)
        tk.Label(account_row, text="会员账号", font=("微软雅黑", 12), fg=C_TEXT_DIM,
                bg=C_VOID, width=8, anchor="w").pack(side="left")
        
        self.pg_account_entry = ClearableEntry(account_row, app=self.app, width=16,
                                              placeholder="请输入账号...")
        self.pg_account_entry.entry.config(font=("微软雅黑", 12))
        self.pg_account_entry.pack(side="left", padx=(0, 8))
        
        bet_row = tk.Frame(content_frame, bg=C_VOID)
        bet_row.pack(fill="x", pady=(0, 10))
        bet_row.bind("<Button-1>", self.on_page_click)
        tk.Label(bet_row, text="投注金额", font=("微软雅黑", 12), fg=C_TEXT_DIM,
                bg=C_VOID, width=8, anchor="w").pack(side="left")
        
        self.pg_bet_entry = ClearableEntry(bet_row, app=self.app, width=16,
                                          placeholder="请输入金额...")
        self.pg_bet_entry.entry.config(font=("微软雅黑", 12))
        self.pg_bet_entry.pack(side="left", padx=(0, 8))
        
        total_row = tk.Frame(content_frame, bg=C_VOID)
        total_row.pack(fill="x", pady=(0, 15))
        total_row.bind("<Button-1>", self.on_page_click)
        tk.Label(total_row, text="总注单量", font=("微软雅黑", 12), fg=C_TEXT_DIM,
                bg=C_VOID, width=8, anchor="w").pack(side="left")
        
        self.pg_total_entry = ClearableEntry(total_row, app=self.app, width=16,
                                            placeholder="请输入注单量...")
        self.pg_total_entry.entry.config(font=("微软雅黑", 12))
        self.pg_total_entry.pack(side="left", padx=(0, 8))
        
        btn_row = tk.Frame(content_frame, bg=C_VOID)
        btn_row.pack(fill="x", pady=(0, 25))
        btn_row.bind("<Button-1>", self.on_page_click)
        
        pg_btn = tk.Label(btn_row, text="PG计算", font=("微软雅黑", 12, "bold"),
                         bg="#8B0000", fg=C_GOLD, padx=5, pady=5, cursor="",
                         highlightthickness=1, highlightbackground=C_GOLD, highlightcolor=C_GOLD)
        pg_btn.pack(fill="x")
        
        def on_enter(e): pg_btn.config(bg="#A52A2A", fg=C_GOLD_LIGHT)
        def on_leave(e): pg_btn.config(bg="#8B0000", fg=C_GOLD)
        
        pg_btn.bind("<Enter>", on_enter)
        pg_btn.bind("<Leave>", on_leave)
        pg_btn.bind("<Button-1>", lambda e: self.on_pg_calc())
        
        # 迎新活动
        welcome_title = tk.Frame(content_frame, bg=C_VOID)
        welcome_title.pack(fill="x", pady=(0, 15))
        welcome_title.bind("<Button-1>", self.on_page_click)
        tk.Label(welcome_title, text="迎新活动", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        welcome_row1 = tk.Frame(content_frame, bg=C_VOID)
        welcome_row1.pack(fill="x", pady=(0, 10))
        welcome_row1.bind("<Button-1>", self.on_page_click)
        
        self.welcome_entry1 = ClearableEntry(welcome_row1, app=self.app, width=16,
                                            placeholder="请输入账号...")
        self.welcome_entry1.entry.config(font=("微软雅黑", 12))
        self.welcome_entry1.pack(side="left", padx=(0, 8))
        
        self.welcome_combo = GoldCombobox(welcome_row1,
                                         values=["签到成就", "投注成就", "全勤成就", "钱包成就",
                                                "晋级成就", "电子成就", "捕鱼成就", "棋牌成就",
                                                "视讯成就", "充值成就", "任务成就"],
                                         width=10, default="签到成就")
        self.welcome_combo.pack(side="left")
        
        welcome_row2 = tk.Frame(content_frame, bg=C_VOID)
        welcome_row2.pack(fill="x")
        welcome_row2.bind("<Button-1>", self.on_page_click)
        
        self.welcome_entry2 = ClearableEntry(welcome_row2, app=self.app, width=16,
                                            placeholder="请输入注单量...")
        self.welcome_entry2.entry.config(font=("微软雅黑", 12))
        self.welcome_entry2.pack(side="left", padx=(0, 8))
        self.create_button(welcome_row2, "点击查询", self.on_welcome_query, "red", width=7)
        
        self.entries.update({
            "pg_account": self.pg_account_entry,
            "pg_bet": self.pg_bet_entry,
            "pg_total": self.pg_total_entry,
            "welcome1": self.welcome_entry1,
            "welcome2": self.welcome_entry2
        })
    
    def create_region3_content(self, parent):
        """区域3：短信特邀 + 活动查询 + 上传数据"""
        content_frame = tk.Frame(parent, bg=C_VOID)
        content_frame.pack(expand=True, fill="both", padx=15, pady=15)
        content_frame.bind("<Button-1>", self.on_page_click)
        
        # 短信特邀
        sms_title = tk.Frame(content_frame, bg=C_VOID)
        sms_title.pack(fill="x", pady=(0, 15))
        sms_title.bind("<Button-1>", self.on_page_click)
        tk.Label(sms_title, text="短信特邀", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        sms_row1 = tk.Frame(content_frame, bg=C_VOID)
        sms_row1.pack(fill="x", pady=(0, 10))
        sms_row1.bind("<Button-1>", self.on_page_click)
        
        self.sms_entry1 = ClearableEntry(sms_row1, app=self.app, width=16,
                                        placeholder="请输入手机号...")
        self.sms_entry1.entry.config(font=("微软雅黑", 12))
        self.sms_entry1.pack(side="left", padx=(0, 8))
        
        self.sms_combo = GoldCombobox(sms_row1,
                                     values=["第一周", "第二周", "第三周", "第四周", "第五周", "第六周"],
                                     width=8, default="第一周")
        self.sms_combo.pack(side="left")
        
        sms_row2 = tk.Frame(content_frame, bg=C_VOID)
        sms_row2.pack(fill="x", pady=(0, 20))
        sms_row2.bind("<Button-1>", self.on_page_click)
        
        self.sms_entry2 = ClearableEntry(sms_row2, app=self.app, width=16,
                                        placeholder="YYYY-MM-DD")
        self.sms_entry2.entry.config(font=("微软雅黑", 12))
        self.sms_entry2.pack(side="left", padx=(0, 8))
        self.create_button(sms_row2, "计算日期", self.on_sms_calc, "query", width=7)
        
        # 活动查询
        activity_title = tk.Frame(content_frame, bg=C_VOID)
        activity_title.pack(fill="x", pady=(0, 15))
        activity_title.bind("<Button-1>", self.on_page_click)
        tk.Label(activity_title, text="活动查询", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        activity_row = tk.Frame(content_frame, bg=C_VOID)
        activity_row.pack(fill="x", pady=(0, 20))
        activity_row.bind("<Button-1>", self.on_page_click)
        
        self.activity_entry = ClearableEntry(activity_row, app=self.app, width=16,
                                            placeholder="请输入账号...")
        self.activity_entry.entry.config(font=("微软雅黑", 12))
        self.activity_entry.pack(side="left", padx=(0, 8))
        self.create_button(activity_row, "点击查询", self.on_activity_query, "query", width=7)
        
        # 上传数据
        upload_title = tk.Frame(content_frame, bg=C_VOID)
        upload_title.pack(fill="x", pady=(0, 15))
        upload_title.bind("<Button-1>", self.on_page_click)
        tk.Label(upload_title, text="上传数据", font=("微软雅黑", 14, "bold"),
                fg=C_GOLD, bg=C_VOID, anchor="w").pack(fill="x")
        
        upload_row = tk.Frame(content_frame, bg=C_VOID)
        upload_row.pack(fill="x")
        upload_row.bind("<Button-1>", self.on_page_click)
        
        self.upload_entry = ClearableEntry(upload_row, app=self.app, width=16,
                                          placeholder="请输入内容...")
        self.upload_entry.entry.config(font=("微软雅黑", 12))
        self.upload_entry.pack(side="left", padx=(0, 8))
        self.create_button(upload_row, "上传数据", self.on_upload, "upload", width=7)
        
        self.entries.update({
            "sms1": self.sms_entry1,
            "sms2": self.sms_entry2,
            "activity": self.activity_entry,
            "upload": self.upload_entry
        })
    
    # ========== 事件处理方法（调用业务逻辑）==========
    
    def on_win_combo1_select(self, event):
        self.win_combo2 = self.logic.win.on_combo1_select(self.win_combo1, self.win_combo2)
    
    def on_midnight_query(self):
        self.logic.midnight.query(self.midnight_entry.get())
    
    def on_phone_query(self):
        self.logic.phone.query(self.phone_entry.get())
    
    def on_vip_query(self):
        self.logic.vip.query(self.vip_entry.get())
    
    def on_vip_days(self, days):
        self.logic.vip.days_query(days)
    
    def on_win_query(self):
        value = self.win_entry.get()
        combo1 = self.win_combo1.get()
        combo2 = self.win_combo2.get() if self.win_combo2 and self.win_combo2.winfo_ismapped() else "未选择"
        self.logic.win.query(value, combo1, combo2)
    
    def on_pg_calc(self):
        self.logic.pg.calculate(
            self.pg_account_entry.get(),
            self.pg_bet_entry.get(),
            self.pg_total_entry.get()
        )
    
    def on_welcome_query(self):
        self.logic.welcome.query(
            self.welcome_entry1.get(),
            self.welcome_combo.get(),
            self.welcome_entry2.get()
        )
    
    def on_sms_calc(self):
        self.logic.sms.calculate(
            self.sms_entry1.get(),
            self.sms_combo.get(),
            self.sms_entry2.get()
        )
    
    def on_activity_query(self):
        self.logic.activity.query(self.activity_entry.get())
    
    def on_upload(self):
        self.logic.upload.upload(self.upload_entry.get())
