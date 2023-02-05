import requests
from bs4 import BeautifulSoup
import json
import lxml


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

hrefs_festival = {}

for i in range(0, 193, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=5%20Feb%202023&to_date=&maxprice=500&o={i}&bannertitle=May"
    req = requests.get(url=url, headers=headers).text

    json_data = json.loads(req)
    html_response = json_data["html"]

    with open(f"pages_html/{i}_index.html", "w", encoding="utf-8") as file:
        file.write(html_response)
        file.close()

    with open(f"pages_html/{i}_index.html", encoding="utf-8") as file:
        html_page = file.read()

    soup = BeautifulSoup(html_page, "lxml")

    all_h3 = soup.find_all("h3", {"class": "margin-top-0 margin-bottom-5 card-title"})

    for h3 in all_h3:
        title = h3.find("a").get("title")
        href = "https://www.skiddle.com" + h3.find("a").get("href")

        hrefs_festival[title] = href

with open("hrefs_festival.json", "w", encoding="utf-8") as file:
    json.dump(hrefs_festival, file, indent=4, ensure_ascii=False)
    file.close()

with open("hrefs_festival.json", encoding="utf-8") as file:
    hrefs = json.load(file)

info_festivals = []

count = 0
for title, url in hrefs.items():

    detail_festival = {}
    detail_festival["title"] = title

    file_name_split = title.split(" ")
    file_name = file_name_split[0]

    src = requests.get(url=url, headers=headers).text

    with open(f"ever_fest_html/{count}_{file_name}_page.html", "w", encoding="utf-8") as file:
        file.write(src)
        file.close()

    with open(f"ever_fest_html/{count}_{file_name}_page.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    try:
        info_block = soup.find("div", {"class": "MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq"})
        date_place_price = info_block.find_all("div", {"class": "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol"})
    except Exception:
        print(f"{count} {title} not found fest blok info\n")
        continue

    try:
        date = date_place_price[0].text
    except Exception:
        date = "not found"
        print(f"{title} not found date")
    detail_festival["date"] = date

    try:
        title_location = date_place_price[1].text
    except Exception:
        title_location = "not found"
        print(f"{title} not found title_location")
    detail_festival["title_location"] = title_location

    try:
        price = date_place_price[2].text
    except Exception:
        price = "not found"
        print(f"{title} not found price")
    detail_festival["price"] = price

    # делаем запрос на часть страницы с FAQs
    url_faqs = f"{url}#faq"

    req = requests.get(url=url_faqs, headers=headers).text
    soup_faqs = BeautifulSoup(req, "lxml")

    # находим блок <div> с FAQs и записываем в JSON
    next_data = soup_faqs.find(id="__NEXT_DATA__").text
    json_data_faqs = json.loads(next_data)

    # создаем файл для каждой страницы и записываем в него данные
    with open(f"faqs_data_ever_fest/{count}_{file_name}_faqs_data.json", "w", encoding="utf-8") as file:
        json.dump(json_data_faqs, file, indent=4, ensure_ascii=False)
        file.close()

    with open(f"faqs_data_ever_fest/{count}_{file_name}_faqs_data.json", encoding="utf-8") as file:
        json_data_faqs = json.load(file)

    faqs = json_data_faqs["props"]["pageProps"]["faqs"]

    faqs_list = []

    for item in faqs:
        question = item.get("question")
        answer = item.get("answer").strip().replace("\r", "").replace("<p>", "").replace("</p>", "").replace("\n", "")

        faqs_dict = {}
        faqs_dict["question"] = question
        faqs_dict["answer"] = answer

        faqs_list.append(faqs_dict)
    detail_festival["faqs"] = faqs_list
    info_festivals.append(detail_festival)

    print(len(info_festivals))
    print(f"{count} {title} записан\n")
    count += 1

with open("info_fests.json", "w", encoding="utf-8") as file:
    json.dump(info_festivals, file, indent=4, ensure_ascii=False)
    file.close()






