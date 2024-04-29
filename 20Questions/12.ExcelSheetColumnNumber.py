def ExcelolumNumber(column : str):
    result = 0
    for i in range(len(column)):
        result *= 26
        result += ord(column[i]) - ord("A") + 1
    return result

print(ExcelolumNumber("ZY"))