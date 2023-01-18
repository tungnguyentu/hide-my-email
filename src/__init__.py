from src.database import Base
from src.auth.models import Account
from src.emails.models import VirtualDomain
from src.emails.proxy.models import VirtualUser
from src.emails.forwards.models import VirtualAliases
from logger import setup_app_level_logger

logger = setup_app_level_logger(name="HideMyEmail", level="INFO")
