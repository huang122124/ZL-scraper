
a = [15,23,30,5,7,8,9,12,16,33,2,66]

def find_min_number(x):
    if len(x)>0:
        print('start')
        i = 0
        min = a[0]
        while i<len(x):
            if min > a[i]:
                min = a[i]
            i = i+1
        print("min is:",min)


if __name__ == '__main__':
    find_min_number(a)