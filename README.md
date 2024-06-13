# Wymagane modułu
```
pip install openmeteo-requests
pip install requests-cache retry-requests numpy pandas
pip install flask
```
# Model LSTM
- train.py - trenowanie modelu według zadanych parametrów
- test.py - wykresy porównujące rzeczywiste dane i przewidywaną temperaturę
- data_preparation.py - skrypt pobierający dane do uczenia

# Analiza danych
analysis.ipynb - notebook z wszystkimi analizowanymi aspektami pogodowymi

# Aplikacja webowa
- web/backend.py - serwer udostępniajacy dane pogodowe z wybranego roku i miesiące
- clientApp/weather-app - readme o uruchamianiu aplikacji klienckiej wewnątrz folderu
