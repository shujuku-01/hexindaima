# pages/search_logic/phone_handler.py
class PhoneHandler:
    """电话回访业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def query(self, value):
        """查询处理"""
        if value:
            self.app.add_log("系统", "电话回访", f"查询: {value}")
        else:
            self.app.add_log("警告", "电话回访", "请输入电话号码")
        print(f"电话回访查询: {value}")
