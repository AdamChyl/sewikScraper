import requests
from bs4 import BeautifulSoup

def sewikToCsv(url):
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for h2 in soup.find_all('h2'):
            
            h2_text = h2.get_text()
            
            if h2_text.startswith("Zdarzenie"):
                id_zdarzenia = int(h2_text.replace("Zdarzenie ", "").strip())
                
        for script in soup.find_all('script'):
            
            script_text = script.get_text()
            
            if 'new OpenLayers.LonLat(' in script_text:
                start_index = script_text.find('new OpenLayers.LonLat(')
                end_index = script_text.find(')', start_index)
                coordinates_text = script_text[start_index+len('new OpenLayers.LonLat('):end_index]
                lon, lat = map(float, coordinates_text.split(','))
                longitude = lon
                latitude = lat
                
        for li in soup.find_all('li'):
            text_li = li.get_text().strip()
            
            if text_li.startswith("WOJ."):
                wojewodztwo = text_li.replace("WOJ. ", "").strip().title()
                
            elif text_li.startswith("Powiat:"):
                powiat = text_li.replace("Powiat: POWIAT", "").strip().title()
                
            elif text_li.startswith("Gmina:"):
                gmina = text_li.replace("Gmina: ", "").strip().title()
                
            elif text_li.startswith("Adres:"):
                if "\n" in text_li:
                    lines = text_li.replace("Adres: ", "").strip().split("\n")
                    adres = " ".join(line.strip() for line in lines).title()
                else:
                    adres = text_li.replace("Adres: ", "").strip().title()
            
            elif text_li.startswith("Data:"):
                data = text_li.replace("Data: ", "").strip().title()
                
            elif text_li.startswith("Godzina:"):
                godzina = text_li.replace("Godzina: ", "").strip().title()
                
            elif text_li.startswith("Charakterystyka miejsca\n                zdarzenia:"):
                miejsce_zdarzenia = text_li.replace("Charakterystyka miejsca\n                zdarzenia:", "").strip().title()
            
            elif text_li.startswith("Teren zabudowany:"):
                obszar = text_li.replace("Teren zabudowany: Obszar", "").strip().title()
                
            elif text_li.startswith("Ograniczenie prędkości:"):
                ograniczenie_tab = text_li.replace("Ograniczenie prędkości:", "").split()
                ograniczenie = ograniczenie_tab[0].strip().title()
        

        for h3_tag in soup.find_all('h3'):
            if h3_tag.get_text() == "Rodzaj zdarzenia":
               ul = h3_tag.find_next('ul')
               if ul:
                   li_rodzaj_zdarzenia = ul.find('li')
                   if li_rodzaj_zdarzenia:
                       rodzaj_zdarzenia = li_rodzaj_zdarzenia.get_text().strip()
                       
            if h3_tag.text == "Inne przyczyny zdarzenia":
                ul = h3_tag.find_next('ul')
                if ul:
                    li_przyczyna = ul.find('li')
                    if li_przyczyna:
                        inne_przyczyny = li_przyczyna.text.strip()
                    else:
                        inne_przyczyny = "Brak"
        
        
        uczestnicy = []
        uczestnicy_counter = -1
        sprawca_id = None
        przyczyna = None
        przyczny_zdarzen = ['Zderzenie pojazdów czołowe', 'Zderzenie pojazdów boczne', 'Zderzenie pojazdów tylne', 'Najechanie na pieszego', 'Zdarzenie z osobą UWR', 'Najechanie na pojazd unieruchomiony', 'Najechanie na drzewo, słup, inny obiekt drogowy', 'Najechanie na drzewo', 'Najechanie na słup, znak', 'Najechanie na zaporę kolejową', 'Najechanie na dziurę, wybój, garb', 'Najechanie na zwierzę', 'Najechanie na barierę ochronną', 'Wywrócenie się pojazdu', 'Wypadek z pasażerem', 'Inne', 'Niedostosowanie prędkości do warunków ruchu', 'Nieudzielenie pierwszeństwa przejazdu', 'Nieudzielenie pierwszeństwa pieszemu', 'Nieprawidłowe: wyprzedzanie', 'Nieprawidłowe: omijanie', 'Nieprawidłowe: wymijanie', 'Nieprawidłowe: przejeżdżanie przejścia dla pieszych', 'Nieprawidłowe: przejeżdżanie przejścia dla rowerów', 'Nieprawidłowe: skręcanie', 'Nieprawidłowe: zmienianie pasa ruchu', 'Nieprawidłowe: Zawracanie', 'Nieprawidłowe: zatrzymywanie, postój', 'Nieprawidłowe: cofanie', 'Jazda po niewłaściwej stronie drogi', 'Wjazd przy czerwonym świetle', 'Nieprzestrzeganie innych sygnałów', 'Niezachowanie bezp. odl. między pojazdami', 'Gwałtowne hamowanie', 'Jazda bez wymaganego oświetlenia', 'Zmęczenie, zaśnięcie', 'Ograniczenie sprawności psychomotorycznej', 'Nieustąpienie pierwszeństwa pieszemu na przejściu dla pieszych', 'Nieustąpienie pierwszeństwa pieszemu przy skręcaniu w drogę poprzeczną', 'Wyprzedzanie pojazdu przed przejściem dla pieszych', 'Omijanie pojazdu przed przejściem dla pieszych', 'Nieprawidłowe przejeżdżanie przejazdu dla rowerzystów', 'Nieustąpienie pierwszeństwa pieszemu w innych okolicznościach', 'Niestosowanie się do sygnalizacji świetlnej', 'Inne przyczyny', 'Inne', 'Pożar pojazdu', 'Niezawiniona niesprawność techniczna pojazdu', 'Niewłaściwy stan jezdni', 'Nieprawidłowa organizacja ruchu', 'Nieprawidłowo zabezp. roboty drogowe', 'Nieprawidłowo działająca sygn. świetlna', 'Nieprawidłowo działająca zapora, rogatka', 'Obiekty, zwierzęta na drodze', 'Nagłe zasłabnięcie kierującego', 'Oślepienie przez inny pojazd lub słońce', 'Z winy pasażera: wyskak. z pojazdu w ruchu', 'Z winy pasażera: wypadnięcie', 'Z winy pasażera', 'Nieustalone', 'Inne, nieustalone', 'Inne', 'Niesprawność techniczna pojazdu', 'Utrata przytomności, śmierć kierującego']
        typy = ["Samochód ciężarowy DMC powyżej 3,5 T", "Samochód ciężarowy DMC powyżej do 3,5 T", "Samochód osobowy", "Rower", "Motorower", "Hulajnoga elektryczna", "Urządzenie transportu osobistego", "Czterokołowiec", "Samochód ciężarowy", "Autobus", "Tramwaj, trolejbus", "Traktor", "Pociąg", "Inny", "Nieznany", "Autobus komunikacji publicznej", "Motocykl", "Motocykl inny", "Pojazd nieustalony", "Motocykl o poj. do 125 cm3 (do 11 kw/0,1 KW/kg)", "Hulajnoga elektryczna (od 2022)", "Ciągnik rolniczy", "Autobus inny", "Urządzenie transportu osobistego (od 2022)"]

        for strong_tag in soup.find_all('strong'):
            strong_text = strong_tag.text.strip()            
            if strong_tag.text in typy:
                ul = strong_tag.find_next('ul')
                if ul:
                    li_pojazd = ul.find('li')
                    if li_pojazd:
                        uczestnicy.append(strong_tag.text.strip() + " " + li_pojazd.text.strip())
                        uczestnicy_counter += 1
                        
            if strong_tag.text == "Pieszy":
                uczestnicy.append("Pieszy")
                uczestnicy_counter += 1
                
            if strong_text in przyczny_zdarzen:
                przyczyna = strong_text
                sprawca_id = uczestnicy_counter
        
        data_dict = {
            'Id': [id_zdarzenia],
            'Województwo': [wojewodztwo],
            'Powiat': [powiat],
            'Gmina': [gmina],
            'Adres': [adres],
            'Data': [data],
            'Godzina': [godzina],
            'Rodzaj_zdarzenia': [rodzaj_zdarzenia],
            'Miejsce_zdarzenia': [miejsce_zdarzenia],
            'Obszar': [obszar],
            'Ograniczenie_predkosci': [ograniczenie],
            'Przyczyna': [przyczyna],
            'Inne przyczyny': [inne_przyczyny],
            'longitude': [longitude],
            'latitude ': [latitude],
        }
        
        if sprawca_id is not None:
            data_dict['Sprawca'] = uczestnicy[sprawca_id]
            
        if len(uczestnicy) > 0: 
            for idx, uczestnik in enumerate(uczestnicy, start=1,):
                if idx-1 != sprawca_id:
                    data_dict[f'Uczestnik_{idx}'] = uczestnicy[idx-1]
        
        bledne_id = [97821538, 97926429, 98053322]
        
        if id_zdarzenia in bledne_id:
            raise Exception("Błąd Id")
        else:
            return data_dict
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Błąd HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Błąd połączenia: {conn_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Inny błąd zapytania: {req_err}")
    except Exception as e:
        print(f"Inny błąd: {e}")