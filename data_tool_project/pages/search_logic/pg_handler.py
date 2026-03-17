# pages/search_logic/pg_handler.py
class PGHandler:
    """PG1计算业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def calculate(self, account, bet, total):
        """PG计算"""
        self.app.add_log("系统", "PG1计算", f"账号: {account}, 投注: {bet}, 总注单: {total}")
        print(f"PG计算 - 账号: {account}, 投注: {bet}, 总注单: {total}")
