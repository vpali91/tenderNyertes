from web_scraper import WebScraper
import pandas
import openpyxl


class DataEntry:

    def save_data(self):
        excel_writer = "D:/projects.xlsx"
        ws = WebScraper()
        ws.webscrape()
        pandas.DataFrame({"Project név":ws.project_names, "Határidő": ws.project_deadlines, "Támogatás maximum összege": ws.project_tam_sum, "Támogatási intenzitás": ws.project_tam_intenz, "Támogatás formája": ws.project_tam_form, "Beadás kezdete": ws.project_bead_kezdet,"Támogatás minimum összege": ws.project_tam_min_sum }).to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None, storage_options=None)
