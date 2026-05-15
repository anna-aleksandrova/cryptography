S = [i for i in range(256)]
K = [0 for _ in range(256)]

j = 0
for i in range(256):
    j = (j + S[i] + K[i]) % 256
    S[i], S[j] = S[j], S[i]
print(S)