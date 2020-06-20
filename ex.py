dict = {'name': [1, 2, 8]}
print(dict['name'[:]])
print(dict['name'][0:2])

dict['name'][:2] = [2, 4, 5]
print(dict['name'][:])

list = [1, 3, 5, 7, 9]

for x in range(0, len(list)):
    print(list[x])
    x = x + 2
    # print(list[x])

import numpy

a = numpy.array([[0, 1, 2], [4, 7, 9], [5, 4, 3]])
print(a)
print(numpy.flip(a,1))

list1 = [1,2]
list2 = [2,1]
print(list1==list2)

x = 'abcdef'
tuple(x)