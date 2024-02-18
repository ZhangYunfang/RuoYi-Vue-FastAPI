from fastapi import Depends
from typing import Union, List
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from exceptions.exception import PermissionException


class CheckUserInterfaceAuth:
    """
    校验当前用户是否具有相应的接口权限
    :param perm: 权限标识
    :param is_strict: 当传入的权限标识是list类型时，是否开启严格模式，开启表示会校验列表中的每一个权限标识，所有的校验结果都需要为True才会通过
    """
    def __init__(self, perm: Union[str, List], is_strict: bool = False):
        self.perm = perm
        self.is_strict = is_strict

    def __call__(self, current_user: CurrentUserModel = Depends(LoginService.get_current_user)):
        user_auth_list = current_user.permissions
        if '*:*:*' in user_auth_list:
            return True
        if isinstance(self.perm, str):
            if self.perm in user_auth_list:
                return True
        if isinstance(self.perm, list):
            if self.is_strict:
                if all([perm_str in user_auth_list for perm_str in self.perm]):
                    return True
            else:
                if any([perm_str in user_auth_list for perm_str in self.perm]):
                    return True
        raise PermissionException(data="", message="该用户无此接口权限")
