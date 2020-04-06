# AttesationNumeriqueCOVID-19
Générateur d'attestation numérique dérogatoire pour le confinement dû au Covid-19

## Installation
```bash
# Création de l'environment python
python3 -m virtualenv .venv --python=/usr/bin/python3

# Installation des dépendances
.venv/bin/pip install -r requirements 
```

## Utilisation
```bash
.venv/bin/python main.py \
	--first-name John \
	--last-name Doe \
	--birth-date 01/01/1900 \
	--birth-city Paname \
	--address "12 GRANDE RUE 75666 Paname" \
	--current-city Paname \
	--leave-date 06/04/2020 \
	--leave-hour 15:00 \
	--motifs travail-courses-sante-famille-sport-judiciaire-missions
```