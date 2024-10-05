"""AppVeyor tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_appveyor import streams


class TapAppVeyor(Tap):
    """Singer tap for AppVeyor."""

    name = "tap-appveyor"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            secret=True,
            description="API Token for AppVeyor.",
        ),
        th.Property(
            "accounts",
            th.ArrayType(th.StringType),
            description=(
                "Account names to get data from. This uses the user-level API key (v2) "
                "that allows working with any account user has access to."
            ),
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of AppVeyor streams.
        """
        return [streams.Projects(tap=self)]
