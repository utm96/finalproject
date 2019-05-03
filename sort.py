a = [1,2,3]
b = [1,4,6,5]
c = []
MAX_VALUE = max(max(a),max(b))
a.append(MAX_VALUE) 
b.append(MAX_VALUE)
i = 0
j = 0
while (i<len(a) and j<len(b)):
    if(a[i] <=b [j]):
        c.append(a[i])
        i +=1
    else:
        c.append(b[j])
        j +=1
    
print(c)