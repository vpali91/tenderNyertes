from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import const


class WebScraper:
    def __init__(self):
        self.s = Service(const.CHROME_DRIVER)
        self.options = Options()
        self.options.add_argument(const.CHROME_DETAILS)
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        self.project_names = []
        self.project_deadlines = []
        self.project_tam_sum = []
        self.project_tam_intenz = []
        self.project_tam_form = []
        self.project_bead_kezdet = []
        self.project_tam_min_sum = []

    def webscrape_checker(self):
        print(self.project_names)
        print(self.project_deadlines)
        print(self.project_tam_sum)
        print(self.project_tam_intenz)
        print(self.project_tam_form)
        print(self.project_bead_kezdet)
        print(self.project_tam_min_sum)

    def webscrape(self):
        self.driver.get(const.TENDER_LINK)
        sleep(3)
        tender_on = True
        i = 1
        while tender_on:
            html_source = self.driver.page_source
            with open(f'html_files/file{i}.html', mode="w", encoding="utf-8") as fp:
                fp.write(html_source)

            with open(f'html_files/file{i}.html', mode="r", encoding="utf-8") as fp:
                content = fp.read()

            soup = BeautifulSoup(content, 'html.parser')

            project_titles = soup.find_all(name='p', class_="project-title")
            project_titles_ = [project_title.get_text() for project_title in project_titles]
            for item in project_titles_:
                self.project_names.append(item)

            project_descriptions = soup.find_all(name='div', class_="project-description")
            project_descriptions_ = [project_description.get_text() for project_description in project_descriptions]
            project_descriptions_string = ''.join(project_descriptions_).replace(chr(160), ' ').replace('Támogatás maximum összege ', '').replace('Támogatási intenzitás ', '').replace('Támogatás formája ','').replace('Beadás kezdete ', '').replace('Támogatás minimum összege ', '').replace('Pályázati dokumentációTerületi szereplők', '').replace('Pályázati dokumentáció', '').replace('Pályázati kitöltő', '')
            project_descriptions_fixed = project_descriptions_string.split('Beadási határidő :')
            project_descriptions_fixed.remove('')

            for item in project_descriptions_fixed:
                list = item.split(':')
                self.project_deadlines.append(list[0])
                self.project_tam_sum.append(list[1])
                self.project_tam_intenz.append(list[2])
                self.project_tam_form.append(list[3])
                self.project_bead_kezdet.append(list[4])
                self.project_tam_min_sum.append(list[5])

            i = i + 1
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            page = soup.find(name="span", class_="react-bootstrap-table-pagination-total").get_text().replace('- ','').replace('/ ', '').split(' ')
            print(page)
            if page[1] != page[2]:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[5]/div/div/div[3]/div[2]/div[2]/ul/li[13]/span/button').click()
                sleep(5)
            else:
                tender_on = False

        self.webscrape_checker()