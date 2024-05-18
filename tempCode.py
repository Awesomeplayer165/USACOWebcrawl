
n = int(input())
pairs = 0
left = 0
for i in range(n):
    if input()[i] == '(':
        left += 1
    elif input()[i] == ')':
        if left > 0:
            pairs += 1
            left -= 1

print(pairs)
