# pages/data_center_subpages/placeholder_subpage.py
import tkinter as tk
from config import C_VOID, C_GOLD, C_TEXT_DIM, C_BORDER

class PlaceholderSubpage(tk.Frame):
    """备用功能子界面"""
    def __init__(self, parent, app, name):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        self.name = name
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        center_frame = tk.Frame(self, bg=C_VOID)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(center_frame,
                text=f"📦 {self.name}",
                font=("微软雅黑", 22, "bold"),
                bg=C_VOID,
                fg=C_GOLD).pack(pady=15)
        
        tk.Label(center_frame,
                text="预留功能模块",
                font=("微软雅黑", 14),
                bg=C_VOID,
                fg=C_TEXT_DIM).pack(pady=10)
        
        tk.Frame(center_frame, height=2, width=350, bg=C_BORDER).pack(pady=25)
        
        tk.Label(center_frame,
                text="🚧 功能开发中",
                font=("微软雅黑", 12),
                bg=C_VOID,
                fg=C_TEXT_DIM).pack()
