# pages/search_logic/sms_handler.py
class SMSHandler:
    """短信特邀业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def calculate(self, phone, week, date):
        """计算日期"""
        self.app.add_log("系统", "短信特邀", f"手机: {phone}, {week}, 日期: {date}")
        print(f"短信特邀 - 手机: {phone}, {week}, 日期: {date}")
