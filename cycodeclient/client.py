import os
import requests

from .types import EssentialHeaders
from .violations import Violations
from .utils import request_safety


class CycodeClient(Violations):
    url = "https://app.cycode.com/api"

    def __init__(self):
        self.token = self.authenticate()

    def assemble_headers(self) -> EssentialHeaders:
        headers = EssentialHeaders(
            Accept="application/json",
            Authorization=f"Bearer {self.token}",
        )
        return headers

    @classmethod
    def authenticate(cls) -> str:
        """
        $ curl https://api.cycode.com/api/v1/auth/api-token -X POST \
            -H "Content-type: application/json" \
            --data '{"clientId": "", "secret": ""}'
        {"token": "", "refresh_token": "", "expires_in": 86400}
        """
        url = f"{cls.url}/v1/auth/api-token"
        data = {
            "clientId": os.getenv("CycodeClientID"),
            "secret": os.getenv("CycodeSecret"),
        }
        with request_safety():
            res = requests.post(url, json=data)
            res.raise_for_status()
        return res.json()["token"]
