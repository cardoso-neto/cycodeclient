import requests
from typing import TypedDict

from .utils import request_safety


class EssentialHeaders(TypedDict):
    Accept: str
    Authorization: str


class Violations:
    url: str
    def assemble_headers(self) -> EssentialHeaders: ...

    def get_violation_details(self, identifier: str) -> dict:
        """
        {"status": "Resolved", "status_reason": "Revoked"}
        or
        {"status": "Dismissed", "status_reason": "Ignored"}
        """
        url = f"{self.url}/alerts/{identifier}"
        with request_safety():
            res = requests.get(url, headers=self.assemble_headers())  # type: ignore
            res.raise_for_status()
        return res.json()

    def get_critical_vulns_in_dep_violations(self):
        """
        https://docs.cycode.com/reference/apiviolationsv2_get
        """
        url = f"{self.url}/violations/v2"
        url += "?detectionRuleIds=305e7372-0b75-4418-ae97-84b24d14e688"
        url += "&detectionRuleIds=ad4aa7e2-a93f-4dd3-8ba2-a4e2e2979e5d"
        url += "&detectionTypeId=9369d10a-9ac0-48d3-9921-5de7fe9a37a7"
        url += "&f0=list,policy_type"
        url += "&f0=SCA"
        url += "&f1=list,status"
        url += "&f1=Open"
        url += "&f2=list,severity"
        url += "&f2=3"
        url += "&limit=2"
        url += "&pageIndex=1"
        url += "&policyType=SCA"
        with request_safety():
            res = requests.get(url, headers=self.assemble_headers())  # type: ignore
            res.raise_for_status()
        return res.json()