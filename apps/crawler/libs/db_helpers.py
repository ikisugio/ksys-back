from django.db import transaction
from datetime import datetime, timedelta
from apps.crawler.models import CrawlList, CrawlDetail
from apps.crm.models import Company, Jigyosyo
from django.utils import timezone


def update_or_create_crawl_list(data):
    print(f"data is {data}")
    print(f"data.jigyosyo__code is {data.get('jigyosyo__code')}")
    data = {k.replace("crawl_list__", ""): v for k, v in data.items()}
    instance, created = CrawlList.objects.update_or_create(
        jigyosyo_code=data.get("jigyosyo__code"),
        # jigyosyo_name=data.get("jigyosyo__name"),
        defaults=data,
    )
    return instance, created


def update_or_create_crawl_detail(data):
    defaults_data = {"detail_fetch_datetime": datetime.now(), **data}
    instance, created = CrawlDetail.objects.update_or_create(
        unique_key_or_primary_key=data.get("unique_key_or_primary_key"),
        defaults=defaults_data,
    )
    return instance, created


@transaction.atomic
def update_or_create_detail_info(detail_data):
    crawl_list_entry = CrawlList.objects.get(
        jigyosyo_code=detail_data.get("jigyosyo__code")
    )

    crawl_detail_entry = CrawlDetail.objects.filter(
        jigyosyo_code=crawl_list_entry
    ).first()

    if crawl_detail_entry and crawl_detail_entry.detail_fetch_datetime:
        if timezone.now() - crawl_detail_entry.detail_fetch_datetime < timedelta(
            days=90
        ):
            return None

    # 1. Create or update Company instance
    company_fields = [
        f.name for f in Company._meta.get_fields() if f.name != "jigyosyos"
    ]
    company_data = {
        **{k: detail_data.get(f"company__{k}") for k in company_fields},
        "company_code": detail_data.get("company__code"),
        "release_datetime": detail_data.get("jigyosyo__release_datetime"),
    }
    company_instance, company_created = Company.objects.update_or_create(
        # company_code=company_data["company_code"],
        defaults=company_data,
    )

    # 2. Create or update Jigyosyo instance with reference to Company instance
    jigyosyo_fields = [
        f.name
        for f in Jigyosyo._meta.get_fields()
        if f.name not in ["list_entry", "companies", "company"]
    ]
    jigyosyo_data = {
        **{k: detail_data.get(f"jigyosyo__{k}") for k in jigyosyo_fields},
        "jigyosyo_code": detail_data.get("jigyosyo__code"),
        "name": crawl_list_entry.jigyosyo_name,
        "kourou_jigyosyo_url": crawl_list_entry.kourou_jigyosyo_url,
        "kourou_release_datetime": detail_data.get("jigyosyo__release_datetime"),
        "crawl_list_entry": crawl_list_entry,
    }
    jigyosyo_instance, _ = Jigyosyo.objects.update_or_create(
        # code=jigyosyo_data["jigyosyo__code"],
        defaults=jigyosyo_data,
    )

    # 3. Update or create other related data
    CrawlDetail.objects.update_or_create(
        jigyosyo_code=crawl_list_entry,
        defaults={"detail_fetch_datetime": datetime.now()},
    )
