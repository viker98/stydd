def checkStraightLine(coordinates):
    point1 = coordinates[0]
    point2 = coordinates[1]     
    deltaX = point2[0] - point1[0]
    deltaY = point2[1] - point1[1]       
    for i in range(2, len(coordinates)):
        currentPoint = coordinates[i]      
        currentDeltaX = currentPoint[0] - point1[0]
        currentDeltaY = currentPoint[1] - point1[1]      
        if deltaX * currentDeltaY != deltaY * currentDeltaX:
            return False
        
    return True
    

print(checkStraightLine([[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]))