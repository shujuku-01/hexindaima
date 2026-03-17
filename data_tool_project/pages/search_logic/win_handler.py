# pages/search_logic/win_handler.py
class WinHandler:
    """连赢查询业务逻辑"""
    
    def __init__(self, app):
        self.app = app
        self.combo2 = None
    
    def on_combo1_select(self, combo1, combo2):
        """第一个选择框选择事件"""
        selected = combo1.get()
        
        if selected == "棋牌":
            combo2.config(values=["3", "5", "10", "15", "20"])
            combo2.set("3")
        elif selected == "真人":
            combo2.config(values=["6", "8", "12", "18", "25", "30", "35"])
            combo2.set("6")
        
        # 显示第二个选择框
        combo2.pack(side="left", padx=5)
        return combo2
    
    def query(self, value, combo1_value, combo2_value):
        """查询处理"""
        if value:
            self.app.add_log("系统", "连赢查询", f"{combo1_value}-{combo2_value} 订单号: {value}")
        else:
            self.app.add_log("警告", "连赢查询", "请输入订单号")
        print(f"连赢查询: {combo1_value}-{combo2_value} 订单号: {value}")
