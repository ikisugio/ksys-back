from django.db import models
from datetime import datetime, timedelta


class CrawlList(models.Model):
    jigyosyo_code = models.CharField(max_length=255, primary_key=True)
    jigyosyo_name = models.CharField(max_length=255, null=True, blank=True)
    kourou_jigyosyo_url = models.CharField(max_length=255, null=True, blank=True)
    fetch_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "crawl_list"


class CrawlDetail(models.Model):
    jigyosyo_code = models.ForeignKey(CrawlList, on_delete=models.CASCADE)
    fetch_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "crawl_detail"
