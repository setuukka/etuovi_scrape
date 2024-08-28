#Tämä ohjelmaa ottaa etuovi.py:n tekemän listan kohteista, hakee niiden tiedot
#ja tallentaa ne (paivamaara)_data.csv -tiedostoon
#Se avataan etuovi_dataframe_muokkaus.ipynb tiedostossa ja hae_kuvat.ipynb tiedostossa



from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import random
import time
from datetime import datetime

def read_html(listing):
    #print("Reading HTML")
    with open(listing, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def get_soup(url, retries = 5):
    for attempt in range(retries):
        try:
            #Funktio hakee seuraavan kohteen lähdekoodin
            response = requests.get(url)
            if response.status_code == 200:
                #Tallennetaan soppa tiedostoon luettavaksi myöhemmin
                with open('listing.html', 'w', encoding='utf-8') as file:
                    file.write(response.text)


                soup = BeautifulSoup(response.content, 'html.parser')
                #print(f"Getting {url}")
                return soup
            else:
                print(f"Request failed with status code {response.status_code}")
                return None
        except PermissionError as e:
            print(f"Attempt {attempt + 1}/{retries} failed with error: {e}")
            if attempt < retries -1:
                time.sleep(1)
            else:
                raise


def wait_random():
    wait_time = random.uniform(0.5, 2)
    print(f"Waiting for {wait_time:.2f} seconds")
    time.sleep(wait_time)

def parse_html(html_content):
    #print("Parsing HTML")
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_price(soup):
    try:
        h3tags = soup.find_all('h3')

        hinta = [tag.get_text(strip = True).replace('\xa0','').replace('€','').strip() for tag in h3tags[0]]
        hinta = int(hinta[0])
    except: 
        hinta = 0
    return hinta

def test_between_ems(soup):
    em_dict = {}
    try:
        em_tags = soup.find_all('em')
        for i in range(len(em_tags)):
            current_em_text = em_tags[i].get_text(strip=True)
            # Get the position of the current </em> tag
            end_pos = str(soup).find(str(em_tags[i])) + len(str(em_tags[i]))
            # Determine the position of the next <em> tag or the end of the document
            if i + 1 < len(em_tags):
                start_pos = str(soup).find(str(em_tags[i + 1]))
            else:
                start_pos = len(str(soup))
            # Extract the text between them
            text_between = str(soup)[end_pos:start_pos]
            em_dict[current_em_text] = text_between.strip()
    except:
        em_dict = {}
    return em_dict

def extract_li(soup):
    list_items = soup.find_all('li')
    for li in list_items:
        print(li)
        print()

def sanahaku(soup, sana):
    results = []
    pienisana = sana.lower()
    for element in soup.find_all(string=True):
        if pienisana in element.lower():
            results.append(element)
    return results

def search_for_exact_phrase(soup, phrase):
    for element in soup.find_all(string=True):
        if phrase in element:
            return True
    return False

def extract_text_from_tags(em_list):
    stripped_dict = {}
    for i in range(len(em_list)):

        soup2 = BeautifulSoup(em_list[i][1], 'html.parser')
        soup2 = soup2.get_text(strip = True)
        stripped_dict[em_list[i][0]] = soup2

    poistettavat = ['Kokonaispinta-ala','Lisätietoja pinta-alasta','Käyttöönottovuosi','Vapautuminen','Hinta','Parvekkeen kuvaus','Kattomateriaali','Kattomateriaalin kuvaus','Huolto','Taloyhtiöön kuuluu','Energialuokka','Kaavoitustiedot','Kaavoitustilanne','Tontin vuokraaja']
    for poistettava in poistettavat:
        stripped_dict.pop(poistettava, None)
    
    return stripped_dict

def write_to_df(stripped_dict: dict):
    #Create a dict
    #features = {list_of_features[i]: list_of_features[i+1] for i in range(0, len(list_of_features),2)}

    new_df = pd.DataFrame([stripped_dict])
    return new_df

def dict_to_variables(sanakirja: dict):
    #for key, value in sanakirja.items():
        #print(key, value)
    list_of_features = []
    sijainti = sanakirja['Sijainti']
    tyyppi = sanakirja['Tyyppi']
    huoneistoselitelma = sanakirja['Huoneistoselitelmä']
    huoneita = sanakirja['Huoneita']
    pinta_ala = sanakirja['Asuintilojen pinta-ala']
    kerrokset = sanakirja['Kerrokset']
    rakennusvuosi = sanakirja['Rakennusvuosi']
    hinta2 = sanakirja['Hinta']
    sauna = sanakirja['Sauna']
    parveke = sanakirja['Parveke']
    kunto = sanakirja['Asunnon kunto']
    lammitys = sanakirja['Lämmitysjärjestelmän kuvaus']
    materiaali = sanakirja['Rakennus- ja pintamateriaalit']
    keittio = sanakirja['Keittiön kuvaus']
    kylpyhuone = sanakirja['Kylpyhuoneen kuvaus']
    olohuone = sanakirja['Olohuoneen kuvaus']
    makuuhuoneet = sanakirja['Makuuhuoneiden kuvaus']
    taloyhtio = sanakirja['Taloyhtiön nimi']
    isannoitsija = sanakirja['Isännöitsijän yhteystiedot']
    tehdyt_remontit = sanakirja['Tehdyt remontit']
    tulevat_remontit = sanakirja['Tulevat remontit']
    tontin_koko = sanakirja['Tontin koko']
    tontin_omistus = sanakirja['Tontin omistus']
    list_of_features.extend([sijainti, tyyppi, huoneistoselitelma, huoneita, pinta_ala, kerrokset, 
                            rakennusvuosi, hinta2, sauna, parveke, kunto, lammitys, materiaali, 
                            keittio, kylpyhuone, olohuone, makuuhuoneet, taloyhtio, isannoitsija,
                            tehdyt_remontit, tulevat_remontit, tontin_koko, tontin_omistus])
    return list_of_features 

def extract_housing_company(soup):
    if soup is None:
        print("soup is none")
        return None
    a_tag = soup.find('a', href=lambda href: href and '/taloyhtiot/' in href)
    if a_tag:
        print("in a tag")
        href_value = a_tag.get('href')
        y_tunnus = href_value.split('/')[-1]
        print(y_tunnus)
        return y_tunnus
    else:
        return None




if __name__ == "__main__":

    current_date = datetime.now().strftime('%d%m%Y') #otetaan päivämäärä
    filename = f"{current_date}_data.csv" #Muodostetaan tiedoston nimi päivämäärästä

    main_df = pd.DataFrame() #Luodaan uusi tyhjä dataframe
    #luetaan dataframe, jossa osoitteet kohteisiin
    etuovi_urls_df = pd.read_csv("24082024_listings.csv")
    #pienempi df testiä varten
    #etuovi_urls_df = etuovi_urls_df.head(5)

    #tähän kutsu funktioon, joka ottaa urlin, hakee sen perusteella soupin
    for i in range(0,len(etuovi_urls_df)):
        print(f"Iteraatio {i} / {len(etuovi_urls_df)}")
        url = etuovi_urls_df['URL'][i]
        print(url)
        #id = etuovi_urls_df['id'][i]
        try:
            soup = get_soup(url, retries = 5)
        except Exception as e:
            print(f"Failed to process {url}: {e}")
            continue

        wait_random()

    #html_content = read_html('listing.html')
    #soup = parse_html(html_content)
    
        hinta = extract_price(soup)
        y_tunnus = extract_housing_company(soup)
        em_dict = test_between_ems(soup)
        if len(em_dict) < 1:
            print(f"Skipping iteration {i} due to empty result")
            continue
        em_list = list(em_dict.items())

        stripped_dict = extract_text_from_tags(em_list)
        stripped_dict['hinta'] = hinta
        stripped_dict['url'] = url
        stripped_dict['haettu_pvm'] = current_date
        stripped_dict['myyty_pvm'] = None
        stripped_dict['myyty'] = 0   
        stripped_dict['y_tunnus'] = y_tunnus
        df = write_to_df(stripped_dict)
        main_df = pd.concat([main_df, df], ignore_index=True, sort=False)
        #print(df.head())
        print("Writing to csv")
        main_df.to_csv(filename, index=False)

    print("Processing complete!")