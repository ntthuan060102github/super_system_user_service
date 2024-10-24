import re
from typing import Union, Any
from dataclasses import asdict

from appbase.dtos.create_user import CreateUserDTO
from appbase.repositories.user import UserRepo
from appbase.models.user import User

from pkg_helpers.logging import logger
from pkg_helpers.auth.user_dto import UserDTO
from pkg_helpers.otp.generate_otp import generate_otp_only_number
from pkg_helpers.background_tasks.send_email import send_mail_with_template
from pkg_helpers.enums.user_account_status import AccountStatuses

class UserService():
    __user_repo = UserRepo()

    __verify_user_key_prefix = "unverified_user"
    __password_regex_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    def get_user_by_email(self, email: str) -> Union[UserDTO, None]:
        try:
            user = self.__user_repo.get_user_by_email(email=email)
            
            if user is None:
                return None

            return user.to_dto()
        except Exception as e:
            logger.exception("UserService.get_user_by_email exc=%s, email=%s", e, email)
            raise e
        
    def get_user_by_id(self, id: Any) -> Union[UserDTO, None]:
        try:
            user = self.__user_repo.get_user_by_id(id=id)
            
            if user is None:
                return None

            return user.to_dto()
        except Exception as e:
            logger.exception("UserService.get_user_by_id exc=%s, id=%s", e, id)
            raise e
        
    def is_valid_password(self, password: str) -> bool:
        try:
            return bool(re.match(self.__password_regex_pattern, password))
        except Exception as e:
            logger.exception("UserService.is_valid_password exc=%s, password=%s", e, password)
            return False
        
    def create_user(self, user_dto: CreateUserDTO) ->  Union[UserDTO, None]:
        try:
            new_user = User(**asdict(user_dto))
            new_user.status = AccountStatuses.UNVERIFIED
            new_user.set_password(user_dto.password)

            user = self.__user_repo.create_user(new_user)

            if user is None:
                logger.error("UserService.create_user UserRepo.create_user fail user_dto=%s, new_user=%s", user_dto, new_user)
                return None
            else:
                otp = generate_otp_only_number(6)
                self.__send_mail_verify_new_user(user.email, otp)
                return user.to_dto()

        except Exception as e:
            logger.exception("UserService.create_user exc=%s, user_dto=%s", e, user_dto)
            return None
        
    def __send_mail_verify_new_user(self, email: str, otp: str):
        try:
            send_mail_with_template.apply_async(
                kwargs={
                    "to": [email],
                    "cc": [],
                    "subject": "Xác thực tài khoản",
                    "template_name": "verify_new_user.html",
                    "context": {
                        "otp": otp
                    }
                }
            )
        except Exception as e:
            logger.exception("UserService.__send_mail_verify_new_user exc=%s, email=%s", e, email)
    