def frange(start, end=None, inc=None):
    "A range function with float arguments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while True:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

T = frange(0.0, 405.0, 5.5)
print repr(T)


