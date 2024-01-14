a = list(enumerate(list(['a', 'b', 'c'])))
# i = list([0, 2])
# for a1 in a:
#     print('---')
#     print(a1)
def foo(n):
    return n[0]
i = list(map(foo, a))
print(i)
# print(a[1])
# print(a) 