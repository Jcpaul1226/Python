#takes in a file and counts how many times each word occurs

#takes a list of words and counts how many times it is found
def occur(word):
    w = set(word)
    rows,cols = (len(w),2)
    arr1 = [[0 for i in range(cols)] for j in range(rows)]
    arr2 = [[0 for i in range(cols)] for j in range(rows)]
    n = 0
    j = 0
    i = 0
    while len(w) != 0:
        check = w.pop()
        n = word.count(check)
        arr1[j][0] = check
        arr1[j][1] = n
        j += 1
    for row in arr1:
        print(row)


print("Please Enter a file to list out words: ")
file = input()
f = open(file, "r")
words = f.read().split()
f.close()
print("This file has",len(words), "words in it and", len(set(words)), "of them are unique!")
arr = occur(words)
print(words)