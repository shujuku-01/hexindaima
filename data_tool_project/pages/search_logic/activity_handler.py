# pages/search_logic/activity_handler.py
class ActivityHandler:
    """活动查询业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def query(self, value):
        """查询处理"""
        if value:
            self.app.add_log("系统", "活动查询", f"查询: {value}")
        else:
            self.app.add_log("警告", "活动查询", "请输入账号")
        print(f"活动查询: {value}")
