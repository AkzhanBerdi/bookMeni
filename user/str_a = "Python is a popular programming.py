def evenNum(num):
    if num % 2 == 0:
        return num * 2
    else:
        return num

numbers = [1,2,3,4,5,6,7,8,9,10]
result = list(map(evenNum, numbers))
print(result)