import requests
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime
from ..utils import iso8601
from ..utils.adnorm import full_norm
from ..etc import configs
from ..libs import db_helpers
from ..models import CrawlList
from apps.crm.models import Company, Jigyosyo


def convert_url(url):
    return url.replace("kani", "kihon")


def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # エラーレスポンスを確認
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Request error for URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for URL {url}: {e}")
        return None


def fetch_company_detail(data_url):
    soup = get_soup(data_url)
    if not soup:
        return {}
    company_soup = soup.find("div", id="tableGroup-1").find("table")
    details = {}

    mappings = {
        "法人番号": "company__code",
        "法人等の種類": "company__type",
        "名称": "company__name",
        "（ふりがな）": "company__name_kana",
        "所在地": "company__address",
        "電話番号": "company__tel",
        "ＦＡＸ番号": "company__fax",
        "ホームページ": "company__url",
        "氏名": "company__repr_name",
        "職名": "company__repr_position",
        "法人等の設立年月日": "company__established_date",
    }

    for soup_td in company_soup.find_all("td"):
        soup_th = soup_td.find_previous("th")

        th = soup_th.text.split(",")[0].strip()
        td = soup_td.text.replace(" ", "").replace("\u3000", "")

        if th in mappings:
            if th == "法人番号" and not td:
                details[mappings[th]] = ""
            elif th == "設立年月日":
                details[mappings[th]] = datetime.strptime(td, "%Y/%m/%d").date()
                print("ssss")
            elif th == "（ふりがな）":
                if soup_td.get("diffid") == "diff-c3":
                    details["company__name_kana"] = td.replace("\u3000", " ")
                elif soup_td.get("diffid") == "diff-c4":
                    details["company__name"] = td.replace("\u3000", " ")
            elif th == "法人等の設立年月日":
                to_date = lambda x: datetime.strptime(x, "%Y/%m/%d").date()
                details[mappings[th]] = to_date(td.replace("\u3000", " "))
            else:
                details[mappings[th]] = td.replace("\u3000", " ")

        if "所在地" in th:
            if soup_td.get("diffid") == "diff-c7":
                details["company__postal_code"] = td.replace("〒", "").strip()
            elif soup_td.get("diffid") == "diff-c8":
                details["company__address"] = full_norm(td)

    return details


def fetch_jigyosyo_detail(base_data_url):
    detail_data_url = convert_url(base_data_url)
    soup = get_soup(detail_data_url)
    if not soup:
        return {}

    details = {
        "jigyosyo__release_datetime": iso8601.from_jp_time(
            soup.find("p").text.split()[0]
        ),
        "jigyosyo__code": detail_data_url.split("JigyosyoCd=")[1].split("-")[0],
        "crawl_detail__fetch_datetime": datetime.now().replace(microsecond=0),
    }

    # キーと対応する検索文字列のマップ
    key_map = {
        "jigyosyo__tel": "電話番号",
        "jigyosyo__fax": "FAX番号",
        "jigyosyo__repr_name": "氏名",
        "jigyosyo__repr_position": "職名",
    }

    # キーごとにテキストを検索し、正規化してdetailsに追加
    for key, search_text in key_map.items():
        raw_text = soup.find(string=search_text).find_next().text.strip()
        details[key] = unicodedata.normalize("NFKC", raw_text)

    # 所在地の情報を取得
    def extract_and_normalize_address(soup):
        address_tag = soup.find(string="所在地").find_next().find_next()
        raw_address = address_tag.text.strip()
        postal_code = raw_address.split("\u3000")[0].replace("〒", "").strip()
        address = raw_address.replace("〒" + postal_code, "").strip()

        # 正規化
        normalized_postal_code = unicodedata.normalize("NFKC", postal_code)
        normalized_address = unicodedata.normalize("NFKC", address)

        return normalized_postal_code, normalized_address

    jigyosyo_postal_code, jigyosyo_address = extract_and_normalize_address(soup)
    details["jigyosyo__postal_code"] = jigyosyo_postal_code
    details["jigyosyo__address"] = full_norm(jigyosyo_address)

    erase_space = (
        lambda x: x.replace(" ", "").replace("\u3000", "") if type(x) == str else x
    )
    details = {k: erase_space(v) for k, v in details.items()}

    return details


def fetch_detail(base_data_url):
    detail_data_url = convert_url(base_data_url)
    print(f"~~~~~~~~~~~{detail_data_url}~~~~~~~~~~~~~~~~~")

    jigyosyo_details = fetch_jigyosyo_detail(detail_data_url)
    company_details = fetch_company_detail(detail_data_url)

    print("fetch ~~~~~~~~~~~~~~")
    print(jigyosyo_details)
    print(company_details)

    return {**jigyosyo_details, **company_details}


# def bulk_insert_jigyosyo(data_list):
#     Jigyosyo.BULK_INSERT_MODE = True
#     for data in data_list:
#         update_or_create_detail_info(data)  # この関数内でJigyosyoのデータを追加または更新します
#     Jigyosyo.BULK_INSERT_MODE = False



def run():
    # CrawlListからすべてのURLを取得
    crawl_list_entries = CrawlList.objects.all()

    for crawl_list_entry in crawl_list_entries:
        base_data_url = crawl_list_entry.kourou_jigyosyo_url
        detail_data = fetch_detail(base_data_url)

        db_helpers.update_or_create_detail_info(detail_data)


    # all_details_data = []

    # for crawl_list_entry in crawl_list_entries:
    #     base_data_url = crawl_list_entry.kourou_jigyosyo_url
    #     detail_data = fetch_detail(base_data_url)
    #     all_details_data.append(detail_data)

    # # 取得した詳細データをデータベースに一括挿入または更新
    # bulk_insert_jigyosyo(all_details_data)