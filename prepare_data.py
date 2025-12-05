"""
Script de préparation et enrichissement des données d'accidents
Fusionne les fichiers CSV et enrichit les codes avec des descriptions
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Dictionnaires de mapping pour enrichir les données
MAPPINGS = {
    'lum': {
        1: 'Plein jour',
        2: 'Crépuscule ou aube',
        3: 'Nuit sans éclairage public',
        4: 'Nuit avec éclairage public non allumé',
        5: 'Nuit avec éclairage public allumé'
    },
    'atm': {
        -1: 'Non renseigné',
        1: 'Normale',
        2: 'Pluie légère',
        3: 'Pluie forte',
        4: 'Neige - grêle',
        5: 'Brouillard - fumée',
        6: 'Vent fort - tempête',
        7: 'Temps éblouissant',
        8: 'Temps couvert',
        9: 'Autre'
    },
    'col': {
        -1: 'Non renseigné',
        1: 'Deux véhicules - frontale',
        2: 'Deux véhicules - par l\'arrière',
        3: 'Deux véhicules - par le côté',
        4: 'Trois véhicules et plus - en chaîne',
        5: 'Trois véhicules et plus - collisions multiples',
        6: 'Autre collision',
        7: 'Sans collision'
    },
    'agg': {
        1: 'Hors agglomération',
        2: 'En agglomération'
    },
    'int': {
        -1: 'Non renseigné',
        1: 'Hors intersection',
        2: 'Intersection en X',
        3: 'Intersection en T',
        4: 'Intersection en Y',
        5: 'Intersection à plus de 4 branches',
        6: 'Giratoire',
        7: 'Place',
        8: 'Passage à niveau',
        9: 'Autre intersection'
    },
    'catr': {
        1: 'Autoroute',
        2: 'Route nationale',
        3: 'Route départementale',
        4: 'Voie communale',
        5: 'Hors réseau public',
        6: 'Parc de stationnement ouvert à la circulation publique',
        9: 'Autre'
    },
    'circ': {
        -1: 'Non renseigné',
        1: 'À sens unique',
        2: 'Bidirectionnelle',
        3: 'À chaussées séparées',
        4: 'Avec voies d\'affectation variable'
    },
    'surf': {
        -1: 'Non renseigné',
        1: 'Normale',
        2: 'Mouillée',
        3: 'Flaques',
        4: 'Inondée',
        5: 'Enneigée',
        6: 'Boue',
        7: 'Verglacée',
        8: 'Corps gras - huile',
        9: 'Autre'
    },
    'plan': {
        -1: 'Non renseigné',
        1: 'Partie rectiligne',
        2: 'En courbe à gauche',
        3: 'En courbe à droite',
        4: 'En S'
    },
    'prof': {
        -1: 'Non renseigné',
        1: 'Plat',
        2: 'Pente',
        3: 'Sommet de côte',
        4: 'Bas de côte'
    },
    'catv': {
        0: 'Indéterminable',
        1: 'Bicyclette',
        2: 'Cyclomoteur <50cm3',
        3: 'Voiturette (Quadricycle à moteur carrossé)',
        4: 'Scooter immatriculé',
        5: 'Motocyclette',
        6: 'Side-car',
        7: 'VL seul',
        8: 'VL + caravane',
        9: 'VL + remorque',
        10: 'VU seul (1,5T <= PTAC <= 3,5T)',
        11: 'VU (10) + caravane',
        12: 'VU (10) + remorque',
        13: 'PL seul (3,5T <PTCA <= 7,5T)',
        14: 'PL seul (> 7,5T)',
        15: 'PL (13) + remorque',
        16: 'PL (14) + remorque',
        17: 'PL > 7,5T + semi-remorque',
        18: 'Transport en commun',
        19: 'Tramway',
        20: 'Tracteur agricole',
        21: 'Véhicule ou engin spécial',
        30: 'Scooter < 50 cm3',
        31: 'Motocyclette > 50 cm3 et <= 125 cm3',
        32: 'Scooter > 50 cm3 et <= 125 cm3',
        33: 'Motocyclette > 125 cm3',
        34: 'Scooter > 125 cm3',
        35: 'Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)',
        36: 'Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)',
        37: 'Autobus',
        38: 'Autocar',
        39: 'Train',
        40: 'Tramway',
        41: 'Cyclomobilette légère',
        42: '3RL <= 50 cm3',
        43: '3RL > 50 cm3 <= 125 cm3',
        50: 'EDP à moteur',
        60: 'EDP sans moteur',
        80: 'VAE',
        99: 'Autre véhicule'
    },
    'obs': {
        -1: 'Non renseigné',
        0: 'Sans obstacle',
        1: 'Véhicule en stationnement',
        2: 'Arbre',
        3: 'Glissière métallique',
        4: 'Glissière béton',
        5: 'Autre glissière',
        6: 'Bâtiment, mur, pile de pont',
        7: 'Support de signalisation verticale ou poste d\'appel d\'urgence',
        8: 'Poteau',
        9: 'Mobilier urbain',
        10: 'Parapet',
        11: 'Îlot, refuge, borne haute',
        12: 'Bordure de trottoir',
        13: 'Fossé, talus, paroi rocheuse',
        14: 'Autre obstacle fixe sur chaussée',
        15: 'Autre obstacle fixe sur trottoir ou accotement',
        16: 'Sortie de chaussée sans obstacle',
        17: 'Buse - tête d\'aqueduc'
    },
    'choc': {
        -1: 'Non renseigné',
        0: 'Aucun',
        1: 'Avant',
        2: 'Avant droit',
        3: 'Avant gauche',
        4: 'Arrière',
        5: 'Arrière droit',
        6: 'Arrière gauche',
        7: 'Côté droit',
        8: 'Côté gauche',
        9: 'Chocs multiples (tonneaux)'
    },
    'manv': {
        -1: 'Non renseigné',
        0: 'Sans changement de direction',
        1: 'Même sens, même file',
        2: 'Entre 2 files',
        3: 'En marche arrière',
        4: 'À contresens',
        5: 'En franchissant le terre-plein central',
        6: 'En changeant de file à gauche',
        7: 'En changeant de file à droite',
        8: 'En déportant à gauche',
        9: 'En déportant à droite',
        10: 'En tournant à gauche',
        11: 'En tournant à droite',
        12: 'En faisant demi-tour sur la chaussée',
        13: 'En sortant du stationnement',
        14: 'En entrant en stationnement',
        15: 'En s\'insérant',
        16: 'En traversant la chaussée',
        17: 'Manœuvre de stationnement',
        18: 'Manœuvre d\'évitement',
        19: 'Ouverture de porte',
        20: 'Arrêté (hors stationnement)',
        21: 'En stationnement (avec occupants)',
        22: 'Circulant sur trottoir',
        23: 'Autres manœuvres'
    },
    'catu': {
        1: 'Conducteur',
        2: 'Passager',
        3: 'Piéton',
        4: 'Piéton en roller ou en trottinette'
    },
    'grav': {
        1: 'Indemne',
        2: 'Tué',
        3: 'Blessé hospitalisé',
        4: 'Blessé léger'
    },
    'sexe': {
        -1: 'Non renseigné',
        1: 'Masculin',
        2: 'Féminin'
    },
    'trajet': {
        -1: 'Non renseigné',
        0: 'Non renseigné',
        1: 'Domicile - travail',
        2: 'Domicile - école',
        3: 'Courses - achats',
        4: 'Utilisation professionnelle',
        5: 'Promenade - loisirs',
        9: 'Autre'
    },
    'secu1': {
        -1: 'Non renseigné',
        0: 'Aucun équipement',
        1: 'Ceinture',
        2: 'Casque',
        3: 'Dispositif enfants',
        4: 'Gilet réfléchissant',
        5: 'Airbag (2RM/3RM)',
        6: 'Gants (2RM/3RM)',
        7: 'Gants + Airbag (2RM/3RM)',
        8: 'Non déterminable',
        9: 'Autre'
    },
    'locp': {
        -1: 'Non renseigné',
        0: 'Sans objet ou non renseigné',
        1: 'Sur chaussée',
        2: 'Sur bande d\'arrêt d\'urgence',
        3: 'Sur accotement',
        4: 'Sur trottoir',
        5: 'Sur piste cyclable',
        6: 'Sur autre voie',
        8: 'Autre'
    },
    'actp': {
        -1: 'Non renseigné',
        0: 'Non renseigné ou sans objet',
        1: 'Sens marche du piéton',
        2: 'Sens inverse de marche du piéton',
        3: 'Traversant',
        4: 'Masqué',
        5: 'Jouant - courant',
        6: 'Avec animal',
        9: 'Autre'
    },
    'etatp': {
        -1: 'Non renseigné',
        0: 'Sans objet',
        1: 'Seul',
        2: 'Accompagné',
        3: 'En groupe'
    },
    'senc': {
        -1: 'Non renseigné',
        1: 'Sens croissant',
        2: 'Sens décroissant'
    },
    'motor': {
        -1: 'Non renseigné',
        1: 'Avant collision',
        2: 'Après collision'
    }
}

def enrichir_colonne(df, colonne, mapping):
    """Enrichit une colonne avec son mapping et garde la valeur originale"""
    if colonne in df.columns:
        df[f'{colonne}_code'] = df[colonne]
        df[f'{colonne}_desc'] = df[colonne].map(mapping).fillna('Non renseigné')
    return df

def calculer_age(an_nais, an_accident=2024):
    """Calcule l'âge à partir de l'année de naissance"""
    if pd.isna(an_nais) or an_nais == -1:
        return None
    return an_accident - an_nais

def determiner_periode_journee(heure):
    """Détermine la période de la journée"""
    if pd.isna(heure):
        return 'Non renseigné'
    try:
        h = int(str(heure).split(':')[0])
        if 6 <= h < 12:
            return 'Matin'
        elif 12 <= h < 18:
            return 'Après-midi'
        elif 18 <= h < 22:
            return 'Soirée'
        else:
            return 'Nuit'
    except:
        return 'Non renseigné'

def determiner_jour_semaine(jour, mois, an):
    """Détermine le jour de la semaine"""
    try:
        date = datetime(int(an), int(mois), int(jour))
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        return jours[date.weekday()]
    except:
        return 'Non renseigné'

def main():
    print("Debut du traitement des donnees d'accidents...")

    # 1. Chargement des données
    print("\nChargement des fichiers CSV...")
    caract = pd.read_csv('dataset/caract-2024.csv', sep=';', low_memory=False)
    lieux = pd.read_csv('dataset/lieux-2024.csv', sep=';', low_memory=False)
    vehicules = pd.read_csv('dataset/vehicules-2024.csv', sep=';', low_memory=False)
    usagers = pd.read_csv('dataset/usagers-2024.csv', sep=';', low_memory=False)

    print(f"  - Caractéristiques: {len(caract)} accidents")
    print(f"  - Lieux: {len(lieux)} enregistrements")
    print(f"  - Véhicules: {len(vehicules)} véhicules")
    print(f"  - Usagers: {len(usagers)} usagers")

    # Nettoyage des noms de colonnes
    vehicules.columns = [col.strip() for col in vehicules.columns]

    # 2. Fusion des données
    print("\nFusion des tables...")

    # Fusion caractéristiques + lieux (1:n)
    df = caract.merge(lieux, on='Num_Acc', how='left', suffixes=('', '_lieux'))
    print(f"  - Après fusion caract + lieux: {len(df)} lignes")

    # Fusion avec véhicules (n:m)
    df = df.merge(vehicules, on='Num_Acc', how='left', suffixes=('', '_veh'))
    print(f"  - Après fusion avec véhicules: {len(df)} lignes")

    # Fusion avec usagers (n:m)
    df = df.merge(usagers, on=['Num_Acc', 'id_vehicule', 'num_veh'], how='left', suffixes=('', '_usager'))
    print(f"  - Après fusion avec usagers: {len(df)} lignes")

    # 3. Enrichissement des données
    print("\nEnrichissement des donnees...")

    # Date et heure
    df['date'] = pd.to_datetime(df['an'].astype(str) + '-' +
                                df['mois'].astype(str).str.zfill(2) + '-' +
                                df['jour'].astype(str).str.zfill(2), errors='coerce')
    df['jour_semaine'] = df.apply(lambda x: determiner_jour_semaine(x['jour'], x['mois'], x['an']), axis=1)
    df['periode_journee'] = df['hrmn'].apply(determiner_periode_journee)
    df['est_weekend'] = df['jour_semaine'].isin(['Samedi', 'Dimanche']).astype(int)

    # Mois en texte
    mois_noms = {1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
                 7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'}
    df['mois_nom'] = df['mois'].astype(int).map(mois_noms)

    # Trimestre
    df['trimestre'] = ((df['mois'].astype(int) - 1) // 3) + 1

    # Âge des usagers
    df['age'] = df['an_nais'].apply(lambda x: calculer_age(x))
    df['tranche_age'] = pd.cut(df['age'],
                               bins=[0, 18, 25, 35, 45, 55, 65, 100],
                               labels=['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'])

    # Enrichissement avec les mappings
    for col, mapping in MAPPINGS.items():
        df = enrichir_colonne(df, col, mapping)

    # 4. Agrégations par accident
    print("\nCalcul des statistiques par accident...")

    # Statistiques par accident
    stats_usagers = usagers.groupby('Num_Acc').agg({
        'grav': lambda x: ((x == 2).sum(), (x == 3).sum(), (x == 4).sum(), (x == 1).sum()),
        'catu': lambda x: (x == 3).sum(),
        'sexe': lambda x: (x == 1).sum() / len(x) if len(x) > 0 else 0,
        'an_nais': lambda x: 2024 - x[x != -1].mean() if len(x[x != -1]) > 0 else None,
        'id_usager': 'count'
    }).reset_index()

    stats_usagers.columns = ['Num_Acc', 'gravite_stats', 'nb_pietons', 'pct_hommes', 'age_moyen', 'nb_usagers']
    stats_usagers[['nb_tues', 'nb_blesses_hospitalises', 'nb_blesses_legers', 'nb_indemnes']] = \
        pd.DataFrame(stats_usagers['gravite_stats'].tolist(), index=stats_usagers.index)
    stats_usagers = stats_usagers.drop('gravite_stats', axis=1)

    # Nombre de véhicules par accident
    stats_vehicules = vehicules.groupby('Num_Acc').size().reset_index(name='nb_vehicules')

    # Fusionner les stats
    df_accident = caract.merge(stats_usagers, on='Num_Acc', how='left')
    df_accident = df_accident.merge(stats_vehicules, on='Num_Acc', how='left')

    # Score de gravité
    df_accident['score_gravite'] = (df_accident['nb_tues'] * 100 +
                                    df_accident['nb_blesses_hospitalises'] * 30 +
                                    df_accident['nb_blesses_legers'] * 10)

    # Catégorie de gravité
    def categoriser_gravite(row):
        if row['nb_tues'] > 0:
            return 'Mortel'
        elif row['nb_blesses_hospitalises'] > 0:
            return 'Grave'
        elif row['nb_blesses_legers'] > 0:
            return 'Léger'
        else:
            return 'Matériel uniquement'

    df_accident['categorie_gravite'] = df_accident.apply(categoriser_gravite, axis=1)
    df_accident['accident_mortel'] = (df_accident['nb_tues'] > 0).astype(int)

    # Enrichir df_accident avec les données de lieux
    # On prend le premier lieu pour chaque accident (en général il n'y en a qu'un)
    lieux_enrichi = lieux.drop_duplicates('Num_Acc', keep='first')
    df_accident = df_accident.merge(lieux_enrichi[['Num_Acc', 'vma', 'nbv', 'catr', 'surf', 'plan', 'prof', 'circ', 'infra', 'situ']],
                                   on='Num_Acc', how='left', suffixes=('', '_lieux'))

    # Ajouter les descriptions pour toutes les colonnes
    for col, mapping in MAPPINGS.items():
        df_accident = enrichir_colonne(df_accident, col, mapping)

    # Enrichissement date
    df_accident['date'] = pd.to_datetime(df_accident['an'].astype(str) + '-' +
                                        df_accident['mois'].astype(str).str.zfill(2) + '-' +
                                        df_accident['jour'].astype(str).str.zfill(2), errors='coerce')
    df_accident['jour_semaine'] = df_accident.apply(lambda x: determiner_jour_semaine(x['jour'], x['mois'], x['an']), axis=1)
    df_accident['periode_journee'] = df_accident['hrmn'].apply(determiner_periode_journee)
    df_accident['est_weekend'] = df_accident['jour_semaine'].isin(['Samedi', 'Dimanche']).astype(int)
    df_accident['mois_nom'] = df_accident['mois'].astype(int).map(mois_noms)
    df_accident['trimestre'] = ((df_accident['mois'].astype(int) - 1) // 3) + 1

    # 5. Sauvegarde
    print("\nSauvegarde des fichiers...")

    # CSV détaillé (niveau usager)
    df.to_csv('dataset/accidents_complet_detaille.csv', index=False, encoding='utf-8-sig')
    print(f"  [OK] accidents_complet_detaille.csv cree ({len(df)} lignes)")

    # CSV synthétique (niveau accident)
    df_accident.to_csv('dataset/accidents_complet_synthese.csv', index=False, encoding='utf-8-sig')
    print(f"  [OK] accidents_complet_synthese.csv cree ({len(df_accident)} lignes)")

    # 6. Rapport de synthèse
    print("\n" + "="*60)
    print("RAPPORT DE SYNTHESE")
    print("="*60)
    print(f"Nombre total d'accidents: {len(caract):,}")
    print(f"Nombre total d'usagers impliques: {len(usagers):,}")
    print(f"Nombre total de vehicules: {len(vehicules):,}")
    print(f"\nAccidents mortels: {df_accident['accident_mortel'].sum():,}")
    print(f"Tues: {df_accident['nb_tues'].sum():,}")
    print(f"Blesses hospitalises: {df_accident['nb_blesses_hospitalises'].sum():,}")
    print(f"Blesses legers: {df_accident['nb_blesses_legers'].sum():,}")
    print(f"Indemnes: {df_accident['nb_indemnes'].sum():,}")
    print("\n" + "="*60)
    print("Traitement termine avec succes!")
    print("="*60)

if __name__ == '__main__':
    main()
