import random
from copy import deepcopy

def main():
    location=[i for i in range(16)]
    print("1 location is{}".format(location))
    count = 1
    PE_location = [deepcopy(location[0:12])]
    LLC1_location = [location[12]]
    LLC2_location = [location[13]]
    DDRC1_location = [location[14]]
    DDRC2_location = [location[15]]

    # begin change
    change1 = 12
    change2 = 13
    location_new = deepcopy(location)
    if(change1 != change2):
        location_new[change1], location_new[change2] = location_new[change2], location_new[change1]
        location_new = [12,8,4,0,13,9,5,1,14,10,6,2,15,11,7,3]
        symmetry_new = symmetry(location_new, PE_location, LLC1_location, LLC2_location, DDRC1_location, DDRC2_location, count)
        print("symmetry_new = {}".format(symmetry_new))
        if(not symmetry_new):
            print("location is{}.".format(location_new))
            location = deepcopy(location_new)
            PE_location.append(location_new[0:12])
            LLC1_location.append(location_new[12])
            LLC2_location.append(location_new[13])
            DDRC1_location.append(location_new[14])
            DDRC2_location.append(location_new[15])
            count = count + 1
    else:
        location_new[change1], location_new[15-change1] = location_new[15-change1], location_new[change1]
        symmetry_new = symmetry(location_new, PE_location, LLC1_location, LLC2_location, DDRC1_location, DDRC2_location, count)
        print("symmetry_new = {}".format(symmetry_new))
        if(not symmetry_new):
            print("location is{}.".format(location_new))
            location = deepcopy(location_new)
            PE_location.append(location_new[0:12])
            LLC1_location.append(location_new[12])
            LLC2_location.append(location_new[13])
            DDRC1_location.append(location_new[14])
            DDRC2_location.append(location_new[15])
            count = count + 1


def rotation(mapping):
    # 定义一个旋转90度的函数
    location = deepcopy(mapping)
    for i in range(16):
        if(location[i]==0):
            location[i] = 12
        elif(location[i]==1):
            location[i] = 8
        elif(location[i]==2):
            location[i] = 4
        elif(location[i]==3):
            location[i] = 0
        elif(location[i]==4):
            location[i] = 13
        elif(location[i]==5):
            location[i] = 9
        elif(location[i]==6):
            location[i] = 5
        elif(location[i]==7):
            location[i] = 1
        elif(location[i]==8):
            location[i] = 14
        elif(location[i]==9):
            location[i] = 10
        elif(location[i]==10):
            location[i] = 6
        elif(location[i]==11):
            location[i] = 2
        elif(location[i]==12):
            location[i] = 15
        elif(location[i]==13):
            location[i] = 11
        elif(location[i]==14):
            location[i] = 7
        elif(location[i]==15):
            location[i] = 3
        else:
            print("Rotation Error!")

    return deepcopy(location)


def reflection(mapping):
    # 定义一个沿竖直方向对称的函数
    location = deepcopy(mapping)
    for i in range(16):
        if(location[i]==0):
            location[i] = 12
        elif(location[i]==1):
            location[i] = 13
        elif(location[i]==2):
            location[i] = 14
        elif(location[i]==3):
            location[i] = 15
        elif(location[i]==4):
            location[i] = 8
        elif(location[i]==5):
            location[i] = 9
        elif(location[i]==6):
            location[i] = 10
        elif(location[i]==7):
            location[i] = 11
        elif(location[i]==8):
            location[i] = 4
        elif(location[i]==9):
            location[i] = 5
        elif(location[i]==10):
            location[i] = 6
        elif(location[i]==11):
            location[i] = 7
        elif(location[i]==12):
            location[i] = 0
        elif(location[i]==13):
            location[i] = 1
        elif(location[i]==14):
            location[i] = 2
        elif(location[i]==15):
            location[i] = 3
        else:
            print("Reflection Error!")

    return deepcopy(location)


def symmetry(mapping, PE_location, LLC1_location, LLC2_location, DDRC1_location, DDRC2_location, count):
    # 判断是否对称配置
    transformation = []
    identical = deepcopy(mapping)
    transformation.append(identical)
    rotation_90 = rotation(deepcopy(mapping))
    transformation.append(rotation_90)
    rotation_180 = rotation(deepcopy(rotation_90))
    transformation.append(rotation_180)
    rotation_270 = rotation(deepcopy(rotation_180))
    transformation.append(rotation_270)
    reflection_y = reflection(deepcopy(mapping))
    transformation.append(reflection_y)
    reflection_y_90 = rotation(deepcopy(reflection_y))
    transformation.append(reflection_y_90)
    reflection_y_180 = rotation(deepcopy(reflection_y_90))
    transformation.append(reflection_y_180)
    reflection_y_270 = rotation(deepcopy(reflection_y_180))
    transformation.append(reflection_y_270)
    for x in transformation:
        for i in range(count):
            if(x[0:12] == PE_location[i]):
                if((x[12] == LLC1_location[i]) and (x[13] == LLC2_location[i])):
                    if((x[14] == DDRC1_location[i]) and (x[15] == DDRC2_location[i])):
                        print("This configuration has been simulated at {} times!".format(i))
                        print("The duplicate configuration is{}.".format(x))
                        return True
                    elif((x[14] == DDRC2_location[i]) and (x[15] == DDRC1_location[i])):
                        print("This configuration has been simulated at {} times!".format(i))
                        print("The duplicate configuration is{}.".format(x))
                        return True
                    else:
                        continue

                elif((x[12] == LLC2_location[i]) and (x[13] == LLC1_location[i])):
                    if((x[14] == DDRC1_location[i]) and (x[15] == DDRC2_location[i])):
                        print("This configuration has been simulated at {} times!".format(i))
                        print("The duplicate configuration is{}.".format(x))
                        return True
                    elif((x[14] == DDRC2_location[i]) and (x[15] == DDRC1_location[i])):
                        print("This configuration has been simulated at {} times!".format(i))
                        print("The duplicate configuration is{}.".format(x))
                        return True
                    else:
                        continue
                else:
                    continue
            else:
                continue
    
    return False





if __name__ == "__main__":
    main()
