import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('data.json', 'w') as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        # first we load existing data into a dict.
        file_data = json.load(file)
        # join new_data with file_data inside emp_details
        file_data.append(new_data)
        # sets file's current position at offset.
        file.seek(0)
        #convert back to json
        json.dump(file_data, file, ensure_ascii=False, indent = 4)




browser = webdriver.Firefox()

browser.get(f'https://www.amazon.com.br/s?k=kindle&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1JHXPI6PYIYI7&sprefix=kindle%2Caps%2C205&ref=nb_sb_noss_1')


isNextDisabled = False

while not isNextDisabled:

    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

        elem_list = browser.find_element(By.CSS_SELECTOR, 'span.rush-component:nth-child(2)')

        items = elem_list.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for item in items:
            title = item.find_element(By.TAG_NAME, 'h2').text
            price = 'No Price Found'
            image = 'No Image Found'
            link = 'No Link Found'
            try:
                price = item.find_element(By.CSS_SELECTOR, '.a-price').text.replace('\n', '.')
            except:
                pass
            try:
                image = item.find_element(By.CLASS_NAME, 's-image').get_attribute('src')
            except:
                pass
            try:
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                pass
                
            print('Title: ',title)
            print('Price: ', price)
            print('Image: ', image)
            print('Link: ', link, '\n\n\n')
            print("----------------------------------------------------------------------------------------------------------------------------------------------\n\n\n")
            write_json({
                'Title':title,
                'Price':price,
                'Image': image,
                'Link': link
            })


        next_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 's-pagination-next')))

        next_class = next_btn.get_attribute('class')

        if 's-pagination-disabled' in next_class:
            isNextDisabled = True
            break
        else:
            browser.find_element(By.CLASS_NAME, 's-pagination-next').click()

    except Exception as e:
        print(e, 'Main Error')
        isNextDisabled = True


