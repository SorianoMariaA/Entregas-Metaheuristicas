import numpy as np
import pandas as pd
import yfinance as yf
import time

start_time = time.time()
# Lista de símbolos de las acciones del S&P 500
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
symbols = df['Symbol'].tolist()

# Obtener precios de cierre ajustados de las acciones del S&P 500
start_date = '2021-01-01'  
end_date = '2022-12-30'    

data = yf.download(symbols, start=start_date, end=end_date)['Adj Close']

# Normalizar los datos
data_norm = data.pct_change()

# Parámetros del algoritmo PSO
num_particles = 100    # Número de partículas
num_iterations = 100   # Número de iteraciones
num_selected_assets = 20  # Número de activos a seleccionar
w_max = 0.9
w_min = 0.4               # Peso de la velocidad anterior
c1 = 1.49            # Peso de la mejor posición propia
c2 = 1.49                # Peso de la mejor posición global

# Rendimiento y riesgo promedio del S&P
returns = data_norm.mean()
risk = data_norm.std()

# Función objetivo (min)
def objective_function(position):
    selected_assets = np.where(position == 1)[0]
    returns_selected = returns[selected_assets]
    risk_selected = risk[selected_assets]
    avg_returns = returns_selected.mean()
    avg_risk = risk_selected.mean()
    #industries_selected = [df[df['Symbols'] == data.columns[i]]['GICS Sector'].values[0] for i in selected_assets]
    #industry_counts = pd.Series(industries_selected).value_counts()
    #max_industry_count = industry_counts.max()
    #industry_diversity_penalty = 0
    
    #if max_industry_count > 0.2 * len(selected_assets):
    #    industry_diversity_penalty = 0.1 * (max_industry_count - 0.2 * len(selected_assets))
    
    return abs(avg_returns - returns.mean()) + abs(avg_risk - risk.mean()) #+ industry_diversity_penalty

# Inicializar la matriz de posiciones
positions = np.zeros((num_particles, len(symbols)))

# Algoritmo PSO
best_positions = np.zeros((num_iterations, len(symbols)))
best_objectives = np.zeros(num_iterations)

for i in range(num_iterations):
    for j in range(num_particles): # Actualizar la velocidad y posición de cada partícula
        r1 = np.random.rand(len(symbols))
        r2 = np.random.rand(len(symbols))
        w = w_max - (w_max - w_min) * ((i / num_iterations) ** 2) #Inercia
        velocity = w * positions[j] + c1 * r1 * (best_positions[i] - positions[j]) + c2 * r2 * (best_positions[i] - positions[j])
        positions[j] = np.where(np.random.rand(len(symbols)) < 1 / (1 + np.exp(-velocity)), 1, 0)

        # Verificar que la suma de cada partícula sea igual al número de activos a seleccionar
        while positions[j].sum() != num_selected_assets:
            excess = positions[j].sum() - num_selected_assets
            if excess > 0:
                indices = np.where(positions[j] == 1)[0]
                np.random.shuffle(indices)
                positions[j][indices[0]] = 0
            else:
                indices = np.where(positions[j] == 0)[0]
                np.random.shuffle(indices)
                positions[j][indices[0]] = 1

    # F0 para cada partícula
    objectives = np.array([objective_function(p) for p in positions])

    # Actualizar la mejor posición global y su F0
    best_index = np.argmin(objectives)
    best_positions[i] = positions[best_index]
    best_objectives[i] = objectives[best_index]

# Activos seleccionados
selected_assets = np.where(best_positions[-1] == 1)[0]
selected_symbols = [data.columns[i] for i in selected_assets]
selected_data = data[selected_symbols]

end_time = time.time()
run_time = end_time - start_time
print("Tiempo de corrida: ", run_time, "segundos") #193.3687

data_New = selected_data.pct_change()
data_New.mean()
risk_New = data_New.std()
risk_New.mean()

print("Activos seleccionados:")
print(selected_symbols)
print()
