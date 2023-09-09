from faker import Faker
from pykakasi import kakasi
from django.utils import timezone
from django.core.management.base import BaseCommand
from apps.crm.models.company import Company
from apps.crm.models.jigyosyo import Jigyosyo
from apps.crawler.models import CrawlList
from apps.crm.models.admin import AdminGroup, AdminUser
from .consts.company import REPR_POSITIONS, COMPANY_TYPES
from .consts.admin import GROUP_NAMES, PREFECTURE_NAME_MAP


fake = Faker("ja_JP")


original_date_time_this_century = fake.date_time_this_century


def datetime_this_century_with_tz():
    return timezone.make_aware(original_date_time_this_century())


fake.date_time_this_century = datetime_this_century_with_tz


def generate_company_data():
    """Generate enhanced fake data for Company model using pykakasi."""
    company_name = fake.company()
    company_type = fake.random_element(
        elements=COMPANY_TYPES
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
        "repr_position": fake.random_element(elements=REPR_POSITIONS),
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
        "repr_position": fake.random_element(elements=REPR_POSITIONS),
        "kourou_jigyosyo_url": fake.url(),
        "kourou_release_datetime": fake.date_time_this_century(),
        "crawl_list_entry": crawl_list_entry,  # Associate the newly created CrawlList instance
    }


def generate_admin_group_data():

    for group_name in GROUP_NAMES:
        if group_name == '本部':
            permission = 'head'
        else:
            permission = 'branch'
        
        AdminGroup.objects.create(name=group_name, permission=permission)


def generate_admin_user_data():
    """Generate data for AdminUser model."""
    # Get all admin groups
    groups = list(AdminGroup.objects.all())
    
    # If no groups exist, generate them first
    if not groups:
        generate_admin_group_data()
        groups = list(AdminGroup.objects.all())
    
    # Randomly assign a group to the user
    group = fake.random_element(elements=groups)
    is_superuser_flag = True if group.name == '本部' else False
    
    english_name = PREFECTURE_NAME_MAP[group.name]
    count = AdminUser.objects.filter(username__startswith=english_name).count() + 1
    username = f"{english_name}_{count}"

    return {
        "username": username,
        "email": fake.unique.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        # "password": fake.password(),
        "is_superuser": is_superuser_flag,
        "group_to_add": group,
    }


def generate_admin_user_data_for_group(group):
    """Generate data for AdminUser model for a specific group."""
    english_name = PREFECTURE_NAME_MAP[group.name]
    count = AdminUser.objects.filter(username__startswith=english_name).count() + 1
    username = f"{english_name}_{count}"
    is_superuser_flag = True if group.name == '本部' else False

    return {
        "username": username,
        "email": fake.unique.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "is_superuser": is_superuser_flag,
        "group_to_add": group,
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
            if "AdminGroup" in model_name_number:
                model_name = "AdminGroup"
                number = 1
            else:
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
                    company = Company.objects.create(**generate_company_data())
                    jigyosyo_data = generate_jigyosyo_data()
                    jigyosyo_data["company"] = company
                    Jigyosyo.objects.create(**jigyosyo_data)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully injected fake data into {model_name}"
                        )
                    )
            elif model_name == "AdminGroup":
                generate_admin_group_data()
                self.stdout.write(self.style.SUCCESS(f"Successfully injected fake data into {model_name}"))
                
            elif model_name == "AdminUser":
                groups = AdminGroup.objects.all()
                for group in groups:
                    for _ in range(number):
                        user_data = generate_admin_user_data_for_group(group)
                        group_to_add = user_data.pop('group_to_add')
                        user = AdminUser(**user_data)
                        user.set_password("testpass")
                        user.save()
                        user.groups.add(group_to_add)
                        self.stdout.write(self.style.SUCCESS(f"Successfully injected fake data into {model_name} for group {group.name}"))
                        
            else:
                self.stdout.write(
                    self.style.ERROR(f"Model {model_name} not recognized.")
                )