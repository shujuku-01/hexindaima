# pages/search_logic/welcome_handler.py
class WelcomeHandler:
    """迎新活动业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def query(self, account, activity, amount):
        """查询处理"""
        self.app.add_log("系统", "迎新活动", f"账号: {account}, 活动: {activity}, 注单量: {amount}")
        print(f"迎新活动 - 账号: {account}, 活动: {activity}, 注单量: {amount}")
