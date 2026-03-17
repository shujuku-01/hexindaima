# pages/search_logic/midnight_handler.py
class MidnightHandler:
    """午夜充值业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def query(self, value):
        """查询处理"""
        if value:
            self.app.add_log("系统", "午夜充值", f"查询: {value}")
        else:
            self.app.add_log("警告", "午夜充值", "请输入账号")
        print(f"午夜充值查询: {value}")
