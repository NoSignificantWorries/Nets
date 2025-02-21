import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class WildberriesCSS:
    SEARCH_BOX = "input.search-catalog__input"
    COOKIES_BUTTON = "button.cookies__btn"
    PAGINATION_NEXT_BUTTON = "a.pagination-next"
    CARD_OBJECT = "article"
    # 0 - read as attribute of container
    # 1 - read text from container
    CARD_PARSING_WAYS = [
        ("data-nm-id", 0),
        ("div > div.product-card__middle-wrap > div.product-card__price > span.price__wrap > ins", 1),
        ("div > div.product-card__middle-wrap > h2.product-card__brand-wrap > span.product-card__brand-container > span", 1),
        ("div > div.product-card__middle-wrap > h2.product-card__brand-wrap > span.product-card__name", 1)
    ]
    '''
    CARD_PARSING_TREE = [
        "data-nm-id",
        {"div": [{
            "div.product-card__middle-wrap": [{
                "div.product-card__price": [{
                    "span.price__wrap": {
                        "ins": None
                    }
                }],
                "h2.product-card__brand-wrap": [{
                    "span.product-card__brand-container": [{
                        "span": None
                    }],
                    "span.product-card__name": [{
                        "span": None
                    }]
                }]
            }]
        }]}
    ]
    '''


class Parser:
    def __init__(self, driver, url, css_objects, delay=5, csvfile="result.csv"):
        self.driver = driver
        self.driver.get(url)
        self.css_objects = css_objects
        self.csv_file = open(csvfile, "w")
        self.csv_writer = csv.writer(self.csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.csv_writer.writerow(["ID", "Price", "Company", "Name"])
        time.sleep(delay)

    def quit(self, delay=3):
        self.csv_file.close()
        time.sleep(delay)
        self.driver.quit()

    def find_product(self, request, delay=2):
        search_box = self.find_element_by_css(self.css_objects.SEARCH_BOX)
        if search_box is None:
            raise "SerchBox element missed!"
        search_box.clear()
        search_box.send_keys(request)
        search_box.send_keys(Keys.RETURN)
        time.sleep(delay)

    def scroll_to_element(self, element, delay=2):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(delay)

    def find_element_by_css(self, element_css):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, element_css)
        except BaseException as error:
            return None

    def find_all_elements_by_css(self, element_css):
        try:
            find_function = EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_css))
            return find_function(self.driver)
        except BaseException as error:
            return None

    def parse_cards_on_page(self):
        cards = self.find_all_elements_by_css(self.css_objects.CARD_OBJECT)
        if cards is None:
            raise "Cards parsing error!"
        for card in cards:
            row = []
            for way, type_id in self.css_objects.CARD_PARSING_WAYS:
                if type_id == 0:
                    row.append(card.get_attribute(way))
                if type_id == 1:
                    text_from_container = card.find_element(By.CSS_SELECTOR, way).text
                    text_from_container = text_from_container.replace("/ ", "")
                    row.append(text_from_container)
            if None not in row:
                self.csv_writer.writerow(row)

    def pagination_next(self, delay=2):
        pagination_button = self.find_element_by_css(self.css_objects.PAGINATION_NEXT_BUTTON)
        if pagination_button is None:
            raise "Pagination button missed!"
        self.scroll_to_element(pagination_button, delay)
        pagination_button.click()


# START PROGRAM
if __name__ == "__main__":
    driver = webdriver.Firefox()
    parser = Parser(driver, "https://www.wildberries.ru", WildberriesCSS, 6)

    cookies_button = parser.find_element_by_css(WildberriesCSS.COOKIES_BUTTON)
    if cookies_button is not None:
        cookies_button.click()

    parser.find_product("стрелы для лука")

    n = 3
    for i in range(n):
        print(f"Parsing cards o page {i + 1}/{n}...")
        parser.parse_cards_on_page()
        print("Page parsing done.")
        if i + 1 < n:
            parser.pagination_next()

    parser.quit()


