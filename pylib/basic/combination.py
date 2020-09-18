

def get_C(n, m):
    l = [0] * n

    while(True):
        for i in range(n):
            if l[i] == 0:
                l[i] = 1
                break
            else:
                l[i] = 0
        if sum(l) == m:
            yield l
    
        if sum(l) == n:
            return





if __name__ == "__main__":
    for c in get_C(5,3):
        print(c)