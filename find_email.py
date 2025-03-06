import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from serpapi import GoogleSearch
import time

# 🔹 Carregar a lista de bares do arquivo CSV
input_file = "bars_madrid.csv"
output_file = "bars_with_emails.csv"

API_KEY = os.getenv("SERPAPI_KEY")

# 🔹 Função para buscar o site do bar no Google usando SerpAPI
def get_website(bar_name):
    query = f"{bar_name} Madrid official site"
    
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": API_KEY
        })
        
        results = search.get_dict()
        if "organic_results" in results:
            for result in results["organic_results"]:
                url = result.get("link")
                if url and "facebook" not in url and "tripadvisor" not in url and "yelp" not in url:
                    return url  # Retorna o primeiro site que parece ser oficial
                
    except Exception as e:
        print(f"Error searching for {bar_name}: {e}")
    
    return None


# 🔹 Função para extrair e-mails do site
def find_email_in_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Procurar padrões de e-mail no texto da página
        import re
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

        if emails:
            return emails[0]  # Retorna o primeiro e-mail encontrado
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# 🔹 Processar cada bar e buscar o e-mail
bars_df = pd.read_csv(input_file)
emails_data = []

for index, row in bars_df.iterrows():
    bar_name = row["Name"]
    print(f"🔎 Searching for {bar_name}...")

    website = get_website(bar_name)
    email = None

    if website:
        print(f"🌍 Found website: {website}")
        email = find_email_in_website(website)
    
    emails_data.append({"Name": bar_name, "Email": email if email else "Not found"})

    # Aguardar um pouco para evitar bloqueios do Google
    time.sleep(3)

# 🔹 Salvar os e-mails no CSV
emails_df = pd.DataFrame(emails_data)
emails_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"✅ Process completed! Results saved in {output_file}")
