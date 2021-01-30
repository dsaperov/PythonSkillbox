citizens = {'humans': [1, 2], 'cats': [3]}
cs = [being for beings in citizens.values() for being in beings]
for value in citizens.values():
    print(*value)
print(cs)