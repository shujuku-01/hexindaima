# pages/search_logic/__init__.py
from .midnight_handler import MidnightHandler
from .phone_handler import PhoneHandler
from .vip_handler import VIPHandler
from .win_handler import WinHandler
from .pg_handler import PGHandler
from .welcome_handler import WelcomeHandler
from .sms_handler import SMSHandler
from .activity_handler import ActivityHandler
from .upload_handler import UploadHandler

class SearchLogic:
    """综合搜索业务逻辑统一入口"""
    
    def __init__(self, app):
        self.app = app
        self.midnight = MidnightHandler(app)
        self.phone = PhoneHandler(app)
        self.vip = VIPHandler(app)
        self.win = WinHandler(app)
        self.pg = PGHandler(app)
        self.welcome = WelcomeHandler(app)
        self.sms = SMSHandler(app)
        self.activity = ActivityHandler(app)
        self.upload = UploadHandler(app)
