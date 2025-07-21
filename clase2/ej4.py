import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('clase2/cleaned_air_quality_data.csv')
plt.figure(figsize=(12, 8))

estacion_latitudes = df['Latitude']
estacion_longitudes = df['Longitude']
plt.scatter(estacion_longitudes, estacion_latitudes, 
            c='blue', alpha=0.5, s=10, edgecolors='black', linewidth=0.5)
plt.title("Ubicaciones de Estaciones de Monitoreo en NSW, Australia")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()