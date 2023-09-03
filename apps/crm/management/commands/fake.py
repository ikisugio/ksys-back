from faker import Faker
from pykakasi import kakasi
from django.utils import timezone
from django.core.management.base import BaseCommand
from apps.crm.models.company import Company
from apps.crm.models.jigyosyo import Jigyosyo
from apps.crawler.models import CrawlList

fake = Faker("ja_JP")
repr_positions = [
    "代表取締役",
    "取締役",
    "執行役員",
    "監査役",
    "常務取締役",
    "専務取締役",
    "部長",
    "課長",
    "主任",
    "担当",
]


original_date_time_this_century = fake.date_time_this_century


def datetime_this_century_with_tz():
    return timezone.make_aware(original_date_time_this_century())


fake.date_time_this_century = datetime_this_century_with_tz


def generate_company_data():
    """Generate enhanced fake data for Company model using pykakasi."""
    company_name = fake.company()
    company_type = fake.random_element(
        elements=("株式会社", "有限会社", "一般社団法人", "公益社団法人", "合同会社", "NPO法人")
    )
    representative_name = fake.name().replace(" ", "")

    # Convert company_name to hiragana using pykakasi
    kakasi_instance = kakasi()
    kakasi_instance.setMode("J", "H")  # Convert Japanese to Hiragana
    conv = kakasi_instance.getConverter()
    company_name_kana = conv.do(company_name)

    return {
        "company_code": fake.unique.random_number(digits=13, fix_len=True),
        "type": company_type,
        "name": company_name,
        "name_kana": company_name_kana,
        "postal_code": fake.zipcode(),
        "address": fake.address(),
        "tel": fake.phone_number(),
        "fax": fake.phone_number(),
        "url": fake.url(),
        "repr_name": representative_name,
        "repr_position": fake.random_element(elements=repr_positions),
        "established_date": fake.date_this_century(),
        "release_datetime": fake.date_time_this_century(),
    }


def generate_jigyosyo_data():
    """Generate enhanced fake data for Jigyosyo model."""
    jigyosyo_name = fake.company()

    # Create a new CrawlList instance with dummy data
    crawl_list_entry = CrawlList.objects.create(
        jigyosyo_code=fake.unique.random_number(digits=10, fix_len=True),
        jigyosyo_name=jigyosyo_name,
        kourou_jigyosyo_url=fake.url(),
        fetch_datetime=fake.date_time_this_century(),
    )

    return {
        "jigyosyo_code": fake.unique.random_number(digits=10, fix_len=True),
        "name": jigyosyo_name,
        "postal_code": fake.zipcode(),
        "address": fake.address(),
        "tel": fake.phone_number(),
        "fax": fake.phone_number(),
        "repr_name": fake.name().replace(" ", ""),
        "repr_position": fake.random_element(elements=repr_positions),
        "kourou_jigyosyo_url": fake.url(),
        "kourou_release_datetime": fake.date_time_this_century(),
        "crawl_list_entry": crawl_list_entry,  # Associate the newly created CrawlList instance
    }


class Command(BaseCommand):
    help = "Inject fake data into specified models."

    def add_arguments(self, parser):
        parser.add_argument(
            "model_name_number",
            type=str,
            nargs="+",
            help="Names of the models and numbers in the format model_name:number.",
        )

    def handle(self, *args, **kwargs):
        model_name_numbers = kwargs["model_name_number"]

        for model_name_number in model_name_numbers:
            model_name, number = model_name_number.split(":")
            number = int(number)

            if model_name == "Company":
                for _ in range(number):
                    Company.objects.create(**generate_company_data())
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully injected fake data into {model_name}"
                        )
                    )
            elif model_name == "Jigyosyo":
                for _ in range(number):
                    # We need to create a company first since Jigyosyo has a ForeignKey to Company
                    company = Company.objects.create(**generate_company_data())
                    jigyosyo_data = generate_jigyosyo_data()
                    jigyosyo_data["company"] = company
                    Jigyosyo.objects.create(**jigyosyo_data)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully injected fake data into {model_name}"
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Model {model_name} not recognized.")
                )
