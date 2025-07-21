
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
#graficos mas lindos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)

#leer el csv
df = pd.read_csv('clase2/air-quality-monitoring-sites-summary.csv')

#shape:una tupla de dimensiones de matriz que representan la forma de un DataFrame determinado.
#print(f"📊 Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
#print("\n🔍 Primeras 3 filas:")
#df.head(3)

#ver info general
#print(df.info())

#por defecto, include solo trae las estadisticas cuyas columnas son numericas
#si quiero todos los tipos de dato, usar el all
#print(df.describe(include='all'))

#eliminar columnas vacias
df = df.dropna(axis=1, how='all')

#eliminar columnas de indice (tipo clave primaria autoincrmental)si existen
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

#renombrar columnas con nombres mas limpios
#izquierda: nombre original, derecha: nombre nuevo
column_mapping = {
    'NSW air quality monitoring (AQMN) site': 'Site',
    'AQMN Region': 'Region',
    'Sub-region,where applicable': 'Subregion',
    'Site address': 'Address',
    'Latitude\n(South)': 'Latitude',
    'Longitude\n(East)': 'Longitude',
    'Altitude (ahd)': 'Altitude',
    'Commissioned': 'Commissioned',
    'Status': 'Status'
}

df = df.rename(columns=column_mapping)

# print(f"✅ Limpieza básica completada: {df.shape[0]} filas × {df.shape[1]} columnas")
# print("\n📋 Principales columnas:")
# main_cols = ['Site', 'Region', 'Address', 'Latitude', 'Longitude', 'Status']
# for col in main_cols:
#     if col in df.columns:
#         print(f"   ✓ {col}")
#
# # Ver ejemplo de coordenadas problemáticas
# print("\n🚨 Ejemplo de coordenadas (aún como texto):")
# if 'Latitude' in df.columns and 'Longitude' in df.columns:
#     print(f"   Latitud: {df['Latitude'].iloc[1]}")
#     print(f"   Longitud: {df['Longitude'].iloc[1]}")
# else:
#     print("   Las columnas 'Latitude' y/o 'Longitude' no existen en el DataFrame.")

#conteo de valores nulos por columna
#print(df.isna().sum())

#eliminar filas sin latitud, longitud o sitio
df = df.dropna(subset=['Latitude', 'Longitude', 'Site'])

def convert_dms_to_decimal(dms_string):
    """
    Convierte coordenadas DMS (ej: "32°38'56\"") a decimal (ej: -32.649)
    """
    if pd.isna(dms_string) or dms_string == '':
        return None
    
    try:
        # Buscar números en el texto
        numbers = re.findall(r'\d+(?:\.\d+)?', str(dms_string))
        
        if len(numbers) >= 2:
            degrees = float(numbers[0])
            minutes = float(numbers[1])
            seconds = float(numbers[2]) if len(numbers) > 2 else 0
            
            # Convertir a decimal
            decimal = degrees + minutes/60 + seconds/3600
            
            # En Australia, latitudes son negativas (sur)
            if 'South' in str(dms_string) or decimal > 0:
                decimal = -abs(decimal)
                
            return decimal
    except:
        pass
    
    return None

#print("🌐 Convirtiendo coordenadas DMS a decimal...")

# Convertir coordenadas
df['Latitude'] = df['Latitude'].apply(convert_dms_to_decimal)
df['Longitude'] = df['Longitude'].apply(convert_dms_to_decimal)

# Verificar resultado
valid_coords = df[['Latitude', 'Longitude']].notna().all(axis=1).sum()
"""print(f"✅ Conversión completada:")
print(f"   Coordenadas válidas: {valid_coords}/{len(df)} estaciones")
print(f"   Porcentaje exitoso: {(valid_coords/len(df)*100):.1f}%")

if valid_coords > 0:
    print(f"\n📍 Rango de coordenadas (Australia):")
    print(f"   Latitud: {df['Latitude'].min():.2f} a {df['Latitude'].max():.2f}")
    print(f"   Longitud: {df['Longitude'].min():.2f} a {df['Longitude'].max():.2f}")
    
# Filtrar datos válidos para análisis geográfico
df_geo = df.dropna(subset=['Latitude', 'Longitude', 'Site']).copy()
print(f"\n📊 Dataset final para análisis: {len(df_geo)} estaciones válidas")"""

#visualizaciones exploratorias
plt.figure(figsize=(12, 5))

# Distribución de altitudes
#alpha:trasparencia de elementos graficos
#bins:la forma en que se agrupan los datos para contar cuántos valores caen dentro de cada grupo. 
#subplot:para crear subgráficos dentro de una figura

