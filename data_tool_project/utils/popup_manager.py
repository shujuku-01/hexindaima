# utils/popup_manager.py
import tkinter as tk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER

class PopupManager:
    """弹窗管理工具类"""
    
    def __init__(self, app):
        self.app = app
    
    def create_popup_base(self, title):
        """创建基础弹窗"""
        popup = tk.Toplevel(self.app)
        popup.transient(self.app)
        popup.overrideredirect(True)
        popup.configure(bg="#0A0A0A", highlightthickness=1, highlightbackground=C_GOLD)
        popup.attributes("-topmost", True)
        
        # 标题栏
        title_bar = tk.Frame(popup, bg=C_GOLD, height=35)
        title_bar.pack(fill="x", side="top")
        
        title_label = tk.Label(title_bar, text=title, bg=C_GOLD, fg="#000000", 
                               font=("微软雅黑", 14, "bold"))
        title_label.pack(expand=True)
        
        close_x = tk.Label(title_bar, text=" ✕ ", bg=C_GOLD, fg="#000000", 
                          font=("Arial", 14, "bold"))
        close_x.place(relx=1.0, rely=0.5, anchor="e", x=-5)
        
        def on_close(e=None):
            try:
                popup.grab_release()
                popup.withdraw()
                popup.destroy()
                self.app.after(50, lambda: self.app.focus_force())
            except:
                pass
        
        close_x.bind("<ButtonRelease-1>", on_close)
        
        # 拖动功能
        def start_move(e):
            popup._drag_x, popup._drag_y = e.x, e.y
        
        def on_drag(e):
            x = popup.winfo_x() + (e.x - popup._drag_x)
            y = popup.winfo_y() + (e.y - popup._drag_y)
            popup.geometry(f"+{x}+{y}")
        
        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", on_drag)
        
        content_frame = tk.Frame(popup, bg="#0A0A0A")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        def finalize_geometry():
            popup.update_idletasks()
            w, h = max(popup.winfo_reqwidth(), 320), max(popup.winfo_reqheight(), 160)
            mx, my, mw, mh = self.app.winfo_x(), self.app.winfo_y(), self.app.winfo_width(), self.app.winfo_height()
            popup.geometry(f"{w}x{h}+{mx + (mw - w) // 2}+{my + (mh - h) // 2}")
            popup.deiconify()
            popup.focus_force()
            try:
                popup.grab_set()
            except:
                pass
        
        return popup, content_frame, finalize_geometry, on_close
    
    def show_copy_popup(self, title, content):
        """
        显示可复制的弹窗 - 点击按钮复制并关闭
        """
        popup, frame, finalize, on_close = self.create_popup_base(title)
        
        # 内容文本
        text_widget = tk.Text(frame, bg="#0A0A0A", fg=C_GOLD, font=("微软雅黑", 12),
                              wrap="word", height=8, width=40, bd=0, highlightthickness=0)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        text_widget.pack(pady=10)
        
        # 按钮容器
        btn_frame = tk.Frame(frame, bg="#0A0A0A")
        btn_frame.pack(pady=10)
        
        # 复制并关闭按钮
        copy_btn = tk.Label(btn_frame, text="复制并关闭", font=("微软雅黑", 12, "bold"),
                           bg=C_GOLD, fg="#000000", padx=20, pady=5,
                           cursor="", highlightthickness=1, highlightbackground=C_GOLD)
        copy_btn.pack(side="left", padx=5)
        
        def on_copy_enter(e):
            copy_btn.config(bg=C_GOLD_LIGHT)
        
        def on_copy_leave(e):
            copy_btn.config(bg=C_GOLD)
        
        def on_copy_click(e):
            self.app.clipboard_clear()
            self.app.clipboard_append(content)
            self.app.add_log("成功", "弹窗", "内容已复制到剪贴板")
            on_close()
        
        copy_btn.bind("<Enter>", on_copy_enter)
        copy_btn.bind("<Leave>", on_copy_leave)
        copy_btn.bind("<Button-1>", on_copy_click)
        
        finalize()
    
    def show_info_popup(self, title, content):
        """
        显示信息弹窗 - 只有关闭按钮
        """
        popup, frame, finalize, on_close = self.create_popup_base(title)
        
        # 内容文本
        label = tk.Label(frame, text=content, fg=C_GOLD, bg="#0A0A0A", 
                        font=("微软雅黑", 12), wraplength=400)
        label.pack(pady=20)
        
        # 关闭按钮
        close_btn = tk.Label(frame, text="关闭", font=("微软雅黑", 12, "bold"),
                            bg=C_BG_MEDIUM, fg=C_GOLD, padx=30, pady=5,
                            cursor="", highlightthickness=1, highlightbackground=C_GOLD)
        close_btn.pack(pady=10)
        
        def on_close_enter(e):
            close_btn.config(bg=C_GOLD_LIGHT, fg="#000000")
        
        def on_close_leave(e):
            close_btn.config(bg=C_BG_MEDIUM, fg=C_GOLD)
        
        close_btn.bind("<Enter>", on_close_enter)
        close_btn.bind("<Leave>", on_close_leave)
        close_btn.bind("<Button-1>", lambda e: on_close())
        
        finalize()
    
    def show_confirm_popup(self, title, content, on_confirm, on_cancel=None):
        """
        显示确认弹窗 - 确认/取消按钮
        
        参数:
            title: 标题
            content: 内容
            on_confirm: 确认回调函数
            on_cancel: 取消回调函数（可选）
        """
        popup, frame, finalize, on_close = self.create_popup_base(title)
        
        # 内容文本
        label = tk.Label(frame, text=content, fg=C_GOLD, bg="#0A0A0A", 
                        font=("微软雅黑", 12), wraplength=400)
        label.pack(pady=20)
        
        # 按钮容器
        btn_frame = tk.Frame(frame, bg="#0A0A0A")
        btn_frame.pack(pady=10)
        
        # 确认按钮
        confirm_btn = tk.Label(btn_frame, text="确认", font=("微软雅黑", 12, "bold"),
                              bg="#8B0000", fg=C_GOLD, padx=20, pady=5,
                              cursor="", highlightthickness=1, highlightbackground=C_GOLD)
        confirm_btn.pack(side="left", padx=5)
        
        # 取消按钮
        cancel_btn = tk.Label(btn_frame, text="取消", font=("微软雅黑", 12, "bold"),
                             bg=C_BG_MEDIUM, fg=C_GOLD, padx=20, pady=5,
                             cursor="", highlightthickness=1, highlightbackground=C_GOLD)
        cancel_btn.pack(side="left", padx=5)
        
        def on_confirm_enter(e):
            confirm_btn.config(bg="#A52A2A", fg=C_GOLD_LIGHT)
        
        def on_confirm_leave(e):
            confirm_btn.config(bg="#8B0000", fg=C_GOLD)
        
        def on_cancel_enter(e):
            cancel_btn.config(bg=C_GOLD_LIGHT, fg="#000000")
        
        def on_cancel_leave(e):
            cancel_btn.config(bg=C_BG_MEDIUM, fg=C_GOLD)
        
        def on_confirm_click(e):
            on_close()
            if on_confirm:
                on_confirm()
        
        def on_cancel_click(e):
            on_close()
            if on_cancel:
                on_cancel()
        
        confirm_btn.bind("<Enter>", on_confirm_enter)
        confirm_btn.bind("<Leave>", on_confirm_leave)
        confirm_btn.bind("<Button-1>", on_confirm_click)
        
        cancel_btn.bind("<Enter>", on_cancel_enter)
        cancel_btn.bind("<Leave>", on_cancel_leave)
        cancel_btn.bind("<Button-1>", on_cancel_click)
        
        finalize()
