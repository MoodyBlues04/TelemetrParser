from __future__ import annotations
from django.db import models
from app.services.dto import TableRow


class ParsedChannel(models.Model):
    name = models.CharField(max_length=255)
    subscribers = models.IntegerField()
    increment = models.IntegerField()
    post_views = models.IntegerField()
    er = models.FloatField()
    references = models.IntegerField()
    geo = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    @classmethod
    def row_updated(cls, parsed_row: TableRow) -> bool:
        if not cls.row_exists(parsed_row):
            return True
        channel = cls.get_by_name(parsed_row.name)
        for key, val in parsed_row.__dict__.items():
            model_val = channel.__dict__.get(key)
            if model_val is not None and model_val != val:
                return True
        return False

    @classmethod
    def row_exists(cls, parsed_row: TableRow) -> bool:
        return cls.get_by_name(parsed_row.name) is not None

    @classmethod
    def get_by_name(cls, name: str) -> ParsedChannel|None:
        return cls.objects.filter(name=name).first()

    @classmethod
    def add_rows(cls, parsed_rows: list[TableRow]) -> None:
        for parsed_row in parsed_rows:
            cls.add_or_update_row(parsed_row)

    @classmethod
    def add_or_update_row(cls, parsed_row: TableRow) -> None:
        cls.objects.update_or_create(
            name=parsed_row.name,
            subscribers=parsed_row.subscribers,
            post_views=parsed_row.post_views,
            er=parsed_row.er,
            references=parsed_row.references,
            increment=parsed_row.increment,
            geo=parsed_row.geo,
            category=parsed_row.category
        )
