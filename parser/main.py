import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def scroll_and_click(driver, button, scrolling=True):
    if button is None:
        return "None element"
    button_classes = button.get("class")
    for class_name in button_classes:
        clickable_button = driver.find_element(By.CLASS_NAME, class_name)
        if clickable_button is not None:
            if scrolling:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", clickable_button)
                    time.sleep(1)
                except Exceprion as error:
                    return error
            clickable_button.click()
            break
    return None


def parse_product(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    description_button = None
    buttons = soup.find_all('button')
    for button in buttons:
        if button.get("aria-label") == "Характеристики и описание":
            description_button = button

    error = scroll_and_click(driver, description_button)
    if error is not None:
        print(f"Error: {errors}")

    return None


def parse_cards(driver, csv_writer):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for card in soup.find_all("article"):
        row = []
        card_id = card.get("data-nm-id")
        if card_id is None:
            continue
        row.append(card_id)
        row.append(card.find("ins").text.strip().replace("\xa0", " "))
        for span in card.find_all("span"):
            classes = span.get("class")
            if classes is None:
                continue
            if classes[0] == "product-card__brand":
                row.append(span.text.strip())
            if classes[0] == "product-card__name":
                row.append(span.text.strip()[2:])
        csv_writer.writerow(row)


def pagination(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    pagination_next = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")
    try:
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
    except Exceprion as error:
        return error
    pagination_next.click()


# START PROGRAM
if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.wildberries.ru")
    time.sleep(8)

    # Parse and click coockies button {{{
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    okey_button = None
    buttons = soup.find_all('button')
    for button in buttons:
        if button.text.strip() == "Окей":
            okey_button = button
    error = scroll_and_click(driver, okey_button, False)
    if error is not None:
        print(f"Error: {errors}")
    # }}}

    request = "стрелы для лука"

    # Find products {{{
    for input_element in soup.find_all("input"):
        if input_element.get("type") == "search" and input_element.get("id") == "searchInput":
            search_box_element = input_element
            break

    for search_class in search_box_element.get("class"):
        element = driver.find_element(By.CLASS_NAME, search_class)
        if element is not None:
            element.clear()
            element.send_keys(request)
            element.send_keys(Keys.RETURN)
            break
    # }}}

    time.sleep(3)
    max_pages = 4

    # Parse pages and products {{{

    result_file = open("result.csv", "w")
    writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["ID", "Price", "Company", "Name"])

    for i_page in range(max_pages):
        print(f"Parsing page {i_page + 1}/{max_pages}...")
        parse_cards(driver, writer)
        print("Parsing done.")
        pagination(driver)
        time.sleep(1)

    result_file.close()

    # }}}

