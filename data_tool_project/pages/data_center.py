# pages/data_center.py
import tkinter as tk
from config import C_VOID, C_BG_MEDIUM, C_GOLD, C_TEXT_DIM, DATA_CENTER_SUBPAGES
from pages.data_center_subpages import FilterSubpage, CopySubpage, PlaceholderSubpage

class DataCenterPage(tk.Frame):
    """数据中心主页面"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.current_subpage = 0
        self.subpages = {}
        self.subpage_labels = []
        
        # 创建3个子界面容器
        self.create_subpages()
        
        # 默认显示第一个子界面
        self.switch_subpage(0)
    
    def create_subpages(self):
        """创建3个子界面容器"""
        # 表格筛选子界面
        filter_subpage = FilterSubpage(self, self.app)
        filter_subpage.place(x=0, y=0, relwidth=1, relheight=1)
        filter_subpage.lower()
        self.subpages["表格筛选"] = filter_subpage
        
        # 按键复制子界面
        copy_subpage = CopySubpage(self, self.app)
        copy_subpage.place(x=0, y=0, relwidth=1, relheight=1)
        copy_subpage.lower()
        self.subpages["按键复制"] = copy_subpage
        
        # 备用功能子界面
        placeholder_subpage = PlaceholderSubpage(self, self.app, "备用功能")
        placeholder_subpage.place(x=0, y=0, relwidth=1, relheight=1)
        placeholder_subpage.lower()
        self.subpages["备用功能"] = placeholder_subpage
    
    def show_subnav(self, parent):
        """在核心系统右侧显示子导航标签"""
        # 清空父容器
        for widget in parent.winfo_children():
            widget.destroy()
        
        # 创建子导航标签
        self.subpage_labels = []
        
        for i, name in enumerate(DATA_CENTER_SUBPAGES):
            label = tk.Label(parent,
                           text=name,
                           font=("微软雅黑", 11),
                           bg=C_BG_MEDIUM,
                           fg=C_GOLD if i == self.current_subpage else C_TEXT_DIM,
                           padx=15, pady=5)
            label.pack(side="left", padx=2)
            label.bind("<Button-1>", lambda e, idx=i: self.on_subpage_click(idx))
            self.subpage_labels.append(label)
    
    def on_subpage_click(self, index):
        """子导航点击事件"""
        self.current_subpage = index
        selected = DATA_CENTER_SUBPAGES[index]
        
        # 更新标签颜色
        for i, label in enumerate(self.subpage_labels):
            if i == index:
                label.config(fg=C_GOLD)
            else:
                label.config(fg=C_TEXT_DIM)
        
        # 切换子界面
        for name, subpage in self.subpages.items():
            if name == selected:
                subpage.lift()
                #self.app.add_log("系统", "子界面切换", f"【{selected}】")
                break
    
    def switch_subpage(self, index):
        """切换子界面（内部调用）"""
        self.current_subpage = index
        selected = DATA_CENTER_SUBPAGES[index]
        
        # 切换子界面
        for name, subpage in self.subpages.items():
            if name == selected:
                subpage.lift()
                break
