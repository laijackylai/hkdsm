import numpy as np

np.set_printoptions(suppress=True)

# test_file = open('6NW24C(e819n830,e820n830).txt', 'r')
# lines = test_file.readlines()

# northings = np.array([])
# eastings = np.array([])
# heights = np.array([])

# for line in lines:
#     inp = line.split(',')
#     east = float(inp[0])
#     north = float(inp[1])
#     height = float(inp[2])
#     northings = np.append(northings, north)
#     eastings = np.append(eastings, east)
#     heights = np.append(heights, height)

# print(len(northings))
# print(len(eastings))
# print(len(heights))

data = np.loadtxt('test.txt', dtype=np.float, delimiter=',')

sorted = np.sort(data, axis=0)
print(sorted)