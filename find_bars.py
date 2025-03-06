import googlemaps
import pandas as pd
import os
from dotenv import load_dotenv

# 🔹 Carregar as variáveis do arquivo .env
load_dotenv()

# 🔹 Obter API Key do .env
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found! Check your .env file.")

# Inicializar cliente do Google Maps
gmaps = googlemaps.Client(key=API_KEY)

# Função para buscar bares em Madrid com filtro por categoria
def get_bars_in_madrid(query="bar"):
    bars_data = []
    location = "Madrid, Spain"

    # 🔹 Buscar lugares com base na consulta (ex: "rock bar in Madrid")
    places = gmaps.places(query=f"{query} in {location}")

    if "results" in places:
        for place in places["results"]:
            name = place.get("name", "N/A")
            address = place.get("formatted_address", "N/A")
            rating = place.get("rating", "N/A")
            place_id = place.get("place_id")

            # 🔹 Construir link do Google Maps para o lugar
            maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            bars_data.append({
                "Name": name,
                "Address": address,
                "Rating": rating,
                "Google Maps URL": maps_url
            })

    return bars_data

# Função para salvar os dados em CSV
def save_to_csv(data, filename="bars_madrid.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    category = input("Enter the type of bar (e.g., 'rock bar', 'cocktail bar'): ")
    bars = get_bars_in_madrid(category)
    
    if bars:
        save_to_csv(bars)
    else:
        print("No data found.")
