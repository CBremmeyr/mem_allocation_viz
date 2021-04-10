import random

gen_len = 25
file = open("process_seq.txt", 'w')
for i in range(gen_len-1):
    print(random.randint(1, 8), end=' ', file=file)
print(random.randint(1, 8), file=file)
