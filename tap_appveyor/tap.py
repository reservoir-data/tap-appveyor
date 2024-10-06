"""AppVeyor tap class."""

from __future__ import annotations

from typing import Any, override

from singer_sdk import RESTStream, Stream, Tap
from singer_sdk import typing as th
from singer_sdk.authenticators import BearerTokenAuthenticator


class AppVeyorStream(RESTStream[Any]):
    """AppVeyor stream class."""

    records_jsonpath = "$[*]"

    @property
    @override
    def url_base(self) -> str:
        url = "https://ci.appveyor.com/api"
        if self.config.get("accounts"):
            return f"{url}/account/{{account_name}}"

        return url

    @property
    @override
    def partitions(self) -> list[dict[str, Any]] | None:
        if accounts := self.config.get("accounts"):
            return [{"account_name": account} for account in accounts]
        return None

    @property
    @override
    def authenticator(self) -> BearerTokenAuthenticator:
        token: str = self.config["token"]
        return BearerTokenAuthenticator(token=token)


class Projects(AppVeyorStream):
    """Projects stream."""

    name = "projects"
    path = "/projects"
    primary_keys = ("projectId",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property("projectId", th.IntegerType),
        th.Property("accountId", th.IntegerType),
        th.Property("accountName", th.StringType),
        th.Property(
            "builds",
            th.ArrayType(
                th.ObjectType(
                    th.Property("buildId", th.IntegerType),
                    th.Property("jobs", th.ArrayType(th.ObjectType())),
                    th.Property("buildNumber", th.IntegerType),
                    th.Property("version", th.StringType),
                    th.Property("message", th.StringType),
                    th.Property("branch", th.StringType),
                    th.Property("commitId", th.StringType),
                    th.Property("authorName", th.StringType),
                    th.Property("authorUsername", th.StringType),
                    th.Property("committerName", th.StringType),
                    th.Property("committerUsername", th.StringType),
                    th.Property("committed", th.DateTimeType),
                    th.Property("messages", th.ArrayType(th.ObjectType())),
                    th.Property("status", th.StringType),
                    th.Property("started", th.DateTimeType),
                    th.Property("finished", th.DateTimeType),
                    th.Property("created", th.DateTimeType),
                    th.Property("updated", th.DateTimeType),
                )
            ),
        ),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("repositoryType", th.StringType),
        th.Property("repositoryScm", th.StringType),
        th.Property("repositoryName", th.StringType),
        th.Property("repositoryBranch", th.StringType),
        th.Property("isPrivate", th.BooleanType),
        th.Property("skipBranchesWithoutAppveyorYml", th.BooleanType),
        th.Property(
            "nuGetFeed",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("publishingEnabled", th.BooleanType),
                th.Property("created", th.DateTimeType),
            ),
        ),
        th.Property("created", th.DateTimeType),
    ).to_dict()


class Collaborators(AppVeyorStream):
    """Users stream."""

    name = "collaborators"
    path = "/collaborators"
    primary_keys = ("accountId",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property("accountId", th.IntegerType),
        th.Property("accountName", th.StringType),
        th.Property("isOwner", th.BooleanType),
        th.Property("isCollaborator", th.BooleanType),
        th.Property("userId", th.IntegerType),
        th.Property("fullName", th.StringType),
        th.Property("email", th.StringType),
        th.Property("roleId", th.IntegerType),
        th.Property("roleName", th.StringType),
        th.Property("successfulBuildNotification", th.StringType),
        th.Property("failedBuildNotification", th.StringType),
        th.Property("notifyWhenBuildStatusChangedOnly", th.BooleanType),
        th.Property("created", th.DateTimeType),
        th.Property("updated", th.DateTimeType),
    ).to_dict()


class Users(Collaborators):
    """Users stream."""

    name = "users"
    path = "/users"


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
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        return [
            Collaborators(tap=self),
            Projects(tap=self),
            Users(tap=self),
        ]
