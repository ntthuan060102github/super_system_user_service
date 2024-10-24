from typing import Union, Any

from appbase.models.user import User

from pkg_helpers.logging import logger

class UserRepo():
    def get_user_by_email(self, email: str) -> Union[User, None]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
    def get_user_by_id(self, id: Any) -> Union[User, None]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
        
    def create_user(self, user: User) -> Union[User, None]:
        try:
            user.save()

            if user.id is not None:
                logger.info("UserRepo.create_user success user_id=%s", user.id)
                return user

            logger.error("UserRepo.create_user fail user=%s", user)
            return None
        except Exception as e:
            logger.exception("UserRepo.create_user exc=%s, user=%s", e, user)
            return None