# Segunda parte: ajuste dos dados ao gráfico
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Função do oscilador harmônico amortecido
def oscilador_amortecido(t, A, b, omega_d, phi):
    return A * np.exp(-b * t) * np.cos(omega_d * t + phi)

# Carrega os dados do arquivo txt
data = np.loadtxt('dados_ajustados.txt', skiprows=1, delimiter='\t')
tempo = data[:, 0]
posicao_x = data[:, 1]

m = 0.103  # em kg, medida na balança e com erro de 0,003, já que se esperava 100g

# Fornece valores iniciais razoáveis para melhorar o ajuste
A_inicial = np.max(posicao_x)
b_inicial = 0.1
omega_d_inicial = 2 * np.pi
phi_inicial = 0

# Ajuste dos parâmetros usando curve_fit
popt, _ = curve_fit(oscilador_amortecido, tempo, posicao_x, p0=[A_inicial, b_inicial, omega_d_inicial, phi_inicial])

# Valores ajustados
A, b, omega_d, phi = popt

# Calcular a curva ajustada
curva_ajustada = oscilador_amortecido(tempo, A, b, omega_d, phi)

omega_0 = np.sqrt((omega_d**2)+(b**2))
# Fator de qualidade (Q)
Q = (omega_0/(2*b))

print(f"Amplitude (A): {A:.4f}")
print(f"Fator de amortecimento (b): {b:.4f}")
print(f"Frequência amortecida (omega_d): {omega_d:.4f} rad/s")
print(f"Fase inicial (phi): {phi:.4f} rad")
print(f"Fator de qualidade (Q): {Q:.4f}")

# Plotagem dos dados
plt.plot(tempo, posicao_x, 'bo', label='Dados experimentais') 
plt.plot(tempo, curva_ajustada, 'r-', label='Curva ajustada')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (m)')
plt.legend()
plt.show()

