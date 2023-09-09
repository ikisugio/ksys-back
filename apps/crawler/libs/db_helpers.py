from django.db import transaction
from datetime import datetime, timedelta
from apps.crawler.models import CrawlList, CrawlDetail
from apps.crm.models import Company, Jigyosyo
from django.utils import timezone


def update_or_create_crawl_list(_crawl_list_data):
    crawl_list_data = {k.replace("crawl_list__", ""): v 
                       for k, v in _crawl_list_data.items()}
    instance, created = CrawlList.objects.get_or_create(
        jigyosyo_code=crawl_list_data.get("jigyosyo_code"),
        # jigyosyo_name=data.get("jigyosyo__name"),
        defaults=crawl_list_data,
    )
    return instance, created


def update_or_create_crawl_detail(data):
    defaults_data = {"fetch_datetime": datetime.now(), **data}
    instance, created = CrawlDetail.objects.update_or_create(
        unique_key_or_primary_key=data.get("unique_key_or_primary_key"),
        defaults=defaults_data,
    )
    return instance, created


def update_or_create_detail_info(detail_data):
    crawl_list_entry = CrawlList.objects.get(
        jigyosyo_code=detail_data.get("jigyosyo__code")
    )

    crawl_detail_entry = CrawlDetail.objects.filter(
        jigyosyo_code=crawl_list_entry
    ).first()

    if crawl_detail_entry and crawl_detail_entry.fetch_datetime:
        if timezone.now() - crawl_detail_entry.fetch_datetime < timedelta(
            days=90
        ):
            return None

    # 1. Create or update Company instance
    company_fields = [
        f.name for f in Company._meta.get_fields() if f.name != "jigyosyos"
    ]
    print(f"detail_data ====================> {detail_data}")
    company_data = {
        **{k: detail_data.get(f"company__{k}") for k in company_fields},
        "company_code": detail_data.get("company__code"),
        "release_datetime": detail_data.get("jigyosyo__release_datetime"),
    }
    print(f"company_data ====================> {company_data}")

    company_instance, company_created = custom_update_or_create(Company, defaults=company_data, name=company_data["name"], address=company_data["address"],)
    
    # company_instance, company_created = Company.objects.update_or_create(
    #     name=company_data["name"],
    #     address=company_data["address"],
    #     defaults=company_data,
    # )


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
        "company": company_instance,
    }
    jigyosyo_instance, _ = Jigyosyo.objects.update_or_create(
        jigyosyo_code=jigyosyo_data["jigyosyo_code"],
        defaults=jigyosyo_data,
    )

    # 3. Update or create other related data
    CrawlDetail.objects.update_or_create(
        jigyosyo_code=crawl_list_entry,
        defaults={"fetch_datetime": datetime.now()},
    )





@transaction.atomic
def custom_update_or_create(model, defaults=None, **kwargs):
    """
    Custom implementation of update_or_create for Django models.
    
    :param model: Django model class.
    :param defaults: Dictionary of values to update or create.
    :param kwargs: Lookup parameters.
    :return: tuple of (object, created) where object is the created or updated object and created is a boolean specifying whether a new object was created.
    """
    defaults = defaults or {}
    
    instance = model.objects.filter(**kwargs).first()
    
    if instance:
        # Update the object's fields
        for key, value in defaults.items():
            setattr(instance, key, value)
        instance.save()
        return instance, False

    else:
        # If the object does not exist, create it
        params = {**kwargs, **defaults}
        instance = model.objects.create(**params)
        return instance, True