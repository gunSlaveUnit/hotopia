from typing import Union, Optional

import requests
from requests import Session

from core.models.users import User
from server.src.api.v1.schemas.users import UserSignUpSchema, UserSignInSchema
from common.src.core.settings import SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL


class AuthService:
    def __init__(self):
        super().__init__()

        self.current_user: Optional[User] = None
        self.authorized_session: Optional[Session] = None

    def _user_access(self, url: str, data: Union[UserSignUpSchema, UserSignInSchema]):
        response = requests.post(url, json=data.model_dump())

        if response.ok:
            self.authorized_session = requests.session()
            self.authorized_session.cookies.set('session', response.cookies['session'])

        return response

    def sign_up(self, data: UserSignUpSchema):
        return self._user_access(SIGN_UP_URL, data)

    def sign_in(self, data: UserSignInSchema):
        return self._user_access(SIGN_IN_URL, data)

    def sign_out(self):
        response = self.authorized_session.post(SIGN_OUT_URL)

        if response.ok:
            self.authorized_session = None
            self.current_user = None

        return response

    def me(self):
        if self.authorized_session is None:
            return

        response = self.authorized_session.get(ME_URL)

        if response.ok:
            self.current_user = User(**response.json())
