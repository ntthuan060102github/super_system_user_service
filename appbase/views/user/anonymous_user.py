from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema

from appbase.services.user import UserService
from appbase.dtos.create_user import CreateUserDTO
from appbase.serializers.user.create_user import CreateUserSerializer

from pkg_helpers.logging import logger
from pkg_helpers.response.response import RestResponse
from pkg_helpers.decorators.validate_request import validate_request

class AnonymousUserView(ViewSet):
    __user_service = UserService()

    @swagger_auto_schema(request_body=CreateUserSerializer)
    @validate_request(CreateUserSerializer)
    def create(self, request: Request, validated_data: dict):
        try:
            if not self.__user_service.is_valid_password(validated_data.get("password", "")):
                return RestResponse().defined_error().set_message("Mật khẩu của bạn chưa đủ an toàn!").response

            dto = CreateUserDTO(**validated_data)
            user = self.__user_service.create_user(dto)

            if user is None:
                return RestResponse().defined_error().set_message("Tạo tài khoản không thành công!").response

            return RestResponse().success().response
        except Exception as e:
            logger.exception("AnonymousUserView.post exc=%s, req=%s", e, request.data)
            return RestResponse().internal_server_error().response