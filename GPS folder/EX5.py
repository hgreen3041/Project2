import numpy as np
import matplotlib.pyplot as plt

N = 100000

X = np.random.uniform(0, 100, N)

Y = np.round(X)

Z = X - Y

z_val = np.linspace(-0.5, 0.5, 1000)
pdf_val = [1 if -0.5 <= z <= 0.5 else 0 for z in z_val]

E_Z = 1.0/12

plt.hist(Z, bins=50, density=True, alpha=0.6, color='b')

plt.plot(z_val, pdf_val, 'r-', linewidth=2)
plt.title('Histogram')
plt.xlabel('Quatizagtion Noise')
plt.ylabel('PDF')
plt.grid(True)
plt.show()

sample_average_Z = np.mean(Z**2)
print(f"Average from part : {E_Z}")
print(f"Sample average of Z^2 : {sample_average_Z}")
print(f"Error: {np.abs(E_Z-sample_average_Z)}")


