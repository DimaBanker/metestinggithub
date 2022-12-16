import numpy as np

start_spread = 0.25
sigma = 0.15
alpha = 0.01
avg_spread = 0.15
n = 5000
term = [i * 48 for i in range(1, 11)]
interval = 1 / 48
result = {}

for i in range(1, n + 1):

    s = [start_spread]

    for d in range(1, term[-1]):

        s.append(s[d - 1] + alpha * (avg_spread - s[d - 1]) + np.random.normal(0, sigma))

    for j in enumerate(term):

        t = j[1]
        loan_spread = [sum(s[-b:]) / b for b in range(t, 0, -1)]
        pl_list = [interval * (s[b - 1] - min(loan_spread[0:b])) for b in range(1, t + 1)]
        pl_sum = [sum(pl_list[:b]) for b in range(1, t + 1)]
        result[t] = result.get(t, 0) + pl_sum[t - 1] / (t * interval)

for k, v in result.items():
    print(k, v / n)


