# pages/inspection.py
import tkinter as tk
from config import C_VOID

class InspectionPage(tk.Frame):
    """检测合格页面"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=C_VOID)
        self.app = app
        # 页面内容为空，但确保Frame可见
