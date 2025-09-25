"""
@author: Adam Balcerzak
"""
import openai
from openai import OpenAI
import pandas as pd

# Tworzenie instancji klienta OpenAI
client = OpenAI()

# Konfiguracja API OpenAI dodana za pomocą zmiennej admin cmd
# setx OPENAI_API_KEY "YOUR_API_KEY_HERE"

# Ścieżka do pliku wejściowego i wyjściowego
input_file = "input_prompts.xlsx"
output_file = "output_results.xlsx"

# Stały fragment prompta
static_prompt = "Jako dziennikarz napisz mi profesjonalny tweet na podany temat:"

# Funkcja do generowania odpowiedzi na podstawie prompta
def generate_response(input_text):
    prompt = f"{static_prompt} {input_text}"
    response = client.chat.completions.create(
        model="gpt-4o",  # Możesz użyć "gpt-4-turbo" dla szybszego działania
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=350,  # Maksymalna liczba tokenów w odpowiedzi
        temperature=0.7  # Kontrola kreatywności
    )
    # Pobranie tekstu z odpowiedzi
    return response.choices[0].message.content

# Wczytaj dane wejściowe z pliku .xlsx
data = pd.read_excel(input_file)
if 'Input' not in data.columns:
    raise ValueError("Plik musi zawierać kolumnę 'Input'.")

# Dodaj kolumnę Output i generuj odpowiedzi dla każdego wiersza
data['Output'] = data['Input'].apply(generate_response)

# Zapisz wyniki do nowego pliku .xlsx
data.to_excel(output_file, index=False)
print(f"Wyniki zapisane w pliku: {output_file}")
