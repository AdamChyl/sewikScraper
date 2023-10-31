import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QGridLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog
from sewikForm import sewikForm
from sewikScraper import sewikScraper
import pandas as pd
import datetime

class sewikScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sewik Scraper')
        self.resize(600, 200)

        main_layout = QGridLayout()
  
        voivodeship_label = QLabel('Województwo:')
        self.voivodeship_combo = QComboBox()
        self.voivodeship_combo.addItem('')
        self.addVoivodeships()
        self.voivodeship_combo.currentIndexChanged.connect(self.updateCounties)
        main_layout.addWidget(voivodeship_label, 0, 0)
        main_layout.addWidget(self.voivodeship_combo, 0, 1)

        county_label = QLabel('Powiat:')
        self.county_combo = QComboBox()
        self.county_combo.addItem('')
        main_layout.addWidget(county_label, 1, 0)
        main_layout.addWidget(self.county_combo, 1, 1)

        from_date_label = QLabel('Od dnia:')
        self.from_date_edit = QLineEdit()
        self.from_date_edit.setPlaceholderText('yyyy-mm-dd')
        main_layout.addWidget(from_date_label, 2, 0)
        main_layout.addWidget(self.from_date_edit, 2, 1)

        to_date_label = QLabel('Do dnia:')
        self.to_date_edit = QLineEdit()
        self.to_date_edit.setPlaceholderText('yyyy-mm-dd')
        main_layout.addWidget(to_date_label, 3, 0)
        main_layout.addWidget(self.to_date_edit, 3, 1)

        download_button = QPushButton('Pobierz Zdarzenia')
        download_button.clicked.connect(self.downloadCsv)
        main_layout.addWidget(download_button, 4, 1, 1, 1)
        
        save_button = QPushButton('Wybierz Ścieżkę Zapisu')
        save_button.clicked.connect(self.chooseSavePath)
        main_layout.addWidget(save_button, 4, 0, 1, 1)

        self.setLayout(main_layout)
        
        self.checked_dates = []

    def addVoivodeships(self):
        voivodeships = [
            'Dolnośląskie', 'Kujawsko-Pomorskie', 'Lubelskie', 'Lubuskie', 'Mazowieckie',
            'Małopolskie', 'Opolskie', 'Podkarpackie', 'Podlaskie', 'Pomorskie',
            'Warmińsko-Mazurskie', 'Wielkopolskie', 'Zachodniopomorskie', 'Łódzkie', 'Śląskie', 'Świętokrzyskie'
        ]
        self.voivodeship_combo.addItems(voivodeships)

    def updateCounties(self):
        selected_voivodeship = self.voivodeship_combo.currentText()
        self.county_combo.clear()
        self.county_combo.addItem('')

        counties = []
        
        if selected_voivodeship == 'Dolnośląskie':
            counties = ['WROCŁAW', 'JELENIA GÓRA', 'LEGNICA', 'WAŁBRZYCH', 'BOLESŁAWIECKI', 'DZIERŻONIOWSKI', 'GŁOGOWSKI', 'GÓROWSKI', 'JAWORSKI', 'JELENIOGÓRSKI', 'KAMIENNOGÓRSKI', 'KŁODZKI', 'LEGNICKI', 'LUBAŃSKI', 'LUBIŃSKI', 'LWÓWECKI', 'MILICKI', 'OLEŚNICKI', 'OŁAWSKI', 'POLKOWICKI', 'STRZELIŃSKI', 'ŚREDZKI', 'ŚWIDNICKI', 'TRZEBNICKI', 'WAŁBRZYSKI', 'WOŁOWSKI', 'WROCŁAWSKI', 'ZĄBKOWICKI', 'ZGORZELECKI', 'ZŁOTORYJSKI']
        elif selected_voivodeship == 'Kujawsko-Pomorskie':
            counties = ['BYDGOSZCZ', 'TORUŃ', 'WŁOCŁAWEK', 'GRUDZIĄDZ', 'ALEKSANDROWSKI', 'BRODNICKI', 'BYDGOSKI', 'CHEŁMIŃSKI', 'GOLUBSKO-DOBRZYŃSKI', 'GRUDZIĄDZKI', 'INOWROCŁAWSKI', 'LIPNOWSKI', 'MOGILEŃSKI', 'NAKIELSKI', 'RADZIEJOWSKI', 'RYPIŃSKI', 'SĘPOLEŃSKI', 'ŚWIECKI', 'TORUŃSKI', 'TUCHOLSKI', 'WĄBRZESKI', 'WŁOCŁAWSKI', 'ŻNIŃSKI']
        elif selected_voivodeship == 'Mazowieckie':
            counties = ['WARSZAWA', 'OSTROŁĘKA', 'PŁOCK', 'RADOM', 'SIEDLCE', 'BIAŁOBRZESKI', 'CIECHANOWSKI', 'GARWOLIŃSKI', 'GOSTYNIŃSKI', 'GRODZISKI', 'GRÓJECKI', 'KOZIENICKI', 'LEGIONOWSKI', 'LIPSKI', 'ŁOSICKI', 'MAKOWSKI', 'MIŃSKI', 'MŁAWSKI', 'NOWODWORSKI', 'OSTROŁĘCKI', 'OSTROWSKI', 'OTWOCKI', 'PIASECZYŃSKI', 'PŁOCKI', 'PŁOŃSKI', 'PRUSZKOWSKI', 'PRZASNYSKI', 'PRZYSUSKI', 'PUŁTUSKI', 'RADOMSKI', 'SIEDLECKI', 'SIERPECKI', 'SOCHACZEWSKI', 'SOKOŁOWSKI', 'SZYDŁOWIECKI', 'WARSZAWSKI ZACHODNI', 'WĘGROWSKI', 'WOŁOMIŃSKI', 'WYSZKOWSKI', 'ZWOLEŃSKI', 'ŻUROMIŃSKI', 'ŻYRARDOWSKI']
        elif selected_voivodeship == 'Małopolskie':
            counties = ['KRAKÓW', 'NOWY SĄCZ', 'TARNÓW', 'BOCHEŃSKI', 'BRZESKI', 'CHRZANOWSKI', 'DĄBROWSKI', 'GORLICKI', 'KRAKOWSKI', 'LIMANOWSKI', 'MIECHOWSKI', 'MYŚLENICKI', 'NOWOSĄDECKI', 'NOWOTARSKI', 'OLKUSKI', 'OŚWIĘCIMSKI', 'PROSZOWICKI', 'SUSKI', 'TARNOWSKI', 'TATRZAŃSKI', 'WADOWICKI', 'WIELICKI']
        elif selected_voivodeship == 'Łódzkie':
            counties = ['ŁÓDŹ', 'PIOTRKÓW TRYBUNALSKI', 'SKIERNIEWICE', 'BEŁCHATOWSKI', 'BRZEZIŃSKI', 'KUTNOWSKI', 'ŁASKI', 'ŁĘCZYCKI', 'ŁOWICKI', 'ŁÓDZKI WSCHODNI', 'OPOCZYŃSKI', 'PABIANICKI', 'PAJĘCZAŃSKI', 'PIOTRKOWSKI', 'PODDĘBICKI', 'RADOMSZCZAŃSKI', 'RAWSKI', 'SIERADZKI', 'SKIERNIEWICKI', 'TOMASZOWSKI', 'WIELUŃSKI', 'WIERUSZOWSKI', 'ZDUŃSKOWOLSKI', 'ZGIERSKI']
        elif selected_voivodeship == 'Lubelskie':
            counties = ['LUBLIN', 'BIAŁA PODLASKA', 'CHEŁM', 'ZAMOŚĆ', 'BIALSKI', 'BIŁGORAJSKI', 'CHEŁMSKI', 'HRUBIESZOWSKI', 'JANOWSKI', 'KRASNOSTAWSKI', 'KRAŚNICKI', 'LUBARTOWSKI', 'LUBELSKI', 'ŁĘCZYŃSKI', 'ŁUKOWSKI', 'OPOLSKI', 'PARCZEWSKI', 'PUŁAWSKI', 'RADZYŃSKI', 'RYCKI', 'ŚWIDNICKI', 'TOMASZOWSKI', 'WŁODAWSKI', 'ZAMOJSKI']
        elif selected_voivodeship == 'Lubuskie':
            counties = ['GORZÓW WIELKOPOLSKI', 'ZIELONA GÓRA', 'GORZOWSKI', 'KROŚNIEŃSKI', 'MIĘDZYRZECKI', 'NOWOSOLSKI', 'SŁUBICKI', 'STRZELECKO-DREZDENECKI', 'SULĘCIŃSKI', 'ŚWIEBODZIŃSKI', 'WSCHOWSKI', 'ZIELONOGÓRSKI', 'ŻAGAŃSKI', 'ŻARSKI']
        elif selected_voivodeship == 'Opolskie':
            counties = ['OPOLE', 'BRZESKI', 'GŁUBCZYCKI', 'KĘDZIERZYŃSKO-KOZIELSKI', 'KLUCZBORSKI', 'KRAPKOWICKI', 'NAMYSŁOWSKI', 'NYSKI', 'OLESKI', 'OPOLSKI', 'PRUDNICKI', 'STRZELECKI']
        elif selected_voivodeship == 'Podkarpackie':
            counties = ['RZESZÓW', 'KROSNO', 'PRZEMYŚL', 'TARNOBRZEG', 'BIESZCZADZKI', 'BRZOZOWSKI', 'DĘBICKI', 'JAROSŁAWSKI', 'JASIELSKI', 'KOLBUSZOWSKI', 'KROŚNIEŃSKI', 'LESKI', 'LEŻAJSKI', 'LUBACZOWSKI', 'ŁAŃCUCKI', 'MIELECKI', 'NIŻAŃSKI', 'PRZEMYSKI', 'PRZEWORSKI', 'ROPCZYCKO-SĘDZISZOWSKI', 'RZESZOWSKI', 'SANOCKI', 'STALOWOWOLSKI', 'STRZYŻOWSKI', 'TARNOBRZESKI']
        elif selected_voivodeship == 'Podlaskie':
            counties = ['BIAŁYSTOK', 'ŁOMŻA', 'SUWAŁKI', 'AUGUSTOWSKI', 'BIAŁOSTOCKI', 'BIELSKI', 'GRAJEWSKI', 'HAJNOWSKI', 'KOLNEŃSKI', 'ŁOMŻYŃSKI', 'MONIECKI', 'SEJNEŃSKI', 'SIEMIATYCKI', 'SOKÓLSKI', 'SUWALSKI', 'WYSOKOMAZOWIECKI', 'ZAMBROWSKI']
        elif selected_voivodeship == 'Pomorskie':
            counties = ['GDAŃSK', 'GDYNIA', 'SŁUPSK', 'SOPOT', 'BYTOWSKI', 'CHOJNICKI', 'CZŁUCHOWSKI', 'KARTUSKI', 'KOŚCIERSKI', 'KWIDZYŃSKI', 'LĘBORSKI', 'MALBORSKI', 'NOWODWORSKI', 'GDAŃSKI', 'PUCKI', 'SŁUPSKI', 'STAROGARDZKI', 'SZTUMSKI', 'TCZEWSKI', 'WEJHEROWSKI']
        elif selected_voivodeship == 'Śląskie':
            counties =['KATOWICE', 'BIELSKO-BIAŁA', 'BYTOM', 'CHORZÓW', 'CZĘSTOCHOWA', 'DĄBROWA GÓRNICZA', 'GLIWICE', 'JASTRZĘBIE-ZDRÓJ', 'JAWORZNO', 'MYSŁOWICE', 'PIEKARY ŚLĄSKIE', 'RUDA ŚLĄSKA', 'RYBNIK', 'SIEMIANOWICE ŚLĄSKIE', 'SOSNOWIEC', 'ŚWIĘTOCHŁOWICE', 'TYCHY', 'ZABRZE', 'ŻORY', 'BĘDZIŃSKI', 'BIELSKI', 'BIERUŃSKO-LĘDZIŃSKI', 'CIESZYŃSKI', 'CZĘSTOCHOWSKI', 'GLIWICKI', 'KŁOBUCKI', 'LUBLINIECKI', 'MIKOŁOWSKI', 'MYSZKOWSKI', 'PSZCZYŃSKI', 'RACIBORSKI', 'RYBNICKI', 'TARNOGÓRSKI', 'WODZISŁAWSKI', 'ZAWIERCIAŃSKI', 'ŻYWIECKI']        
        elif selected_voivodeship == 'Świętokrzyskie':
            counties = ['KIELCE', 'BUSKI', 'JĘDRZEJOWSKI', 'KAZIMIERSKI', 'KIELECKI', 'KONECKI', 'OPATOWSKI', 'OSTROWIECKI', 'PIŃCZOWSKI', 'SANDOMIERSKI', 'SKARŻYSKI', 'STARACHOWICKI', 'STASZOWSKI', 'WŁOSZCZOWSKI']
        elif selected_voivodeship == 'Warmińsko-Mazurskie':
            counties = ['OLSZTYN', 'ELBLĄG', 'BARTOSZYCKI', 'BRANIEWSKI', 'DZIAŁDOWSKI', 'ELBLĄSKI', 'EŁCKI', 'GIŻYCKI', 'GOŁDAPSKI', 'IŁAWSKI', 'KĘTRZYŃSKI', 'LIDZBARSKI', 'MRĄGOWSKI', 'NIDZICKI', 'NOWOMIEJSKI', 'OLECKI', 'OLSZTYŃSKI', 'OSTRÓDZKI', 'PISKI', 'SZCZYCIEŃSKI', 'WĘGORZEWSKI']
        elif selected_voivodeship == 'Wielkopolskie':
            counties = ['POZNAŃ', 'KALISZ', 'KONIN', 'LESZNO', 'CHODZIESKI', 'CZARNKOWSKO-TRZCIANECKI', 'GNIEŹNIEŃSKI', 'GOSTYŃSKI', 'GRODZISKI', 'JAROCIŃSKI', 'KALISKI', 'KĘPIŃSKI', 'KOLSKI', 'KONIŃSKI', 'KOŚCIAŃSKI', 'KROTOSZYŃSKI', 'LESZCZYŃSKI', 'MIĘDZYCHODZKI', 'NOWOTOMYSKI', 'OBORNICKI', 'OSTROWSKI', 'OSTRZESZOWSKI', 'PILSKI', 'PLESZEWSKI', 'POZNAŃSKI', 'RAWICKI', 'SŁUPECKI', 'SZAMOTULSKI', 'ŚREDZKI', 'ŚREMSKI', 'TURECKI', 'WĄGROWIECKI', 'WOLSZTYŃSKI', 'WRZESIŃSKI', 'ZŁOTOWSKI']
        elif selected_voivodeship == 'Zachodniopomorskie':
            counties = ['SZCZECIN', 'KOSZALIN', 'ŚWINOUJŚCIE', 'BIAŁOGARDZKI', 'CHOSZCZEŃSKI', 'DRAWSKI', 'GOLENIOWSKI', 'GRYFICKI', 'GRYFIŃSKI', 'KAMIEŃSKI', 'KOŁOBRZESKI', 'KOSZALIŃSKI', 'ŁOBESKI', 'MYŚLIBORSKI', 'POLICKI', 'PYRZYCKI', 'SŁAWIEŃSKI', 'STARGARDZKI', 'SZCZECINECKI', 'ŚWIDWIŃSKI', 'WAŁECKI']
        else:
            counties = []

        self.county_combo.addItems(counties)
        
    def get_counties_for_voivodeship(self, selected_voivodeship):
        
        if selected_voivodeship == 'Dolnośląskie':
            return ['WROCŁAW', 'JELENIA GÓRA', 'LEGNICA', 'WAŁBRZYCH', 'BOLESŁAWIECKI', 'DZIERŻONIOWSKI', 'GŁOGOWSKI', 'GÓROWSKI', 'JAWORSKI', 'JELENIOGÓRSKI', 'KAMIENNOGÓRSKI', 'KŁODZKI', 'LEGNICKI', 'LUBAŃSKI', 'LUBIŃSKI', 'LWÓWECKI', 'MILICKI', 'OLEŚNICKI', 'OŁAWSKI', 'POLKOWICKI', 'STRZELIŃSKI', 'ŚREDZKI', 'ŚWIDNICKI', 'TRZEBNICKI', 'WAŁBRZYSKI', 'WOŁOWSKI', 'WROCŁAWSKI', 'ZĄBKOWICKI', 'ZGORZELECKI', 'ZŁOTORYJSKI']
        elif selected_voivodeship == 'Kujawsko-Pomorskie':
            return ['BYDGOSZCZ', 'TORUŃ', 'WŁOCŁAWEK', 'GRUDZIĄDZ', 'ALEKSANDROWSKI', 'BRODNICKI', 'BYDGOSKI', 'CHEŁMIŃSKI', 'GOLUBSKO-DOBRZYŃSKI', 'GRUDZIĄDZKI', 'INOWROCŁAWSKI', 'LIPNOWSKI', 'MOGILEŃSKI', 'NAKIELSKI', 'RADZIEJOWSKI', 'RYPIŃSKI', 'SĘPOLEŃSKI', 'ŚWIECKI', 'TORUŃSKI', 'TUCHOLSKI', 'WĄBRZESKI', 'WŁOCŁAWSKI', 'ŻNIŃSKI']
        elif selected_voivodeship == 'Mazowieckie':
            return ['WARSZAWA', 'OSTROŁĘKA', 'PŁOCK', 'RADOM', 'SIEDLCE', 'BIAŁOBRZESKI', 'CIECHANOWSKI', 'GARWOLIŃSKI', 'GOSTYNIŃSKI', 'GRODZISKI', 'GRÓJECKI', 'KOZIENICKI', 'LEGIONOWSKI', 'LIPSKI', 'ŁOSICKI', 'MAKOWSKI', 'MIŃSKI', 'MŁAWSKI', 'NOWODWORSKI', 'OSTROŁĘCKI', 'OSTROWSKI', 'OTWOCKI', 'PIASECZYŃSKI', 'PŁOCKI', 'PŁOŃSKI', 'PRUSZKOWSKI', 'PRZASNYSKI', 'PRZYSUSKI', 'PUŁTUSKI', 'RADOMSKI', 'SIEDLECKI', 'SIERPECKI', 'SOCHACZEWSKI', 'SOKOŁOWSKI', 'SZYDŁOWIECKI', 'WARSZAWSKI ZACHODNI', 'WĘGROWSKI', 'WOŁOMIŃSKI', 'WYSZKOWSKI', 'ZWOLEŃSKI', 'ŻUROMIŃSKI', 'ŻYRARDOWSKI']
        elif selected_voivodeship == 'Małopolskie':
            return ['KRAKÓW', 'NOWY SĄCZ', 'TARNÓW', 'BOCHEŃSKI', 'BRZESKI', 'CHRZANOWSKI', 'DĄBROWSKI', 'GORLICKI', 'KRAKOWSKI', 'LIMANOWSKI', 'MIECHOWSKI', 'MYŚLENICKI', 'NOWOSĄDECKI', 'NOWOTARSKI', 'OLKUSKI', 'OŚWIĘCIMSKI', 'PROSZOWICKI', 'SUSKI', 'TARNOWSKI', 'TATRZAŃSKI', 'WADOWICKI', 'WIELICKI']
        elif selected_voivodeship == 'Łódzkie':
            return ['ŁÓDŹ', 'PIOTRKÓW TRYBUNALSKI', 'SKIERNIEWICE', 'BEŁCHATOWSKI', 'BRZEZIŃSKI', 'KUTNOWSKI', 'ŁASKI', 'ŁĘCZYCKI', 'ŁOWICKI', 'ŁÓDZKI WSCHODNI', 'OPOCZYŃSKI', 'PABIANICKI', 'PAJĘCZAŃSKI', 'PIOTRKOWSKI', 'PODDĘBICKI', 'RADOMSZCZAŃSKI', 'RAWSKI', 'SIERADZKI', 'SKIERNIEWICKI', 'TOMASZOWSKI', 'WIELUŃSKI', 'WIERUSZOWSKI', 'ZDUŃSKOWOLSKI', 'ZGIERSKI']
        elif selected_voivodeship == 'Lubelskie':
            return ['LUBLIN', 'BIAŁA PODLASKA', 'CHEŁM', 'ZAMOŚĆ', 'BIALSKI', 'BIŁGORAJSKI', 'CHEŁMSKI', 'HRUBIESZOWSKI', 'JANOWSKI', 'KRASNOSTAWSKI', 'KRAŚNICKI', 'LUBARTOWSKI', 'LUBELSKI', 'ŁĘCZYŃSKI', 'ŁUKOWSKI', 'OPOLSKI', 'PARCZEWSKI', 'PUŁAWSKI', 'RADZYŃSKI', 'RYCKI', 'ŚWIDNICKI', 'TOMASZOWSKI', 'WŁODAWSKI', 'ZAMOJSKI']
        elif selected_voivodeship == 'Lubuskie':
            return ['GORZÓW WIELKOPOLSKI', 'ZIELONA GÓRA', 'GORZOWSKI', 'KROŚNIEŃSKI', 'MIĘDZYRZECKI', 'NOWOSOLSKI', 'SŁUBICKI', 'STRZELECKO-DREZDENECKI', 'SULĘCIŃSKI', 'ŚWIEBODZIŃSKI', 'WSCHOWSKI', 'ZIELONOGÓRSKI', 'ŻAGAŃSKI', 'ŻARSKI']
        elif selected_voivodeship == 'Opolskie':
            return ['OPOLE', 'BRZESKI', 'GŁUBCZYCKI', 'KĘDZIERZYŃSKO-KOZIELSKI', 'KLUCZBORSKI', 'KRAPKOWICKI', 'NAMYSŁOWSKI', 'NYSKI', 'OLESKI', 'OPOLSKI', 'PRUDNICKI', 'STRZELECKI']
        elif selected_voivodeship == 'Podkarpackie':
            return ['RZESZÓW', 'KROSNO', 'PRZEMYŚL', 'TARNOBRZEG', 'BIESZCZADZKI', 'BRZOZOWSKI', 'DĘBICKI', 'JAROSŁAWSKI', 'JASIELSKI', 'KOLBUSZOWSKI', 'KROŚNIEŃSKI', 'LESKI', 'LEŻAJSKI', 'LUBACZOWSKI', 'ŁAŃCUCKI', 'MIELECKI', 'NIŻAŃSKI', 'PRZEMYSKI', 'PRZEWORSKI', 'ROPCZYCKO-SĘDZISZOWSKI', 'RZESZOWSKI', 'SANOCKI', 'STALOWOWOLSKI', 'STRZYŻOWSKI', 'TARNOBRZESKI']
        elif selected_voivodeship == 'Podlaskie':
            return ['BIAŁYSTOK', 'ŁOMŻA', 'SUWAŁKI', 'AUGUSTOWSKI', 'BIAŁOSTOCKI', 'BIELSKI', 'GRAJEWSKI', 'HAJNOWSKI', 'KOLNEŃSKI', 'ŁOMŻYŃSKI', 'MONIECKI', 'SEJNEŃSKI', 'SIEMIATYCKI', 'SOKÓLSKI', 'SUWALSKI', 'WYSOKOMAZOWIECKI', 'ZAMBROWSKI']
        elif selected_voivodeship == 'Pomorskie':
            return ['GDAŃSK', 'GDYNIA', 'SŁUPSK', 'SOPOT', 'BYTOWSKI', 'CHOJNICKI', 'CZŁUCHOWSKI', 'KARTUSKI', 'KOŚCIERSKI', 'KWIDZYŃSKI', 'LĘBORSKI', 'MALBORSKI', 'NOWODWORSKI', 'GDAŃSKI', 'PUCKI', 'SŁUPSKI', 'STAROGARDZKI', 'SZTUMSKI', 'TCZEWSKI', 'WEJHEROWSKI']
        elif selected_voivodeship == 'Śląskie':
            return ['KATOWICE', 'BIELSKO-BIAŁA', 'BYTOM', 'CHORZÓW', 'CZĘSTOCHOWA', 'DĄBROWA GÓRNICZA', 'GLIWICE', 'JASTRZĘBIE-ZDRÓJ', 'JAWORZNO', 'MYSŁOWICE', 'PIEKARY ŚLĄSKIE', 'RUDA ŚLĄSKA', 'RYBNIK', 'SIEMIANOWICE ŚLĄSKIE', 'SOSNOWIEC', 'ŚWIĘTOCHŁOWICE', 'TYCHY', 'ZABRZE', 'ŻORY', 'BĘDZIŃSKI', 'BIELSKI', 'BIERUŃSKO-LĘDZIŃSKI', 'CIESZYŃSKI', 'CZĘSTOCHOWSKI', 'GLIWICKI', 'KŁOBUCKI', 'LUBLINIECKI', 'MIKOŁOWSKI', 'MYSZKOWSKI', 'PSZCZYŃSKI', 'RACIBORSKI', 'RYBNICKI', 'TARNOGÓRSKI', 'WODZISŁAWSKI', 'ZAWIERCIAŃSKI', 'ŻYWIECKI']        
        elif selected_voivodeship == 'Świętokrzyskie':
            return ['KIELCE', 'BUSKI', 'JĘDRZEJOWSKI', 'KAZIMIERSKI', 'KIELECKI', 'KONECKI', 'OPATOWSKI', 'OSTROWIECKI', 'PIŃCZOWSKI', 'SANDOMIERSKI', 'SKARŻYSKI', 'STARACHOWICKI', 'STASZOWSKI', 'WŁOSZCZOWSKI']
        elif selected_voivodeship == 'Warmińsko-Mazurskie':
           return ['OLSZTYN', 'ELBLĄG', 'BARTOSZYCKI', 'BRANIEWSKI', 'DZIAŁDOWSKI', 'ELBLĄSKI', 'EŁCKI', 'GIŻYCKI', 'GOŁDAPSKI', 'IŁAWSKI', 'KĘTRZYŃSKI', 'LIDZBARSKI', 'MRĄGOWSKI', 'NIDZICKI', 'NOWOMIEJSKI', 'OLECKI', 'OLSZTYŃSKI', 'OSTRÓDZKI', 'PISKI', 'SZCZYCIEŃSKI', 'WĘGORZEWSKI']
        elif selected_voivodeship == 'Wielkopolskie':
            return ['POZNAŃ', 'KALISZ', 'KONIN', 'LESZNO', 'CHODZIESKI', 'CZARNKOWSKO-TRZCIANECKI', 'GNIEŹNIEŃSKI', 'GOSTYŃSKI', 'GRODZISKI', 'JAROCIŃSKI', 'KALISKI', 'KĘPIŃSKI', 'KOLSKI', 'KONIŃSKI', 'KOŚCIAŃSKI', 'KROTOSZYŃSKI', 'LESZCZYŃSKI', 'MIĘDZYCHODZKI', 'NOWOTOMYSKI', 'OBORNICKI', 'OSTROWSKI', 'OSTRZESZOWSKI', 'PILSKI', 'PLESZEWSKI', 'POZNAŃSKI', 'RAWICKI', 'SŁUPECKI', 'SZAMOTULSKI', 'ŚREDZKI', 'ŚREMSKI', 'TURECKI', 'WĄGROWIECKI', 'WOLSZTYŃSKI', 'WRZESIŃSKI', 'ZŁOTOWSKI']
        elif selected_voivodeship == 'Zachodniopomorskie':
            return ['SZCZECIN', 'KOSZALIN', 'ŚWINOUJŚCIE', 'BIAŁOGARDZKI', 'CHOSZCZEŃSKI', 'DRAWSKI', 'GOLENIOWSKI', 'GRYFICKI', 'GRYFIŃSKI', 'KAMIEŃSKI', 'KOŁOBRZESKI', 'KOSZALIŃSKI', 'ŁOBESKI', 'MYŚLIBORSKI', 'POLICKI', 'PYRZYCKI', 'SŁAWIEŃSKI', 'STARGARDZKI', 'SZCZECINECKI', 'ŚWIDWIŃSKI', 'WAŁECKI']
    
    def get_voivodeship(self):
        return [ 'Dolnośląskie', 'Kujawsko-Pomorskie', 'Lubelskie', 'Lubuskie', 'Mazowieckie', 'Małopolskie', 'Opolskie', 'Podkarpackie', 'Podlaskie', 'Pomorskie', 'Warmińsko-Mazurskie', 'Wielkopolskie', 'Zachodniopomorskie', 'Łódzkie', 'Śląskie', 'Świętokrzyskie']
        
    def chooseSavePath(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        save_path, _ = QFileDialog.getSaveFileName(self, "Wybierz Ścieżkę Zapisu", "", "Pliki CSV (*.csv);;Wszystkie pliki (*)", options=options)
    
        if save_path:
            self.output_file_path = save_path

    def downloadCsv(self):
        voivodeship = self.voivodeship_combo.currentText()
        county = self.county_combo.currentText()
        from_date = self.from_date_edit.text()
        to_date = self.to_date_edit.text()
        
        if not from_date or not to_date:
            QMessageBox.warning(self, 'Błąd', 'Proszę wypełnić wszystkie pola.')
            return
            
        if hasattr(self, 'output_file_path'):
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    
            scrapped_data = []
            current_date = from_date
            latest_date = None
            if county and voivodeship:
                while current_date <= to_date:
                    if latest_date is None or current_date > latest_date:
                        sewikForm(voivodeship, county, current_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
                        additional_data = sewikScraper("sewik_page.html")
                        os.remove("sewik_page.html")
                        scrapped_data.extend(additional_data)
                        self.checked_dates.append(current_date.strftime("%Y-%m-%d"))
    
                        for entry in additional_data:
                            entry_date = datetime.datetime.strptime(entry['Data'][0], "%Y-%m-%d")
                            if latest_date is None or entry_date > latest_date:
                                latest_date = entry_date
                                current_date = entry_date
    
                    current_date += datetime.timedelta(days=1)
            elif voivodeship:
                counties_list = self.get_counties_for_voivodeship(voivodeship)
    
                for county in counties_list:
                    current_date = from_date
                    latest_date = None
                    while current_date <= to_date:
                        if latest_date is None or current_date > latest_date:
                            sewikForm(voivodeship, county, current_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
                            additional_data = sewikScraper("sewik_page.html")
                            os.remove("sewik_page.html")
                            scrapped_data.extend(additional_data)
    
                            for entry in additional_data:
                                entry_date = datetime.datetime.strptime(entry['Data'][0], "%Y-%m-%d")
                                if latest_date is None or entry_date > latest_date:
                                    latest_date = entry_date
                                    current_date = entry_date
    
                        current_date += datetime.timedelta(days=1)
            else:
                voivodeship_list = self.get_voivodeship()
                for voivodeship in voivodeship_list:
                    counties_list = self.get_counties_for_voivodeship(voivodeship)
        
                    for county in counties_list:
                        current_date = from_date
                        latest_date = None
                        while current_date <= to_date:
                            if latest_date is None or current_date > latest_date:
                                sewikForm(voivodeship, county, current_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
                                additional_data = sewikScraper("sewik_page.html")
                                os.remove("sewik_page.html")
                                scrapped_data.extend(additional_data)
        
                                for entry in additional_data:
                                    entry_date = datetime.datetime.strptime(entry['Data'][0], "%Y-%m-%d")
                                    if latest_date is None or entry_date > latest_date:
                                        latest_date = entry_date
                                        current_date = entry_date
        
                            current_date += datetime.timedelta(days=1)
    
            df = pd.DataFrame(scrapped_data)
            df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)
            df.to_csv(self.output_file_path, index=False, encoding='utf-8', sep=';')
        else:
            QMessageBox.warning(self, 'Błąd', 'Proszę wybrać ścieżkę zapisu pliku.')
            
            

def main():
    app = QApplication(sys.argv)
    window = sewikScraperApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()