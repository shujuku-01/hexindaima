# pages/data_center_subpages/filter_subpage.py
import tkinter as tk
from tkinter import ttk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER, BTN_RESET, BTN_IMPORT, BTN_START, BTN_HOVER, C_SUCCESS, C_ERROR
from widgets.gold_combobox import GoldCombobox
from pages.data_center_subpages.copy_subpage import TextControlPanel

class FilterSubpage(tk.Frame):
    """表格筛选子界面（左1右2布局）"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.import_labels = {}  # 存储标签引用
        self.import_status_labels = {}  # 存储状态标签的引用
        self.abcd_status_label = None  # ABCD表格状态标签
        self.bh3_status_label = None   # BH3表格状态标签
        self.percent_combo = None
        self.create_widgets()
    
    def create_button(self, parent, text, command, btn_type="default", width=None, small=False):
        """创建黑金风格按钮"""
        bg_color = {
            "reset": "#8B0000",  # 深红色
            "import": BTN_IMPORT,
            "start": BTN_START
        }.get(btn_type, BTN_RESET)
        
        if small:
            padx_val = 4
            pady_val = 3
            font_size = 9
        else:
            padx_val = 10
            pady_val = 8
            font_size = 11
        
        btn = tk.Label(parent,
                      text=text,
                      font=("微软雅黑", font_size, "bold"),
                      bg=bg_color,
                      fg=C_GOLD,
                      padx=padx_val, pady=pady_val,
                      cursor="",
                      highlightthickness=1,
                      highlightbackground=C_GOLD,
                      highlightcolor=C_GOLD,
                      width=width)
        btn.pack(side="left", fill="x", expand=True, padx=1)
        
        def on_enter(e):
            if btn_type == "reset":
                btn.config(bg="#A52A2A", fg=C_GOLD_LIGHT)  # 深红色悬停变亮
            else:
                btn.config(bg=BTN_HOVER, fg=C_GOLD_LIGHT)
        
        def on_leave(e):
            btn.config(bg=bg_color, fg=C_GOLD)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e: command())
        
        return btn
    
    def on_label_click(self, tag):
        """标签点击事件 - 导入表格"""
        if not hasattr(self.app, 'file_importer'):
            self.app.add_log("错误", "系统", "文件导入模块未初始化")
            return
        
        if not hasattr(self.app, 'data_vault'):
            self.app.data_vault = {}
        if not hasattr(self.app, 'M1_data_storage'):
            self.app.M1_data_storage = {}
        
        # 创建虚拟按钮用于状态更新
        dummy_btn = tk.Label(self)
        
        self.app.file_importer.import_single(
            tag=tag,
            btn_widget=dummy_btn,
            scope="ALPHA",
            data_vault=self.app.data_vault,
            m1_storage=self.app.M1_data_storage,
            callback=self.on_import_complete
        )
    
    def on_import_complete(self, tag, df):
        """导入完成回调 - 更新标签颜色和状态"""
        if tag in self.import_labels:
            label = self.import_labels[tag]
            # 标签文字变绿色
            label.config(fg=C_SUCCESS)
            
            # 更新状态标签
            if tag in self.import_status_labels:
                status_label = self.import_status_labels[tag]
                status_label.config(text=f"已选择({len(df)}行)", fg=C_SUCCESS)
    
    def on_batch_import_abcd(self):
        """ABCD表格批量导入"""
        if not hasattr(self.app, 'file_importer'):
            self.app.add_log("错误", "系统", "文件导入模块未初始化")
            return
        
        target_list = [
            "A表充值未提", "A表站内信",
            "B表50任务", "B表300任务", "B表站内信",
            "C表未使用APP", "C表站内信",
            "D表30钱包", "D表100钱包", "D表1000钱包", "D表站内信"
        ]
        
        self.app.add_log("系统", "批量导入", "开始批量导入 ABCD 表格...")
        
        # 调用统一的批量导入方法
        self.app.file_importer.batch_import(
            target_list=target_list,
            import_labels=self.import_labels,
            import_status_labels=self.import_status_labels,
            abcd_status_label=self.abcd_status_label,
            batch_name="ABCD"
        )
    
    def on_batch_import_bh3(self):
        """BH3表格批量导入"""
        if not hasattr(self.app, 'file_importer'):
            self.app.add_log("错误", "系统", "文件导入模块未初始化")
            return
        
        target_list = [
            "B表50任务", "B表300任务", "B表站内信",
            "H表任务", "H表站内信",
            "3神秘彩金", "3幸运彩金", "3神秘站内信", "3幸运站内信"
        ]
        
        self.app.add_log("系统", "批量导入", "开始批量导入 BH3 表格...")
        
        # 调用统一的批量导入方法
        self.app.file_importer.batch_import(
            target_list=target_list,
            import_labels=self.import_labels,
            import_status_labels=self.import_status_labels,
            bh3_status_label=self.bh3_status_label,
            batch_name="BH3"
        )
    
    def on_reset_click(self):
        """重置数据按钮点击事件 - 清空所有导入的表格"""
        # 清空数据存储
        if hasattr(self.app, 'data_vault'):
            # 清空左侧标签的状态
            for tag in self.import_labels:
                self.import_labels[tag].config(fg=C_TEXT_DIM)
            for tag in self.import_status_labels:
                self.import_status_labels[tag].config(text="", fg=C_SUCCESS)
            
            # 清空ABCD和BH3状态标签
            if self.abcd_status_label:
                self.abcd_status_label.config(text="0/11", fg=C_GOLD)
            if self.bh3_status_label:
                self.bh3_status_label.config(text="0/9", fg=C_GOLD)
            
            # 清空data_vault
            self.app.data_vault.clear()
            
            # 清空M1_data_storage
            if hasattr(self.app, 'M1_data_storage'):
                self.app.M1_data_storage.clear()
            
            self.app.add_log("系统", "核心控制", "所有数据已重置")
        else:
            self.app.add_log("警告", "核心控制", "没有数据可重置")
        
        print("重置所有数据")
    
    def on_start_all(self):
        """核心启动(全部)按钮点击事件"""
        percent = self.percent_combo.get_value()
        # 检查核心引擎是否存在
        if not hasattr(self.app, 'core_engine'):
            self.app.add_log("错误", "核心控制", "核心引擎未初始化")
            return
        self.app.add_log("执行", "核心控制", f"核心启动(全部) - 比例: {percent}")
        # 执行表格筛选逻辑
        self.app.core_engine.execute_alpha(percent)

    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器 - 使用固定宽度的paned window
        main_paned = tk.PanedWindow(self, bg=C_VOID, sashwidth=2, sashrelief="flat",
                                    sashpad=0, showhandle=False, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ===== 左侧区域 (固定40%宽度) =====
        left_container = tk.Frame(main_paned, bg=C_VOID, width=300)
        main_paned.add(left_container, width=300, minsize=250)
        
        # 左侧标题
        left_title_frame = tk.Frame(left_container, bg=C_VOID, height=25)
        left_title_frame.pack(fill="x", pady=(0, 5))
        left_title_frame.pack_propagate(False)
        
        tk.Label(left_title_frame,
                text="📥 数据导入",
                font=("微软雅黑", 12, "bold"),
                bg=C_VOID,
                fg=C_GOLD).pack(anchor="w")
        
        # 左侧内容区域
        left_frame = tk.Frame(left_container, bg=C_VOID)
        left_frame.pack(fill="both", expand=True)
        
        # 创建内容容器
        left_content = tk.Frame(left_frame, bg=C_VOID)
        left_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 所有标签
        label_font = ("微软雅黑", 11)
        status_font = ("微软雅黑", 10, "bold")
        
        all_labels = [
            "昨日首存", "昨日充值", "昨日登录", "充值未提", "总表未提",
            "原始数据B", "原始数据H", "原始数据3", 
            "备用标签1", "备用标签2", "备用标签3"
        ]
        
        for label_text in all_labels:
            row_frame = tk.Frame(left_content, bg=C_VOID)
            row_frame.pack(fill="x", pady=6)
            
            # 左侧标签
            label = tk.Label(row_frame,
                           text=label_text,
                           font=label_font,
                           bg=C_VOID,
                           fg=C_TEXT_DIM,
                           anchor="w")
            label.pack(side="left")
            
            # 右侧状态标签
            status_label = tk.Label(row_frame,
                                   text="",
                                   font=status_font,
                                   bg=C_VOID,
                                   fg=C_SUCCESS,
                                   anchor="e")
            status_label.pack(side="right", padx=(10, 0))
            
            # 绑定点击事件
            label.bind("<Button-1>", lambda e, t=label_text: self.on_label_click(t))
            
            # 悬停效果
            label.bind("<Enter>", lambda e, l=label: l.config(fg=C_GOLD_LIGHT))
            label.bind("<Leave>", lambda e, l=label, t=label_text: l.config(
                fg=C_SUCCESS if hasattr(self.app, 'data_vault') and 
                               t in self.app.data_vault and 
                               self.app.data_vault[t] is not None 
                          else C_TEXT_DIM
            ))
            
            self.import_labels[label_text] = label
            self.import_status_labels[label_text] = status_label
            
            # 检查是否已有数据
            if hasattr(self.app, 'data_vault') and label_text in self.app.data_vault and self.app.data_vault[label_text] is not None:
                df = self.app.data_vault[label_text]
                label.config(fg=C_SUCCESS)
                status_label.config(text=f"已选择({len(df)}行)", fg=C_SUCCESS)
        
        # ===== 右侧区域 =====
        right_container = tk.Frame(main_paned, bg=C_VOID, width=450)
        main_paned.add(right_container, width=450, minsize=400)
        
        # 右侧使用垂直分割
        right_paned = tk.PanedWindow(right_container, bg=C_VOID, sashwidth=2,
                                     sashrelief="flat", sashpad=0, showhandle=False,
                                     orient=tk.VERTICAL)
        right_paned.pack(fill="both", expand=True)
        
        # ===== 右上区域 (数据导出) =====
        top_container = tk.Frame(right_paned, bg=C_VOID)
        right_paned.add(top_container, height=120, minsize=100)
        
        # 右上标题
        top_title_frame = tk.Frame(top_container, bg=C_VOID, height=25)
        top_title_frame.pack(fill="x", pady=(0, 5))
        top_title_frame.pack_propagate(False)
        
        tk.Label(top_title_frame,
                text="📤 数据导出",
                font=("微软雅黑", 12, "bold"),
                bg=C_VOID,
                fg=C_GOLD).pack(anchor="w")
        
        # 右上内容区域
        right_top = tk.Frame(top_container, bg=C_VOID)
        right_top.pack(fill="both", expand=True)
        
        # 创建垂直居中容器
        top_center = tk.Frame(right_top, bg=C_VOID)
        top_center.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)
        
        # ABCD表格行
        row1 = tk.Frame(top_center, bg=C_VOID)
        row1.pack(fill="x", pady=5)
        
        abcd_label = tk.Label(row1,
                             text="ABCD表格",
                             font=("微软雅黑", 12),
                             bg=C_VOID,
                             fg=C_GOLD,
                             cursor="hand2")
        abcd_label.pack(side="left", padx=8)
        
        # 绑定批量导入事件
        abcd_label.bind("<Button-1>", lambda e: self.on_batch_import_abcd())
        
        # 悬停效果
        abcd_label.bind("<Enter>", lambda e, l=abcd_label: l.config(fg=C_GOLD_LIGHT))
        abcd_label.bind("<Leave>", lambda e, l=abcd_label: l.config(fg=C_GOLD))
        
        self.abcd_status_label = tk.Label(row1,
                                         text="0/11",
                                         font=("微软雅黑", 11, "bold"),
                                         bg=C_VOID,
                                         fg=C_GOLD)
        self.abcd_status_label.pack(side="right", padx=8)
        
        # BH3表格行
        row2 = tk.Frame(top_center, bg=C_VOID)
        row2.pack(fill="x", pady=5)
        
        bh3_label = tk.Label(row2,
                            text="BH3表格",
                            font=("微软雅黑", 12),
                            bg=C_VOID,
                            fg=C_GOLD,
                            cursor="hand2")
        bh3_label.pack(side="left", padx=8)
        
        # 绑定批量导入事件
        bh3_label.bind("<Button-1>", lambda e: self.on_batch_import_bh3())
        
        # 悬停效果
        bh3_label.bind("<Enter>", lambda e, l=bh3_label: l.config(fg=C_GOLD_LIGHT))
        bh3_label.bind("<Leave>", lambda e, l=bh3_label: l.config(fg=C_GOLD))
        
        self.bh3_status_label = tk.Label(row2,
                                        text="0/9",
                                        font=("微软雅黑", 11, "bold"),
                                        bg=C_VOID,
                                        fg=C_GOLD)
        self.bh3_status_label.pack(side="right", padx=8)
        
        # ===== 右下区域 (核心控制) =====
        bottom_container = tk.Frame(right_paned, bg=C_VOID)
        right_paned.add(bottom_container, height=140, minsize=120)
        
        # 右下标题
        bottom_title_frame = tk.Frame(bottom_container, bg=C_VOID, height=25)
        bottom_title_frame.pack(fill="x", pady=(0, 5))
        bottom_title_frame.pack_propagate(False)
        
        tk.Label(bottom_title_frame,
                text="⚙️ 核心控制",
                font=("微软雅黑", 12, "bold"),
                bg=C_VOID,
                fg=C_GOLD).pack(anchor="w")
        
        # 右下内容区域
        right_bottom = tk.Frame(bottom_container, bg=C_VOID)
        right_bottom.pack(fill="both", expand=True)
        
        # 创建主容器 - 使用垂直居中
        bottom_center = tk.Frame(right_bottom, bg=C_VOID)
        bottom_center.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)
        
        # 第一行：选择框 + 重置数据
        row1 = tk.Frame(bottom_center, bg=C_VOID)
        row1.pack(fill="x", pady=4)
        
        # 选择框（左侧）- 减小宽度
        select_frame = tk.Frame(row1, bg=C_VOID)
        select_frame.pack(side="left")
        
        tk.Label(select_frame,
                text="比例选择:",
                font=("微软雅黑", 11),
                bg=C_VOID,
                fg=C_GOLD).pack(side="left", padx=5)
        
        self.percent_combo = GoldCombobox(select_frame, width=4, default="20%")  # 宽度从8减小到6
        self.percent_combo.pack(side="left", padx=3)
        
        # 重置数据按钮（右侧）- 加大宽度，深红色
        reset_btn = self.create_button(row1, "重置数据", self.on_reset_click, "reset")
        reset_btn.config(padx=15, pady=2)  # 加大按钮
        reset_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # 第二行：核心启动(全部)
        row2 = tk.Frame(bottom_center, bg=C_VOID)
        row2.pack(fill="x", pady=4)
        
        # 核心启动(全部) - 占满整行
        start_all_btn = self.create_button(row2, "核心启动(全部)", self.on_start_all, "start")
        start_all_btn.pack(side="left", fill="x", expand=True)
        
        # ===== 文本控制区域 =====
        text_container = tk.Frame(right_paned, bg=C_VOID)
        right_paned.add(text_container, height=560, minsize=520)
        
        # 创建文本控制面板实例
        self.text_control_panel = TextControlPanel(text_container, self.app)
        self.text_control_panel.pack(fill="both", expand=True)
