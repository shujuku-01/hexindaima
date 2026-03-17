# pages/search_logic/vip_handler.py
class VIPHandler:
    """活跃VIP业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def query(self, value):
        """查询处理"""
        if value:
            self.app.add_log("系统", "活跃VIP", f"查询: {value}")
        else:
            self.app.add_log("警告", "活跃VIP", "请输入VIP等级")
        print(f"活跃VIP查询: {value}")
    
    def days_query(self, days):
        """天数查询"""
        self.app.add_log("系统", "活跃VIP", f"{days}天查询")
        print(f"活跃VIP {days}天查询")
