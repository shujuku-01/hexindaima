# widgets/gold_combobox.py
import tkinter as tk
from tkinter import ttk
from config import C_VOID, C_GOLD, C_GOLD_LIGHT, C_BG_MEDIUM, C_TEXT_DIM, C_BORDER

class GoldCombobox(ttk.Combobox):
    """黑金风格的选择框组件 - 固定金色箭头"""
    
    def __init__(self, parent, values=None, width=8, default="20%", **kwargs):
        # 创建样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置黑金样式 - 箭头颜色固定为金色
        style.configure(
            "Gold.TCombobox",
            fieldbackground=C_BG_MEDIUM,  # 输入框背景
            background=C_BG_MEDIUM,        # 下拉按钮背景
            foreground=C_GOLD,              # 文字颜色
            arrowcolor=C_GOLD,              # 箭头颜色固定金色
            bordercolor=C_GOLD,              # 边框颜色
            lightcolor=C_BG_MEDIUM,
            darkcolor=C_BG_MEDIUM,
            borderwidth=1,
            relief="flat",
            padding=(3, 1),
            font=("微软雅黑", 12)  # 设置字体大小为12，与标签一致
        )
        
        # 映射所有状态下的颜色都保持不变
        style.map(
            "Gold.TCombobox",
            fieldbackground=[("readonly", C_BG_MEDIUM), ("disabled", C_BG_MEDIUM), ("active", C_BG_MEDIUM), ("focus", C_BG_MEDIUM)],
            background=[("readonly", C_BG_MEDIUM), ("disabled", C_BG_MEDIUM), ("active", C_BG_MEDIUM), ("focus", C_BG_MEDIUM)],
            foreground=[("readonly", C_GOLD), ("disabled", C_GOLD), ("active", C_GOLD), ("focus", C_GOLD)],
            arrowcolor=[("readonly", C_GOLD), ("disabled", C_GOLD), ("active", C_GOLD), ("focus", C_GOLD), ("pressed", C_GOLD)],
            bordercolor=[("readonly", C_GOLD), ("disabled", C_GOLD), ("active", C_GOLD), ("focus", C_GOLD)],
            selectbackground=[("readonly", C_BG_MEDIUM), ("focus", C_BG_MEDIUM)],
            selectforeground=[("readonly", C_GOLD), ("focus", C_GOLD)]
        )
        
        # 初始化选择框
        super().__init__(
            parent,
            style="Gold.TCombobox",
            values=values if values else [f"{i}%" for i in range(10, 100, 10)] + ["99%"],
            width=width,
            state="readonly",
            font=("微软雅黑", 12),  # 设置字体大小
            **kwargs
        )
        
        # 设置默认值
        self.set(default)
        
        # 锁定所有编辑操作
        self.bind("<Key>", lambda e: "break")              # 禁止键盘输入
        self.bind("<Button-3>", lambda e: "break")         # 禁止右键
        self.bind("<Double-Button-1>", lambda e: "break")  # 禁止双击
        self.bind("<B1-Motion>", lambda e: "break")        # 禁止拖拽选中
        self.bind("<Control-c>", lambda e: "break")        # 禁止复制
        self.bind("<Control-v>", lambda e: "break")        # 禁止粘贴
        self.bind("<Control-x>", lambda e: "break")        # 禁止剪切
        self.bind("<FocusIn>", self.on_focus_in)           # 获得焦点时清除选中
        
        # 配置下拉列表样式
        self.configure_combobox_popdown()
    
    def on_focus_in(self, event):
        """获得焦点时清除选中状态"""
        self.selection_clear()
        # 延迟一点移走焦点，避免影响下拉选择
        self.after(10, lambda: self.master.focus_set())
    
    def configure_combobox_popdown(self):
        """配置下拉列表样式"""
        try:
            # 获取下拉列表组件
            popdown = self.tk.call('ttk::combobox::PopdownWindow', self)
            self.popdown = self.nametowidget(popdown)
            
            # 配置下拉列表样式
            if hasattr(self, 'popdown'):
                listbox = self.popdown.f.l
                listbox.configure(
                    bg=C_BG_MEDIUM,
                    fg=C_GOLD,
                    selectbackground=C_BG_MEDIUM,
                    selectforeground=C_GOLD,
                    borderwidth=1,
                    relief="flat",
                    highlightthickness=1,
                    highlightcolor=C_GOLD,
                    highlightbackground=C_GOLD,
                    font=("微软雅黑", 12)  # 设置下拉列表字体
                )
        except:
            pass
    
    def get_value(self):
        """获取当前选中值"""
        return self.get()


