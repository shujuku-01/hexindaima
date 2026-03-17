# pages/search_logic/upload_handler.py
class UploadHandler:
    """上传数据业务逻辑"""
    
    def __init__(self, app):
        self.app = app
    
    def upload(self, value):
        """上传处理"""
        if value:
            self.app.add_log("系统", "上传数据", f"上传: {value}")
        else:
            self.app.add_log("警告", "上传数据", "请输入内容")
        print(f"上传数据: {value}")
