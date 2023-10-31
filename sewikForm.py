from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sewikForm(voivodeship, county, start_date, end_date):
    driver = webdriver.Chrome()
    driver.get("https://sewik.pl/search")
    try:
        voivodeship_dropdown = Select(driver.find_element(By.ID, "filter_form_voivodeship"))
        voivodeship_dropdown.select_by_visible_text(voivodeship)

        county_dropdown = Select(driver.find_element(By.ID, "filter_form_county"))
        county_dropdown.select_by_visible_text(county)

        start_date_input = driver.find_element(By.ID, "filter_form_fromDate")
        start_date_input.clear()
        start_date_input.send_keys(start_date)

        end_date_input = driver.find_element(By.ID, "filter_form_toDate")
        end_date_input.clear()
        end_date_input.send_keys(end_date)

        submit_button = driver.find_element(By.ID, "filter_form_accidents")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        page_source = driver.page_source
        
        with open("sewik_page.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        
    finally:
        driver.quit()
