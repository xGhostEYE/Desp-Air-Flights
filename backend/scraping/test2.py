from curses.ascii import isalpha

from bleach import clean


data = [['WS738'],
        ['WS', '1534DL', '7028'],
        ['5T1720'],
        ['WS461'],
        ['WS3192'],
        ['AC', '322LH', '6671OS', '8372SN', '9558'],
        ['AC', '213NZ', '4817']]
cleanedflights = []

for i in range(len(data)):
    print("data line: ", data[i])
    if len(data[i]) > 1:
        cleanedflights.append(str(data[i][0])+str(data[i][1]))
    else:
        cleanedflights.append(str(data[i][0]))
for i in range(len(cleanedflights)):
    if str(data[i][-1]).isalpha() and str(data[i][-2]).isalpha():
        cleanedflights[i] = cleanedflights[i][:len(cleanedflights[i]) - 2]
print(cleanedflights)
    # if len(data[i]) == 1:
    #     cleanedflights.append(str(data[i][0]))
    
    # print("data line: ", data[i])

    # if len(data[i]) >= 2:
    #     for j in range(len(data[i])):
    #         if str(data[i][1][j]).isalpha():
    #             str(data[i][1]).split(data[i][1][j], 1)[0]
    #         cleanedflights.append(str.join(str(data[i][0]) + str(data[i][1])))
