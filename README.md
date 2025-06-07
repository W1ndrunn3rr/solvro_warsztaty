# Solvro Warsztaty

## Wymagania

- Python 3.12 lub nowszy
- Poetry (opcjonalnie) lub pip

## Instalacja

### Opcja 1: Używając Poetry (zalecane)

```bash
# Zainstaluj zależności
poetry install
```

### Opcja 2: Używając pip

```bash
# Utwórz środowisko wirtualne (opcjonalnie)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate     # Windows

# Zainstaluj zależności
pip install torch torchvision Pillow
```

## Uruchamianie

### Z Poetry
Linux :
```bash
poetry run python image_classifier_app.py
```

Windows:
```bash
python -m poetry run python image_classifier_app.py
```

### Bez Poetry

Linux: 
```bash
# W katalogu projektu (z aktywnym środowiskiem wirtualnym)
python image_classifier_app.py
```

Windows: 
```bash
# W katalogu projektu (z aktywnym środowiskiem wirtualnym)
python image_classifier_app.py
```

## Jak używać aplikacji

1. **Uruchom aplikację** - wykonaj powyższe komendy
2. **Wgraj obraz** - kliknij przycisk "Wgraj Obraz" i wybierz plik obrazu (JPEG, PNG, BMP, TIFF)
3. **Podejrzyj obraz** - wybrany obraz pojawi się w oknie aplikacji
4. **Klasyfikuj** - kliknij przycisk "Przewiduj" aby uruchomić klasyfikację
5. **Zobacz wynik** - wynik (0 lub 1) pojawi się w oknie alertu wraz z poziomem pewności

## Obsługiwane formaty obrazów

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Troubleshooting

### Błąd: "Nie znaleziono pliku modelu"
- Upewnij się, że plik `model.pth` znajduje się w głównym katalogu projektu

### Problemy z GUI na Linux
- Upewnij się, że masz zainstalowane biblioteki GUI:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
```