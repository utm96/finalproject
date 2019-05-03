
def isSignal(i,j,visited,radar):
    return (i >=0 and j >=0 and i<len(radar) and j< len(radar[0]) and not visited[i][j] and radar[i][j])

def checkNeighbor(i,j,visited,radar,counter):
    visited[i][j] = True
    radar[i][j] = counter
    # 8 hang xom cho moi o
    rowNeighbor = [-1, -1, -1,  0, 0,  1, 1, 1]
    colNeighbor = [-1,  0,  1, -1, 1, -1, 0, 1]
    for k in range(8):
        if isSignal(i+rowNeighbor[k],j+colNeighbor[k],visited,radar):
            checkNeighbor(i+rowNeighbor[k],j+colNeighbor[k],visited,radar,counter)

with open('tank.txt') as f:
    w, h = [int(x) for x in next(f).split()]
    radar = []
    for line in f: 
        radar.append([int(x) for x in line.split()])
visited  = [[False for i in range(h)] for i in range(w)]

counter = 0
for m in range(w):
    for n in range(h):
        if visited[m][n] == False and radar[m][n] ==1: 
            counter += 1
            checkNeighbor(m,n,visited,radar,counter)

with open('result.txt','w') as f:
    f.write(str(counter))
    for row in radar:
        f.write("\n" + " ".join(str(v) for v in row))