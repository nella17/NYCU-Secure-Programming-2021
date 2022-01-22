from solve import *

keys = np.array(initialize(7000))
scores = np.array([])
for i in keys:
    scores = np.append(scores, fitness(tuple(i)))

keys = keys[scores.argsort()[::-1]][:600]

for m in range(350):
    np.random.shuffle(keys)
    for i in range(len(keys)//2):
        child = np.array(crossover(keys[i*2], keys[i*2+1], 0.5))
        keys = np.concatenate((keys, [child]))

    np.random.shuffle(keys)
    for i in range(len(keys)//2):
        keys[i] = mutate(keys[i])

    scores = np.array([])
    for i in keys:
        scores = np.append(scores, fitness(tuple(i)))

    keys = keys[scores.argsort()[::-1]][:600]
    scores = scores[scores.argsort()[::-1]][:600]
    print(m, int(scores[0]))
    print(list(keys[0]))
    print(decrypt(ctx, keys[0]))
