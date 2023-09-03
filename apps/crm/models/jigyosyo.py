from django.db import models
from apps.crawler.models import CrawlList


class Jigyosyo(models.Model):
    jigyosyo_code = models.CharField(max_length=255, primary_key=True)
    company = models.ForeignKey(
        "crm.Company", on_delete=models.CASCADE, related_name="jigyosyos"
    )
    crawl_list_entry = models.OneToOneField(
        CrawlList, on_delete=models.CASCADE, related_name="jigyosyo"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    repr_name = models.CharField(max_length=255, null=True, blank=True)
    repr_position = models.CharField(max_length=255, null=True, blank=True)
    kourou_jigyosyo_url = models.CharField(max_length=255, null=True, blank=True)
    kourou_release_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "jigyosyo"
