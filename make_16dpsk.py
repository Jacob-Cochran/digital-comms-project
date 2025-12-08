import numpy as np

pi = np.pi

angles = np.arange(0, 2*pi, 2*pi/16)

points = np.exp(1j * angles)


symbolMap = [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 8, 9]

# for point in points:
print("[", end="")
for i in range(len(points)):
    point = points[i]
    print(f"{point.real:.6f} + {point.imag:.6f}j,", end="")

print("]")



# print(points)
# print(symbolMap)