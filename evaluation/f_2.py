import matplotlib.pyplot as plt
import math
import numpy as np
from f_2_eval import eval_f_2_m

n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_f_2_m("f_2_eval.txt", "f_2_helper.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Bivariate 2nd Frequency Moment')
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
from f_2_eval import eval_f_2_m

dim = 3
n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_f_2_m("f_2_eval.txt", n_vals, dim) 

fig, ax1 = plt.subplots()
ax1.set_title('Multivariate 2nd Frequency Moment : k = 3')
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
from f_2_eval import eval_f_2_m

dim = 4
n_vals = [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_h, runtimes_h, min_h, max_h, accuracy_d, runtimes_d, min_d, max_d = eval_f_2_m("f_2_eval.txt", n_vals, dim) 

fig, ax1 = plt.subplots()
ax1.set_title('Multivariate 2nd Frequency Moment : k = 4')
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



