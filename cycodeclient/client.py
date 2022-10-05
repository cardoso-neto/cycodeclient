import logging
import os
import requests

from .violations import Violations
from .utils import request_safety


class CycodeClient(Violations):
    url = "https://api.cycode.com/api"
    base_headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }

    def __init__(self):
        self.token = self.authenticate()

    def assemble_headers(self) -> dict[str, str]:
        return self.base_headers | {"Authorization": f"Bearer {self.token}"}

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
        logging.info("Logged in to Cycode API.")
        return res.json()["token"]
