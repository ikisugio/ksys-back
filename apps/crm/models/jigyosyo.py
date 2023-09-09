from django.db import models
from django.apps import apps
from apps.crawler.models import CrawlList


class Jigyosyo(models.Model):
    BULK_INSERT_MODE = False
    jigyosyo_code = models.CharField(max_length=255, primary_key=True)
    company = models.ForeignKey(
        "crm.Company", on_delete=models.CASCADE, related_name="jigyosyos", null=True, blank=True
    )
    crawl_list_entry = models.OneToOneField(
        CrawlList, on_delete=models.CASCADE, related_name="jigyosyo", null=True, blank=True
    )
    type = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    repr_name = models.CharField(max_length=255, null=True, blank=True)
    repr_position = models.CharField(max_length=255, null=True, blank=True)
    kourou_jigyosyo_url = models.CharField(max_length=255, null=True, blank=True)
    kourou_release_datetime = models.DateTimeField(null=True, blank=True)
    
    # def save(self, *args, **kwargs):
    #     super(Jigyosyo, self).save(*args, **kwargs)
    #     if not Jigyosyo.BULK_INSERT_MODE:
    #         apps.get_model("crm", "LogicalJigyosyo").create_grouped_jigyosyo()


    class Meta:
        db_table = "jigyosyo"
