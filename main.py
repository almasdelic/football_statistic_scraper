import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def view_statistics():
    print("Dobrodošli u sistem praćenja analiza utakmica klubova u sezoni 24/25...")
    time.sleep(2)
    print("Molimo sačekajte, učitavamo sistem...")
    time.sleep(2)
    
    data_for_excel =[]
    
    url = "https://fbref.com/en/comps/8/Champions-League-Stats"
    data = requests.get(url)

    soup = BeautifulSoup(data.text, features="lxml")
    
    standing_table = soup.select('table.stats_table')[0]  # Uzimamo tabelu sa timovima kroz klasu 'stats_table'1

    links = standing_table.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]

    team_urls = [f"https://fbref.com{l}" for l in links]  # Dodajem pravi link za svaki tim pojedinačno

    # Dobijanje naziva timova
    table_rows = standing_table.find_all('tr')
    teams = [row.find('a').text for row in table_rows if row.find('a')]

    # Prikaz timova sa indeksima
    print("Timovi koji učestvuju ove sezone:")
    for i, team in enumerate(teams):
        print(f"{i}: {team}")

    # Unos korisničkog izbora
    while True:
        try:
            tim_index = int(input("Za koji tim želite statistiku? Unesite indeks: "))
            if tim_index < 0 or tim_index >= len(teams):
                print("Unijeli ste neispravan indeks, molimo unesite validan indeks!")
            else:
                selected_team = teams[tim_index]
                team_url = team_urls[tim_index]
                break  # Izlazimo iz petlje ako je unos validan
        except ValueError:
            print("Greška: Unesite broj (validan indeks tima).")

    print(f"Izabrali ste tim: {selected_team} (Indeks: {tim_index}). Molim sačekajte da se podaci ispišu...")
    time.sleep(4)
    print("Još malo....")
    time.sleep(2)

    # Preuzimanje podataka o izabranom timu
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures") # Lociramo tabelu koja u sebi sadrzi text 'Scores & Fixtures'
    
    # Prikaz statistike utakmica
    print(f"Statistika utakmica za {selected_team}:")
    print(matches)
    
    # Dodavanje statistike utakmica u Excel
    for match in matches[0].values.tolist():
        data_for_excel.append(match)

    # Pitaj korisnika da li želi da sačuva podatke u Excel fajl
    save_to_excel = input("Želite li da sačuvate podatke u Excel fajl? (da/ne): ").lower()

    if save_to_excel == "da":
        # Upisivanje u Excel fajl sa nazivom kluba kao imenom fajla
        file_name = f"statistika_{selected_team}.xlsx"
        df = pd.DataFrame(data_for_excel)
        df.to_excel(file_name, index=False, header=False)
        print(f"Podaci su sačuvani u Excel fajl '{file_name}'.")
    elif save_to_excel == "ne":
        print("Podaci nisu sačuvani.")
    else:
        print("Nepoznat odgovor. Podaci nisu sačuvani.")

view_statistics()

print("*****************************")

# Pitanje korisniku da li želi da pogleda statistiku za drugi tim
while True:
    new_team = input("Želite li pogledati statistiku za drugi tim? (da/ne): ").lower()

    if new_team == "da":
        view_statistics()
    elif new_team == "ne":
        print("Hvala što ste koristili sistem!")
        break
    else:
        print("Molimo vas da unesete 'da' ili 'ne'.")

'''team_url = team_urls[0]
#print(team_url)
data = requests.get(team_url)
#print(data.text)

matches = pd.read_html(data.text, match="Scores & Fixtures") # Lociramo tabelu koja u sebi sadrzi text 'Scores & Fixtures'
#print(type(matches))
#print(matches)'''

