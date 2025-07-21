import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('clase2/cleaned_air_quality_data.csv')

#obtener coordenadas y determinar la estacion mas alta y la mas baja
estacion_mas_alta_row = df.loc[df['Latitude'].idxmax()]
estacion_mas_baja_row = df.loc[df['Latitude'].idxmin()]
print(f"Estación más alta: Sitio: {estacion_mas_alta_row['Site']}, Región: {estacion_mas_alta_row['Region']}")
print(f"Estación más baja: Sitio: {estacion_mas_baja_row['Site']}, Región: {estacion_mas_baja_row['Region']}")
