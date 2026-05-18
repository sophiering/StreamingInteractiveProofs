import matplotlib.pyplot as plt
import math
from miller_rabin_eval import eval_large_primes

k = [1,2,3,4,5,10,11]
n = [math.pow(2,5)]
correctness, runtimes = eval_large_primes(n, k)

fig, ax1 = plt.subplots()
ax1.set_title('Miller-Rabin for prime numbers')
ax1.set_xlabel('k')

ax1.plot(k, runtimes, 'purple')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(k, correctness)
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()