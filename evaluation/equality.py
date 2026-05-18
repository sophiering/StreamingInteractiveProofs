import matplotlib.pyplot as plt
import math
import numpy as np
from equality_eval import exact_eq

n_vals =  [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_t, runtimes_t, min_t, max_t, accuracy_f, runtimes_f, min_f, max_f = exact_eq("equality_eval.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Exact Equality')
ax1.set_xlabel('n')

mean_t = np.array(runtimes_t)
min_t = np.array(min_t)
max_t = np.array(max_t)

mean_f = np.array(runtimes_f)
min_f = np.array(min_f)
max_f = np.array(max_f)

t_err = [mean_t - min_t, max_t - mean_t]
f_err = [mean_f - min_f, max_f - mean_f]

plt.errorbar(n_vals, runtimes_t, yerr = t_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_f, yerr = f_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_t, 'blue')
ax2.plot(n_vals, accuracy_f, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

import matplotlib.pyplot as plt
import math
import numpy as np
from equality_eval import eval_eq

n_vals =  [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_t, runtimes_t, min_t, max_t, accuracy_f, runtimes_f, min_f, max_f = eval_eq("equality_eval.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Multiset Equality')
ax1.set_xlabel('n')

mean_t = np.array(runtimes_t)
min_t = np.array(min_t)
max_t = np.array(max_t)

mean_f = np.array(runtimes_f)
min_f = np.array(min_f)
max_f = np.array(max_f)

t_err = [mean_t - min_t, max_t - mean_t]
f_err = [mean_f - min_f, max_f - mean_f]

plt.errorbar(n_vals, runtimes_t, yerr = t_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_f, yerr = f_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_t, 'blue')
ax2.plot(n_vals, accuracy_f, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

import matplotlib.pyplot as plt
import math
import numpy as np
from equality_eval import exc_mr

n_vals =  [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_t, runtimes_t, min_t, max_t, accuracy_f, runtimes_f, min_f, max_f = exc_mr("equality_eval.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Exact Equality')
ax1.set_xlabel('n')

mean_t = np.array(runtimes_t)
min_t = np.array(min_t)
max_t = np.array(max_t)

mean_f = np.array(runtimes_f)
min_f = np.array(min_f)
max_f = np.array(max_f)

t_err = [mean_t - min_t, max_t - mean_t]
f_err = [mean_f - min_f, max_f - mean_f]

plt.errorbar(n_vals, runtimes_t, yerr = t_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_f, yerr = f_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_t, 'blue')
ax2.plot(n_vals, accuracy_f, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

import matplotlib.pyplot as plt
import math
import numpy as np
from equality_eval import exact_eq

n_vals =  [int(math.pow(2,5)), int(math.pow(2,10)), int(math.pow(2,12)), int(math.pow(2,13)), int(math.pow(2,14)), int(math.pow(2,15))]
accuracy_t, runtimes_t, min_t, max_t, accuracy_f, runtimes_f, min_f, max_f = exact_eq("equality_eval.txt", n_vals) 

fig, ax1 = plt.subplots()
ax1.set_title('Multiset Equality')
ax1.set_xlabel('n')

mean_t = np.array(runtimes_t)
min_t = np.array(min_t)
max_t = np.array(max_t)

mean_f = np.array(runtimes_f)
min_f = np.array(min_f)
max_f = np.array(max_f)

t_err = [mean_t - min_t, max_t - mean_t]
f_err = [mean_f - min_f, max_f - mean_f]

plt.errorbar(n_vals, runtimes_t, yerr = t_err, capsize=6, color='purple')
plt.errorbar(n_vals, runtimes_f, yerr = f_err, capsize=6, color='violet', linestyle='dotted')
ax1.set_ylabel('Average runtime (s)', color = 'purple')

ax2 = ax1.twinx()
ax2.plot(n_vals, accuracy_t, 'blue')
ax2.plot(n_vals, accuracy_f, 'lightblue', linestyle='dotted')
plt.ylim(0,110)
ax2.set_ylabel('Accuracy (%)', color = 'tab:blue')
plt.show()

