# etuovi_scrape

etuovi.py
..hakee annetun kiinteän osoitteen perusteella listan ilmoitusten suorista osoitteista
Esimerkiksi: url = 'https://www.etuovi.com/myytavat-asunnot/oulu?haku=M2140784029' sisältää Oulun kaikki myynnissä olevat kohteet

soup_testing.py

..hakee edellä luodun osoitelistan perusteella ilmoitussivun sisällön ja koostaa niistä CSV-tiedoston.

etuovi_dataframe_muokkaus.ipynb
..muokkaa edellä luotua CSV-tiedostoa yhtenäisempään muotoon. Täällä tapahtuu myös uuden ja vanhan dataframen yhdistäminen, jossa 1) lisätään uudet kohteet 2) merkitään "myydyiksi" kohteet, joita ei enää löydy 3) muodostetaan hae_kuvat.csv, jonka perusteella voidaan hakea kohteiden kuvat ja kuvaus omiin kansioihinsa.

