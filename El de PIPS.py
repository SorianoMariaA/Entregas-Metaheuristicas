# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 20:50:27 2023

@author: Silvia
"""

import pandas as pd
import numpy as np
import yfinance as yf
from pyswarms import PSO
import pyswarms as ps
# Obtener lista de símbolos de las acciones del S&P 500
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
symbols = df['Symbol'].tolist()

# Obtener precios de cierre ajustados de las acciones del S&P 500
start_date = '2021-01-01'  # Fecha de inicio deseada ymd
end_date = '2022-12-30'    # Fecha de fin deseada

data = yf.download(symbols, start=start_date, end=end_date)['Adj Close']

# Get the returns
returns = data.pct_change()

# Create a particle swarm object
pso = PSO(n_particles=100, dimensions=len(returns))

# Set the inertia weight
pso.inertia_weight = 0.9

# Set the cognitive and social acceleration coefficients
pso.cognitive_acceleration_coefficient = 1.4
pso.social_acceleration_coefficient = 1.4

# Set the error tolerance
pso.error_tolerance = 1e-6

# Initialize the particles
pso.particles = np.random.rand(pso.n_particles, len(returns))

# Set the fitness function
def fitness(particles):
    # Calculate the portfolio return
    return np.sum(particles * returns)

# Run the PSO algorithm
pso.optimize(fitness, max_iter=1000)

# Get the best particle
best_particle = pso.best_particle

# Print the best particle
print(best_particle)