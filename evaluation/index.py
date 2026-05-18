import matplotlib.pyplot as plt
import math
import numpy as np
from index_eval import eval_index

n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_index("index_eval.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Index')
ax1.set_xlabel('n')

mean_h = np.array(runtimes_h)
min_h = np.array(min_h)
max_h = np.array(max_h)

mean_d = np.array(runtimes_d)
min_d = np.array(min_d)
max_d = np.array(max_d)

h_err = [mean_h - min_h, max_h - mean_h]
d_err = [mean_d - min_d, max_d - mean_d]
plt.errorbar(n_vals, runtimes_h, yerr = h_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_d, yerr = d_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_h, 'blue')
ax2.plot(n_vals, accuracy_d, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()



import matplotlib.pyplot as plt
import math
import numpy as np
from index_eval import eval_multivariate

n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15)), int(math.pow(2,16))]
dim = 3
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_multivariate("index_eval.txt", n_vals, dim) 

fig, ax1 = plt.subplots()
ax1.set_title('Multivariate Index : k = 3')
ax1.set_xlabel('n')

mean_h = np.array(runtimes_h)
min_h = np.array(min_h)
max_h = np.array(max_h)

mean_d = np.array(runtimes_d)
min_d = np.array(min_d)
max_d = np.array(max_d)

h_err = [mean_h - min_h, max_h - mean_h]
d_err = [mean_d - min_d, max_d - mean_d]
plt.errorbar(n_vals, runtimes_h, yerr = h_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_d, yerr = d_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_h, 'blue')
ax2.plot(n_vals, accuracy_d, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()



import matplotlib.pyplot as plt
import math
import numpy as np
from index_eval import eval_multivariate

n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15)), int(math.pow(2,16))]
dim = 4
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_multivariate("index_eval.txt", n_vals, dim) 

fig, ax1 = plt.subplots()
ax1.set_title('Multivariate Index : k = 4')
ax1.set_xlabel('n')

mean_h = np.array(runtimes_h)
min_h = np.array(min_h)
max_h = np.array(max_h)

mean_d = np.array(runtimes_d)
min_d = np.array(min_d)
max_d = np.array(max_d)

h_err = [mean_h - min_h, max_h - mean_h]
d_err = [mean_d - min_d, max_d - mean_d]
plt.errorbar(n_vals, runtimes_h, yerr = h_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_d, yerr = d_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_h, 'blue')
ax2.plot(n_vals, accuracy_d, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()



import matplotlib.pyplot as plt
import math
import numpy as np
from index_eval import eval_honest_v_index

dim = 3
n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_honest_v_index("index_eval.txt", dim, n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Honest Verifier ZK Index : k = 3')
ax1.set_xlabel('n')

mean_h = np.array(runtimes_h)
min_h = np.array(min_h)
max_h = np.array(max_h)

mean_d = np.array(runtimes_d)
min_d = np.array(min_d)
max_d = np.array(max_d)

h_err = [mean_h - min_h, max_h - mean_h]
d_err = [mean_d - min_d, max_d - mean_d]
plt.errorbar(n_vals, runtimes_h, yerr = h_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_d, yerr = d_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_h, 'blue')
ax2.plot(n_vals, accuracy_d, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

import matplotlib.pyplot as plt
import math
import numpy as np
from index_eval import eval_zk_index

n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
dim = 3
accuracy_h, runtimes_h, min_h, max_h, accuracy_d_p, runtimes_d_p, min_d_p, max_d_p, accuracy_d_v, runtimes_d_v, min_d_v, max_d_v = eval_zk_index("index_eval.txt", dim, n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('ZK Index : k = 3')
ax1.set_xlabel('n')

mean_h = np.array(runtimes_h)
min_h = np.array(min_h)
max_h = np.array(max_h)

mean_d_p = np.array(runtimes_d_p)
min_d_p = np.array(min_d_p)
max_d_p = np.array(max_d_p)

mean_d_v = np.array(runtimes_d_v)
min_d_v = np.array(min_d_v)
max_d_v = np.array(max_d_v)

h_err = [mean_h - min_h, max_h - mean_h]
d_p_err = [mean_d_p - min_d_p, max_d_p - mean_d_p]
d_v_err = [mean_d_v - min_d_v, max_d_v - mean_d_v]
plt.errorbar(n_vals, runtimes_h, yerr = h_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_d_p, yerr = d_p_err, capsize=6, color='violet', linestyle='dotted')
plt.errorbar(n_vals, runtimes_d_v, yerr = d_v_err, capsize=6, color='pink', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_h, 'blue')
ax2.plot(n_vals, accuracy_d_p, 'lightblue', linestyle='dotted')
ax2.plot(n_vals, accuracy_d_v, 'teal', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

