from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas
import openpyxl

# Ide másold be a saját google form linked
GOOGLE_FORM_LINK = 'https://forms.gle/5wPX4iVJnY969bUo9'

TENDER_LINK = 'https://www.palyazat.gov.hu/plyzatkeres'

options = Options()

# to open default chrome profile. You need to close all chrome windows before it will work
options.add_argument('user-data-dir=C:/Users/viczj/AppData/Local/Google/Chrome/User Data')

s = Service("D:/chromedriver.exe")

driver = webdriver.Chrome(service=s, options=options)

driver.get(TENDER_LINK)
sleep(3)
tender_on = True
i = 1
project_names = []
project_deadlines =[]
project_tam_sum = []
project_tam_intenz = []
project_tam_form = []
project_bead_kezdet = []
project_tam_min_sum = []

while tender_on:
    html_source = driver.page_source
    with open(f'file{i}.html', mode="w", encoding="utf-8") as fp:
        fp.write(html_source)

    with open(f'file{i}.html', mode="r", encoding="utf-8") as fp:
        content = fp.read()

    soup = BeautifulSoup(content, 'html.parser')

    project_titles = soup.find_all(name='p', class_="project-title")
    project_titles_ = [project_title.get_text() for project_title in project_titles]
    for item in project_titles_:
        project_names.append(item)

    project_descriptions = soup.find_all(name='div', class_="project-description")
    project_descriptions_ = [project_description.get_text() for project_description in project_descriptions]
    project_descriptions_string =''.join(project_descriptions_).replace(chr(160),' ').replace('Támogatás maximum összege ', '').replace('Támogatási intenzitás ','').replace('Támogatás formája ','').replace('Beadás kezdete ','').replace('Támogatás minimum összege ','').replace('Pályázati dokumentációTerületi szereplők','').replace('Pályázati dokumentáció','').replace('Pályázati kitöltő','')
    project_descriptions_fixed = project_descriptions_string.split('Beadási határidő :')
    project_descriptions_fixed.remove('')

    for item in project_descriptions_fixed:
        list = item.split(':')
        project_deadlines.append(list[0])
        project_tam_sum.append(list[1])
        project_tam_intenz.append(list[2])
        project_tam_form.append(list[3])
        project_bead_kezdet.append(list[4])
        project_tam_min_sum.append(list[5])

    i = i+1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)
    page = soup.find(name="span", class_="react-bootstrap-table-pagination-total").get_text().replace('- ','').replace('/ ','').split(' ')
    print(page)
    if page[1]!=page[2]:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div/div/div[3]/div[2]/div[2]/ul/li[13]/span/button').click()
        sleep(5)
    else:
        tender_on = False

print(project_titles_)
print(project_descriptions)
print(project_descriptions_fixed)
print(project_deadlines)
print(project_tam_sum)
print(project_tam_intenz)
print(project_tam_form)
print(project_bead_kezdet)
print(project_tam_min_sum)

excel_writer = "D:/table.xlsx"
pandas.DataFrame({"Project név":project_names, "Határidő": project_deadlines, "Támogatás maximum összege": project_tam_sum, "Támogatási intenzitás":project_tam_intenz, "Támogatás formája": project_tam_form, "Beadás kezdete": project_bead_kezdet,"Támogatás minimum összege": project_tam_min_sum }).to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None, storage_options=None)

