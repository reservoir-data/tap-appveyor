"""REST client handling, including AppVeyorStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class AppVeyorStream(RESTStream[t.Any]):
    """AppVeyor stream class."""

    _url_base = "https://ci.appveyor.com/api"
    records_jsonpath = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API base URL."""
        if self.config.get("accounts"):
            return f"{self._url_base}/account/{{account_name}}"

        return self._url_base

    @property
    def partitions(self) -> list[dict[str, t.Any]] | None:
        """Return a list of partitions."""
        if accounts := self.config.get("accounts"):
            return [{"account_name": account} for account in accounts]
        return None

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
        }

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict[str, t.Any] = {}
        return params
