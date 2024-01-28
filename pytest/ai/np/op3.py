import numpy as np

z = np.ones((3,4)) / 4
print(f"{z = }")

z[0]  = 1
print(f"{z = }")

z[0]  = 0
print(f"{z = }")

z[0,0] = 1
print(f"{z = }")


