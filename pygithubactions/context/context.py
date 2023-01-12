import json
import os
from typing import Optional


class Context:
    """Processes all env vars set by github in runner"""

    def __init__(self) -> None:
        self._payload: dict = {}
        self._event_name: Optional[str] = os.getenv('GITHUB_EVENT_NAME')
        self.sha: Optional[str] = os.getenv('GITHUB_SHA')
        self.ref: Optional[str] = os.getenv('GITHUB_REF')
        self.workflow: Optional[str] = os.getenv('GITHUB_WORKFLOW')
        self.action: Optional[str] = os.getenv('GITHUB_ACTION')
        self.actor: Optional[str] = os.getenv('GITHUB_ACTOR')
        self.job: Optional[str] = os.getenv('GITHUB_JOB')
        self.run_number: Optional[str] = os.getenv('GITHUB_RUN_NUMBER')
        self.run_id: Optional[str] = os.getenv('GITHUB_RUN_ID')
        self.api_url: str = (
            os.getenv('GITHUB_API_URL') or 'https://api.github.com'
        )
        self.server_url: str = (
            os.getenv('GITHUB_SERVER_URL') or 'https://github.com'
        )
        self.graphql_url: str = (
            os.getenv('GITHUB_GRAPHQL_URL') or 'https://api.github.com/graphql'
        )
        self.process_payload()

    def process_payload(self) -> None:
        if 'GITHUB_EVENT_PATH' in os.environ:
            with open(os.environ['GITHUB_EVENT_PATH'], 'r') as f:
                content = f.read()
                self._payload = json.loads(content)

    @property
    def payload(self) -> dict:
        return self._payload

    @property
    def event_name(self) -> Optional[str]:
        return self._event_name


def get_context() -> Context:
    return Context()