class ClearableEntry(tk.Frame):
    """带清除按钮的输入框组件 - 点击X后恢复初始状态"""
    
    def __init__(self, parent, app=None, width=12, placeholder="", bg_color=C_BG_MEDIUM, 
                 text_color=C_GOLD, on_clear_callback=None, **kwargs):
        super().__init__(parent, bg=C_VOID)
        
        self.app = app
        self.width = width
        self.placeholder = placeholder
        self.bg_color = bg_color
        self.text_color = text_color
        self.on_clear_callback = on_clear_callback
        self.has_placeholder = bool(placeholder)
        self.is_placeholder_showing = False
        
        self.create_widgets()
        self.bind_events()
        
        if self.has_placeholder:
            self.show_placeholder()
    
    def create_widgets(self):
        """创建组件"""
        # 外层边框
        self.border = tk.Frame(self, bg=C_GOLD, padx=1, pady=1)
        self.border.pack()
        
        # 内层容器
        self.inner = tk.Frame(self.border, bg=self.bg_color)
        self.inner.pack(fill="x")
        
        # 输入框
        self.entry = tk.Entry(self.inner,
                              font=("微软雅黑", 11),
                              bg=self.bg_color,
                              fg="gray",
                              insertbackground=C_GOLD,
                              bd=0,
                              highlightthickness=0,
                              width=self.width,
                              takefocus=1)
        self.entry.pack(side="left", fill="x", expand=True, padx=(5, 0), ipady=5)
        
        # 清除按钮
        self.clear_btn = tk.Label(self.inner,
                                  text="✕",
                                  bg=self.bg_color,
                                  fg=self.bg_color,
                                  font=("Arial", 11, "bold"),
                                  width=2,
                                  takefocus=0)
        self.clear_btn.pack(side="right", padx=2)
    
    def bind_events(self):
        """绑定事件"""
        # 输入框事件
        self.entry.bind("<KeyRelease>", self.on_text_change)
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<Button-1>", self.on_entry_click)
        
        # 清除按钮事件
        self.clear_btn.bind("<Button-1>", self.on_clear_click)
        
        # 阻止清除按钮获得焦点
        self.clear_btn.bind("<FocusIn>", lambda e: self.entry.focus_set())
    
    def on_entry_click(self, event):
        """点击输入框时的处理"""
        if self.has_placeholder and self.is_placeholder_showing:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.text_color)
            self.is_placeholder_showing = False
        self.update_clear_button()
    
    def on_text_change(self, event):
        """文本变化时更新清除按钮显示"""
        self.update_clear_button()
    
    def on_focus_in(self, event):
        """获得焦点时处理"""
        if self.has_placeholder and self.is_placeholder_showing:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.text_color)
            self.is_placeholder_showing = False
        self.update_clear_button()
    
    def on_focus_out(self, event):
        """失去焦点时处理"""
        current_text = self.entry.get()
        if not current_text:
            if self.has_placeholder:
                self.show_placeholder()
            else:
                self.entry.delete(0, tk.END)
                self.entry.config(fg="gray")
        self.update_clear_button()
    
    def on_clear_click(self, event):
        """点击清除按钮 - 恢复初始状态"""
        if self.clear_btn.cget("fg") != self.bg_color:
            if self.has_placeholder:
                # 有占位符：清空后显示占位符，并移除焦点
                self.show_placeholder()
                # 移除焦点，让输入框恢复到初始状态
                self.master.focus_set()
            else:
                # 无占位符：清空
                self.entry.delete(0, tk.END)
                self.entry.config(fg="gray")
                self.update_clear_button()
            
            if self.on_clear_callback:
                self.on_clear_callback()
    
    def update_clear_button(self):
        """更新清除按钮的显示状态"""
        current_text = self.entry.get()
        if current_text and not (self.has_placeholder and self.is_placeholder_showing):
            self.clear_btn.config(fg="#FF0000")
        else:
            self.clear_btn.config(fg=self.bg_color)
    
    def show_placeholder(self):
        """显示占位符"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg="gray")
        self.is_placeholder_showing = True
        self.update_clear_button()
    
    def get(self):
        """获取输入框内容"""
        if self.is_placeholder_showing:
            return ""
        return self.entry.get()
    
    def set(self, value):
        """设置输入框内容"""
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, str(value))
            self.entry.config(fg=self.text_color)
            self.is_placeholder_showing = False
        elif self.has_placeholder:
            self.show_placeholder()
        else:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="gray")
            self.is_placeholder_showing = False
        self.update_clear_button()
    
    def clear(self):
        """清空输入框"""
        if self.has_placeholder:
            self.show_placeholder()
        else:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="gray")
            self.is_placeholder_showing = False
        self.update_clear_button()
    
    def disable(self):
        """禁用输入框"""
        self.entry.config(state="disabled", takefocus=0)
        self.border.config(bg=C_TEXT_DIM)
        self.clear_btn.config(fg=self.bg_color)
    
    def enable(self):
        """启用输入框"""
        self.entry.config(state="normal", takefocus=1)
        self.border.config(bg=C_GOLD)
        self.update_clear_button()
    
    def set_readonly(self, readonly=True):
        """设置只读状态"""
        if readonly:
            self.entry.config(state="readonly", takefocus=0)
            self.border.config(bg=C_TEXT_DIM)
            self.clear_btn.config(fg=self.bg_color)
        else:
            self.entry.config(state="normal", takefocus=1)
            self.border.config(bg=C_GOLD)
            self.update_clear_button()
    
    def focus(self):
        """获得焦点"""
        self.entry.focus_set()
