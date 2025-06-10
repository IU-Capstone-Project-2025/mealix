import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

categories = [
    ['https://magnit.ru/catalog/4834-moloko_syr_yaytsa?shopCode=167401&shopType=6', 28],
    ['https://magnit.ru/catalog/37741-syry_mm?shopCode=167401&shopType=6', 12],
    ['https://magnit.ru/catalog/4884-ovoshchi_frukty?shopCode=167401&shopType=6', 5],
    ['https://magnit.ru/catalog/5269-khleb_vypechka_sneki?shopCode=167401&shopType=6', 10],
    ['https://magnit.ru/catalog/4528-bakaleya_sousy?shopCode=167401&shopType=6', 28],
    ['https://magnit.ru/catalog/16363-konservy_myed_varene?shopCode=167401&shopType=6', 20],
    ['https://magnit.ru/catalog/4855-myaso_ptitsa_kolbasy?shopCode=167401&shopType=6', 3],
    ['https://magnit.ru/catalog/17591-sosiski_kolbasy_delikatesy?shopCode=167401&shopType=6', 16],
    ['https://magnit.ru/catalog/4998-ryba_moreprodukty?shopCode=167401&shopType=6', 15],
    ['https://magnit.ru/catalog/4459-zamorozhennye_produkty?shopCode=167401&shopType=6', 20],
    ['https://magnit.ru/catalog/5011-sladosti_torty_pirozhnye?shopCode=167401&shopType=6', 28],
    ['https://magnit.ru/catalog/5276-chay_kofe_kakao?shopCode=167401&shopType=6', 22],
    ['https://magnit.ru/catalog/4874-napitki_soki_voda?shopCode=167401&shopType=6', 25],
    ['https://magnit.ru/catalog/12435-chipsy_orekhi_sukhariki?shopCode=167401&shopType=6', 10],
    ['https://magnit.ru/catalog/7660-zdorovoe_pitanie_?shopCode=167401&shopType=6', 10]
]

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

progress_file = "progress.txt"

def read_progress():
    if os.path.exists(progress_file):
        with open(progress_file, "r") as file:
            lines = file.readlines()
            progress = {}
            for line in lines:
                category, page = line.strip().split(":")
                progress[category] = int(page)
            return progress
    return {}

def save_progress(category, page):
    progress = read_progress()
    progress[category] = page
    with open(progress_file, "w") as file:
        for cat, pg in progress.items():
            file.write(f"{cat}:{pg}\n")

try:
    progress = read_progress()
    for category_url, total_pages in categories:
        category_name = category_url.split('/catalog/')[1].split('?')[0].replace('_', '-')
        
        start_page = progress.get(category_name, 1)
        
        with open(f"{category_name}_links.txt", "a", encoding="utf-8") as file:
            for page in range(start_page, total_pages + 1):
                try:
                    current_url = f"{category_url}&page={page}" if page > 1 else category_url
                    driver.get(current_url)
                    
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "unit-catalog-product-preview"))
                    )
                    
                    product_elements = driver.find_elements(By.CLASS_NAME, "unit-catalog-product-preview")
                    for product in product_elements:
                        try:
                            link_element = product.find_element(By.CLASS_NAME, "pl-hover-base")
                            link = link_element.get_attribute("href")
                            print(link)
                            
                            price_element = driver.find_element(By.CLASS_NAME, "product-details__price--current")
                            print(price_element)
                            price = price_element.text.strip()
                            
                            print(price)
                            print()
                        except Exception as e:
                            print()
                    
                    print(f"Обработана страница {page} из {total_pages} для категории {category_name}")
                    
                    save_progress(category_name, page)
                    
                    time.sleep(2)
                except Exception as e:
                    print(f"Ошибка на странице {page} категории {category_name}: {e}")
                    save_progress(category_name, page - 1)
                    break

except Exception as e:
    print(f"Критическая ошибка: {e}")

finally:
    driver.quit()