from dataclasses import dataclass
from datetime import datetime
from pkg_helpers.enums.gender import Genders
from pkg_helpers.enums.user_account_status import AccountStatuses
from pkg_helpers.enums.role import Roles

@dataclass
class CreateUserDTO():
    email: str = "" 
    first_name: str = "" 
    last_name: str = ""
    gender: Genders = None
    birthday: datetime.date = None
    phone_number: str = ""
    status: AccountStatuses = None
    role: Roles = None
    password: str = ""