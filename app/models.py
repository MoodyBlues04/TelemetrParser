from __future__ import annotations
from django.db import models
from app.services.dto import TableRow


class ParsedChannel(models.Model):
    name = models.CharField(max_length=255)
    image = models.TextField()
    subscribers = models.IntegerField()
    increment = models.IntegerField()
    post_views = models.IntegerField()
    er = models.FloatField()
    references = models.IntegerField()
    geo = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ('name', 'image')

    @classmethod
    def row_updated(cls, parsed_row: TableRow) -> bool:
        channel = cls.get_by_row(parsed_row)
        if channel is None:
            return True
        for key, val in parsed_row.__dict__.items():
            model_val = channel.__dict__.get(key)
            if model_val is not None and model_val != val:
                return True
        return False

    @classmethod
    def get_by_row(cls, parsed_row: TableRow) -> ParsedChannel | None:
        return cls.objects.filter(name=parsed_row.name, image=parsed_row.image).first()

    @classmethod
    def add_rows(cls, parsed_rows: list[TableRow]) -> None:
        for parsed_row in parsed_rows:
            cls.add_or_update_row(parsed_row)

    @classmethod
    def add_or_update_row(cls, parsed_row: TableRow) -> None:
        cls.objects.update_or_create(
            name=parsed_row.name,
            image=parsed_row.image,
            defaults={
                "subscribers": parsed_row.subscribers,
                "post_views": parsed_row.post_views,
                "er": parsed_row.er,
                "references": parsed_row.references,
                "increment": parsed_row.increment,
                "geo": parsed_row.geo,
                "category": parsed_row.category,
                "status": parsed_row.status,
                "link": parsed_row.link
            }
        )
