import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('clase2/cleaned_air_quality_data.csv')
#print('nombre columnas: ', df.columns.tolist())

#crear un grafico que muestre estaciones por region
region_counts = df['Region'].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(region_counts.index, region_counts.values, color='orange', alpha=0.7)
plt.title('Número de Estaciones por Región en NSW')
plt.ylabel('Cantidad de Estaciones')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()