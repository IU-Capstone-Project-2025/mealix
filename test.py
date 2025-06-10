import re
import csv
from bs4 import BeautifulSoup

def parse_html_to_csv(html_file_path, output_csv_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    product_data = {
        'Наименование': 'NaN',
        'Вес/объем': 'NaN',
        'Ккал': 'NaN',
        'Белки': 'NaN',
        'Жиры': 'NaN',
        'Углеводы': 'NaN',
        'Тип_продукта': 'NaN',
        'Бренд': 'NaN',
        'Производитель': 'NaN',
        'Артикул': 'NaN',
        'Состав': 'NaN',
        'Описание': 'NaN',
        'image_url': 'NaN',
        'rating_score': 'NaN'
    }

    name_elem = soup.find('span', {'itemprop': 'name'})
    if name_elem:
        full_name = name_elem.text.strip()
        weight_match = re.search(r'(\d+\s*[гмлkкgл]+)$', full_name)
        if weight_match:
            product_data['Вес/объем'] = weight_match.group(1)
            product_data['Наименование'] = full_name[:weight_match.start()].strip(', ')
        else:
            product_data['Наименование'] = full_name

    img_elem = soup.find('img', class_='product-details-gallery__slide-image')
    if img_elem and 'src' in img_elem.attrs:
        product_data['image_url'] = img_elem['src']

    nutrition_section = soup.find('section', class_='product-details-nutrition-facts')
    if nutrition_section:
        nutrition_items = nutrition_section.find_all('div', class_='product-details-nutrition-facts__list-item')
        for item in nutrition_items:
            title = item.find('div', class_='product-details-nutrition-facts__list-item__title').text.strip()
            value = item.find_all('div', class_='pl-text')[-1].text.strip()
            if title == 'Ккал':
                product_data['Ккал'] = value
            elif title == 'Белки':
                product_data['Белки'] = value
            elif title == 'Жиры':
                product_data['Жиры'] = value
            elif title == 'Углеводы':
                product_data['Углеводы'] = value

    parameters_section = soup.find('section', class_='product-details-parameters')
    if parameters_section:
        param_items = parameters_section.find_all('div', class_='product-details-parameters-list__item')
        for item in param_items:
            label_elem = item.find('span', style=lambda x: x and '--_c:var(--pl-text-secondary)' in x)
            value_elem = item.find('span', style=lambda x: x and '--_c:var(--pl-text-primary)' in x)
            if label_elem and value_elem:
                label = label_elem.text.strip()
                value = value_elem.text.strip()
                if label == 'Тип продукта':
                    product_data['Тип_продукта'] = value
                elif label == 'Бренд':
                    product_data['Бренд'] = value
                elif label == 'Производитель':
                    product_data['Производитель'] = value
                elif label == 'Артикул':
                    product_data['Артикул'] = value

        composition_items = parameters_section.find('section', class_='product-details-parameters-flat')
        # print(composition_items)
        # print()
        for item in composition_items:
            p_tag = item.find('p')
            if p_tag:
                product_data['Состав'] = p_tag.text.strip()



        description_section = parameters_section.find('div', {'itemprop': 'description'})
        if description_section:
            product_data['Описание'] = description_section.text.strip()

        raiting_score = soup.find('span', class_='product-rating-score').text
        product_data['rating_score'] = raiting_score
        

    with open(output_csv_path, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=product_data.keys())
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(product_data)

if __name__ == "__main__":
    parse_html_to_csv('page_source.html', 'products.csv')