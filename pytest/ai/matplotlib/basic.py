

import matplotlib.pyplot as plt
import numpy as np




x = np.arange(1, 100)
y = x ** 2 - 3

# plot 线性图
plt.plot(x, y, label="y = x^2", c='red')
plt.xlabel("x")
plt.ylabel("y")

plt.show()

# bar 柱状图
#plt.bar(x, y)
#plt.show()


# hist 直方图
n = [1,2,2,2,2,3,3,4,4,7,7,7,7,7]

plt.hist(n)
plt.show()

# pie 扇状图



# scatter 散点图
plt.scatter(x, y)
plt.show()

