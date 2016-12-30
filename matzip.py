mat1 = [[1,2,3], [4,5,6], [7,8,9]]
mat2 = [["a","b","c"], ["d","e","f"], ["g","h","i"]]

mat3 = zip(mat1, mat2)

print mat3

mat4 = [[3,4,5],[6,7,8],[9,10,11]]

mat5 = zip(*(mat1, mat4))
mat5a = zip(mat1, mat4)

print mat5
print mat5a

mat6 = []

for item in mat5:
    mat6.append(zip(item[0], item[1]))

print mat6

mat7 = []

for item in mat6:
    numlist = []
    for num in item:
        numlist.append((num[0]+num[1])/2)
    mat7.append(numlist)

print mat7
