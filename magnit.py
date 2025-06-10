from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://magnit.ru/product/1000501598-mr_ricco_mayonez_provansal_67_340g_d_p?shopCode=167401&shopType=6"

try:
    logging.info("Открываем страницу: %s", url)
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
        )
        logging.info("Карточки товаров найдены")
    except Exception as e:
        logging.error("Не удалось найти карточки товаров: %s", e)
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logging.info("HTML страницы сохранен в page_source.html")
        raise

    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять')]"))
        )
        cookie_button.click()
        logging.info("Модальное окно (cookie) закрыто")
    except:
        logging.info("Модальное окно не найдено")

    page = 1
    while True:
        logging.info("Обрабатываем страницу %d", page)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        products = driver.find_elements(By.CLASS_NAME, "product-card")
        logging.info("Найдено %d товаров на странице %d", len(products), page)

        for product in products:
            try:
                name_element = product.find_element(By.CLASS_NAME, "product-card__title")
                name = name_element.text.strip() if name_element else "N/A"

                price_elements = product.find_elements(By.CLASS_NAME, "product-card__price")
                price = price_elements[0].text.strip() if price_elements else "N/A"

                weight_elements = product.find_elements(By.CLASS_NAME, "product-card__weight")
                weight = weight_elements[0].text.strip() if weight_elements else "N/A"

                print(f"Название: {name}")
                print(f"Цена: {price}")
                print(f"Вес: {weight}")
                print("-" * 50)

            except Exception as e:
                logging.warning("Ошибка при обработке товара: %s", e)
                continue

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Показать ещё')]"))
            )
            ActionChains(driver).move_to_element(next_button).click().perform()
            time.sleep(3)
            page += 1
        except:
            logging.info("Больше страниц нет")
            break

except Exception as e:
    logging.error("Произошла ошибка: %s", e)
    with open("error_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logging.info("HTML страницы сохранен в error_page_source.html")

finally:
    driver.quit()
    logging.info("Браузер закрыт")