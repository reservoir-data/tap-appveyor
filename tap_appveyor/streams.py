"""Stream type classes for tap-appveyor."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_appveyor.client import AppVeyorStream


class Projects(AppVeyorStream):
    """Users stream."""

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
