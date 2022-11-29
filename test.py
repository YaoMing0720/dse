import math
def Get():
    filename = "m5out/stats.txt"
    strVal0 = "simOps"
    line0_number = 0
    with open(filename, 'r') as file:
        for line0 in file.readlines():
            line0_number += 1
            if strVal0 in line0.strip():
                obj0 = (float)(line0.split()[1])
                break
    strVal1 = "simSeconds"
    line1_number = 0
    with open(filename, 'r') as file:
        for line1 in file.readlines():
            line1_number += 1
            if strVal1 in line1.strip():
                obj1 = (float)(line1.split()[1])
                break
    return obj0 / obj1 / math.pow(10, 5)


def main():
    obj = Get()
    print("obj=", obj)

main()

a,b,c,d=200, 6, 0.7, 10
        