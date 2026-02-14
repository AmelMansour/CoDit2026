# =========================================================
# Mashhad EMS ARP - Exact CPLEX Version with Metrics
# =========================================================

# ======= Section 0: Imports =======
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from scipy.spatial.distance import cdist
from docplex.mp.model import Model
import time

# ======= Section 1: Chemins =======
base_path = r"C:\Users\amelb\OneDrive\Bureau\MashhadDataset\\"

# ======= Section 2: Charger les données =======
calls = pd.read_excel(base_path + "Data_file_1_Mashhad_EMS_Calls.xlsx")
census_tracts = gpd.read_file(base_path + "02 Mashhad_Census_Tracts\\Mashhad_Census_Tracts.shp")
ambulance_stations = gpd.read_file(base_path + "03 Mashhad_Ambulance_Stations\\Mashhad_Ambulance_Stations.shp")

# ======= Section 3: Prétraitement spatial =======
census_tracts = census_tracts.to_crs(epsg=32640)
census_tracts["centroid"] = census_tracts.geometry.centroid

calls = calls.merge(
    census_tracts[['Tract_ID', 'centroid']],
    left_on='Census tract ID',
    right_on='Tract_ID',
    how='left'
)

calls['geometry'] = calls['centroid']
calls_gdf = gpd.GeoDataFrame(calls, geometry="geometry", crs="EPSG:32640")
calls_gdf = calls_gdf.dropna(subset=["geometry"]).reset_index(drop=True)

# Réduire dataset pour test
MAX_CALLS = 10
if len(calls_gdf) > MAX_CALLS:
    calls_gdf = calls_gdf.sample(MAX_CALLS, random_state=42).reset_index(drop=True)

stations_gdf = ambulance_stations.to_crs(epsg=32640)
stations_coords = np.array([[pt.x, pt.y] for pt in stations_gdf.geometry])
calls_coords = np.array([[pt.x, pt.y] for pt in calls_gdf.geometry])

print("Nombre d'appels EMS utilisés :", len(calls_gdf))

# ======= Section 4: Matrices de distances =======
dist_station_call = cdist(stations_coords, calls_coords)
dist_call_call = cdist(calls_coords, calls_coords)

# Paramètres ARP
N_calls = len(calls_gdf)
N_ambulances = 6                    # nombre d'ambulances pour le test exact
service_time = np.full(N_calls, 10.0)        # minutes
AMBULANCE_SPEED_KMH = 40
METERS_PER_MIN = (AMBULANCE_SPEED_KMH * 1000) / 60
critical_time = np.full(N_calls, 60.0)      # minutes

# ======= Section 5: Modèle CPLEX =======
mdl = Model(name="Mashhad_ARP_Exact")

# Variables binaires x[k,i] = 1 si ambulance k sert l'appel i
x = {(k,i): mdl.binary_var(name=f"x_{k}_{i}") for k in range(N_ambulances) for i in range(N_calls)}

# Variables de temps d'arrivée t[i] pour chaque appel
t = {i: mdl.continuous_var(lb=0, name=f"t_{i}") for i in range(N_calls)}

# ======= Section 6: Contraintes =======

# 1) Chaque appel doit être servi par exactement une ambulance
for i in range(N_calls):
    mdl.add_constraint(mdl.sum(x[k,i] for k in range(N_ambulances)) == 1, ctname=f"Call_{i}_served")

# 2) Temps critique pour chaque appel
for i in range(N_calls):
    mdl.add_constraint(t[i] <= critical_time[i], ctname=f"CriticalTime_{i}")

# 3) Temps minimal depuis la station pour chaque appel
for k in range(N_ambulances):
    for i in range(N_calls):
        travel_time = dist_station_call[k,i] / METERS_PER_MIN
        mdl.add_constraint(t[i] >= travel_time * x[k,i], ctname=f"Time_{k}_{i}")

# ======= Section 7: Fonction objectif =======
# Minimiser distance totale
total_distance = mdl.sum(x[k,i] * dist_station_call[k,i] for k in range(N_ambulances) for i in range(N_calls))
mdl.minimize(total_distance)

# ======= Section 8: Résolution avec temps de calcul =======
start = time.perf_counter()
solution = mdl.solve(log_output=True)
end = time.perf_counter()
comp_time = end - start

if solution:
    print("\n=== Solution CPLEX trouvée ===")
    metrics_total_distance = 0
    response_times = []
    critical_covered = 0

    for k in range(N_ambulances):
        served_calls = [i for i in range(N_calls) if x[k,i].solution_value > 0.5]
        if served_calls:
            print(f"Ambulance {k} sert appels : {served_calls}")
        # Calcul métriques
        time_i = 0
        for idx, i in enumerate(served_calls):
            if idx == 0:
                time_i = dist_station_call[k,i] / METERS_PER_MIN
                dist = dist_station_call[k,i]
            else:
                prev = served_calls[idx-1]
                dist = dist_call_call[prev, i]
                time_i += dist / METERS_PER_MIN + service_time[prev]
            metrics_total_distance += dist
            response_times.append(time_i)
            if time_i <= critical_time[i]:
                critical_covered += 1

    avg_response = np.mean(response_times) if response_times else 0

    print("\n=== Métriques finales ===")
    print(f"Distance totale (km)          : {metrics_total_distance/1000:.2f}")
    print(f"Temps de réponse moyen (min)  : {avg_response:.2f}")
    print(f"Nombre appels à temps critique: {critical_covered}/{N_calls}")
    print(f"Temps de calcul (s)           : {comp_time:.2f}")
else:
    print("Pas de solution trouvée. Vérifie le nombre d'ambulances ou le temps critique.")