"""plt.subplot(1, 2, 1)
altitude_data = df.dropna(subset=['Altitude'])['Altitude']
plt.hist(altitude_data, bins=15, color='lightblue', edgecolor='black', alpha=0.7)
plt.title("Distribución de Altitudes")
plt.xlabel("Altura (metros)")
plt.ylabel("Cantidad de estaciones")
plt.grid(True, alpha=0.3)

# Estadísticas básicas
plt.subplot(1, 2, 2)
# Crear un gráfico de caja simple
plt.boxplot(altitude_data, vert=True, patch_artist=True,
            boxprops={'facecolor': 'lightgreen', 'alpha': 0.7})
plt.ylabel("Altura (metros)")
plt.title("Estadísticas de Altitud")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
"""print(f"📊 Estadísticas de altitud ({len(altitude_data)} estaciones):")
print(f"   Mínima: {altitude_data.min():.0f}m")
print(f"   Máxima: {altitude_data.max():.0f}m")
print(f"   Promedio: {altitude_data.mean():.0f}m")
print(f"   Mediana: {altitude_data.median():.0f}m")"""

plt.figure(figsize=(12, 8))

# Mapa simple pero informativo de las estaciones
df_geo = df.dropna(subset=['Latitude', 'Longitude', 'Site']).copy()
"""plt.scatter(df_geo['Longitude'], df_geo['Latitude'], 
           c='red', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)

plt.title("Ubicaciones de Estaciones de Monitoreo en NSW, Australia")
plt.xlabel("Longitud (Este)")
plt.ylabel("Latitud (Sur)")
plt.grid(True, alpha=0.3)

plt.text(0.02, 0.98, f"Total: {len(df_geo)} estaciones", 
         transform=plt.gca().transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
         verticalalignment='top')

# Mejorar los límites para mostrar bien NSW
lat_range = df_geo['Latitude'].max() - df_geo['Latitude'].min()
lon_range = df_geo['Longitude'].max() - df_geo['Longitude'].min()
plt.xlim(df_geo['Longitude'].min() - lon_range*0.1, 
         df_geo['Longitude'].max() + lon_range*0.1)
plt.ylim(df_geo['Latitude'].min() - lat_range*0.1, 
         df_geo['Latitude'].max() + lat_range*0.1)

plt.tight_layout()
plt.show()

print(f"🌍 Cobertura geográfica:")
print(f"   📍 {len(df_geo)} estaciones distribuidas en NSW")
print(f"   📐 Área cubierta: ~{abs(lat_range)*111:.0f} km (Norte-Sur)")
print(f"   📐 Área cubierta: ~{abs(lon_range)*85:.0f} km (Este-Oeste)")"""

#CUANTOS SITIOS MIDEN CADA CONTAMINANTE?
cols_contaminantes = ['PM10', 'PM2.5', 'NO/NO2/NOx', 'SO2', 'O3', 'CO']
available_pollutants = [col for col in cols_contaminantes if col in df_geo.columns]

if available_pollutants:
    # Contar estaciones que miden cada contaminante
    pollutant_counts = df_geo[available_pollutants].notna().sum().sort_values(ascending=True)
    
    plt.figure(figsize=(10, 6))
    #plt.barh es una función de la biblioteca Matplotlib en Python que se utiliza para crear gráficos de barras horizontales
    bars = plt.barh(range(len(pollutant_counts)), pollutant_counts.values, 
                    color='coral', alpha=0.7)
    plt.yticks(range(len(pollutant_counts)), pollutant_counts.index)
    plt.xlabel("Número de estaciones")
    plt.title("🏭 Estaciones que Miden Cada Contaminante")
    plt.grid(True, alpha=0.3, axis='x')
    
    # Añadir valores en las barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center')
    
    plt.tight_layout()
    plt.show()
    
    print(f"⚗️ Análisis de contaminantes:")
    total_stations = len(df_geo)
    for pollutant, count in pollutant_counts.items():
        percentage = (count / total_stations) * 100
        print(f"   {pollutant:<12}: {count:3d} estaciones ({percentage:4.1f}%)")
        
    print(f"\n📊 Hallazgos:")
    print(f"   🥇 Más monitoreado: {pollutant_counts.index[-1]} ({pollutant_counts.iloc[-1]} estaciones)")
    print(f"   📉 Menos monitoreado: {pollutant_counts.index[0]} ({pollutant_counts.iloc[0]} estaciones)")
else:
    print("❌ No se encontraron columnas de contaminantes")

# Guardar el DataFrame limpio para futuros análisis
df.to_csv('clase2/cleaned_air_quality_data.csv', index=False)