# Dashboard Accidents de la Route 2024

Analyse interactive des accidents de la circulation routière en France pour l'année 2024.

## Aperçu

Ce projet propose une visualisation des données d'accidents corporels issues de l'ONISR (data.gouv.fr). L'objectif est d'identifier les facteurs de risque et les périodes critiques pour orienter les actions de prévention.

## Démo en ligne

Repo github : https://github.com/ilyann0810/dataviz2

https://dataviz2-hrtgcdqbwmekjuwmrtib9a.streamlit.app/

## Installation locale

```bash
git clone https://github.com/ilyann0810/dataviz2.git
cd dataviz2
pip install -r requirements.txt
streamlit run app.py
```

## Données


Source : data.gouv.fr - Accidents corporels de la circulation routière

J'ai fusionné, nettoyé et filtré, avec le script prepare_data.py les 4 tables 2024 (caract, lieux, usagers, véhicules) en un seul fichier : `accidents_complet_synthese.csv`. 

- Source : [data.gouv.fr (ONISR)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)
- Période : 2024
- Licence : Licence Ouverte 2.0

## Auteur

Ilyann Mouisset--Ferrara - BDML2

Projet réalisé dans le cadre du cours de Data Visualization à l'EFREI.
