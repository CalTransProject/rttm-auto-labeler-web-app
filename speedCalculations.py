import os
import math

"""
Right now plan identify different vehicles
"""

"""NOTE: Math Information"""
#Code rounds the speeds to the 4th decimal but most have 0's after the 2nd decimal so all outputs are to the 1st or 2nd decimal
#time is 0.1 seconds every 1 frame
#Code speed for every 5 seconds (50 frames)
#Conversion IF needed for seconds to hours so use: 5 seconds x (1 minute/60 seconds) x (1 hour/60 minutes)
#distance formula : sqrt( (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2 )
"""
NOTE: currently have 2 matrix arrays. 
1: is to hold distances for multiple vehicles. 
2: is for frame count and used to check if a vehicle was in a previous frame
"""
#Want to create a multi-dimensional array to hold distances for multiple vehicles

#-------------------------------- test code for speed using actual details of vehicles from auto-labeler ------------------------------------------

# VERY ROUGH ESTIMATE for center of intersection (9.00, 3.764, -3.40)
# Frames 35 to 42 were generated since vehicle detection was missing
# Frames 47 to 50 were generated since vehicle detection was missing

"""NOTE: the Y's change drastically from frame 35 and on, so vehicle speed is too high for those frames"""
"""Could source from vehicle not being detected for # of frames and manually error when updating details"""

#generated from chatgpt using a screenshot I provided of the auto-labeler and coordinates from the auto-labeler
referencePoint = [9.00, 3.764, -3.40]
counter_matrix = [[0.0] * 6 for _ in range(10)]

def initialize(folder_path):
    #folder_path = r"C:\Users\Matthew\Desktop\Runs_ Mahfuz March 28th\run_20260406_015653_7856\exports\labels_txt_reviewed"
    
    # store files in list
    files = sorted(f for f in os.listdir(folder_path) if f.endswith(".txt"))
    if(len(files) == 0):
        raise FileNotFoundError("No txt files in folder")

    # this is frame counter/index, start at -1 so in loop frame count is accurate
    frame_count = -1
    # create a matrix of 10 x 51 so if at most there are 10 vehicles a frame then we can collect the distances for all frames
    distances_matrix = [[0.0] * 51 for _ in range(10)]
    speed_matrix = [[0.0] * 51 for _ in range(10)]
    return folder_path, files, frame_count, distances_matrix, speed_matrix

def calc_dist_and_speed(folder_path, files, frame_count):
    # only look at the first 51 text files, those are the ones I manually checked and updated
    """using 5 files for unit testing"""
    distances_array = [0.0] * 51
    for filename in files[:5]:
        file_path = os.path.join(folder_path, filename)

        # read each file, reset sedan_found each time, update count (aka frame #)
        # set current distance index and speed as default "0", will be updated with calculations
        with open(file_path, "r") as file:
            sedan_found = False
            frame_count = frame_count + 1
            distances_array[frame_count] = 0
            speed = 0

            # read each line and split information into independent values
            for line in file:
                values = line.split()

                # if theres an empty line skip it
                if len(values) == 0:
                    continue

                # if theres a Sedan vehicle gather that information
                # currently only focusing on 1 sedan from the extracted information
                if values[0] == "Sedan":
                    sedan_found = True

                    try:
                        vehicle = values[0]
                        x = float(values[1])
                        y = float(values[2])
                        z = float(values[3])
                    except IndexError:
                        print("ERROR: Missing X, Y, or Z coordinate in ", filename)
                        continue
                    except ValueError:
                        print("ERROR: Invalid value in ", filename)
                        continue

                    # calculate the distance between the vehicle and reference point for current frame and
                    # store distance into distances array for speed calculation later
                    distance = math.sqrt((x - referencePoint[0])**2 + (y - referencePoint[1])**2 + (z - referencePoint[2])**2 )
                    distances_array[frame_count] = round(distance, 4)

                    #print("Current frame:", count)
                    #print("Previous frame distance:", distances_array[count-2])

                    # if vehicle was not in the previous frame or if currently frame 1 do not calculate speed of vehicle for that frame
                    if (frame_count == 1 or distances_array[frame_count-1] == 0):
                        print(vehicle, x, y, z, "\tFrame: ", frame_count, "\tDistance: ", distance, "\tDistances in array: ", distances_array[frame_count], "\tSpeed of vehicle: ", speed)
                        continue
                    # else if vehicle was in previous frame and current frame then calculate speed 
                    else: 
                        speed = abs(distances_array[frame_count] - distances_array[frame_count-1]) / (0.1)
                        speed = round(speed, 4)

                    print(vehicle, x, y, z, "\tFrame: ", frame_count, "\tDistance: ", distance, "\tDistances in array: ", distances_array[frame_count], "\tSpeed of vehicle: ", speed)

            # since im only focusing on 1 Sedan currently use this to skip other vehicle types like SUV
            if not sedan_found:
                continue

#this is a placeholder and will be replaced when my code interacts with Alfonso's code or json file containing distances
#created multiple methods to organize and clean up the multiple_vehicles method for better legibility
def calcDist (x,y,z, distances_matrix, vehicle_count, frame_count, distance):
    distance = math.sqrt((x - referencePoint[0])**2 + (y - referencePoint[1])**2 + (z - referencePoint[2])**2 )
    distances_matrix[vehicle_count][frame_count] = round(distance, 4)
    return distances_matrix, distance

def averageSpeeds(startFrame, endFrame, speed_matrix, vehicle_count,vehicle):
    i = 0 #index value
    averageOneSec = 0
    averageOneSpeed = 0
    averageFiveSec = 0
    averageFiveSpeed = 0
    for i in range(startFrame, endFrame+1):
        j = speed_matrix[vehicle_count][i]
        if j != 0:
            averageOneSpeed = averageOneSpeed + j
            averageOneSec = averageOneSec + 1
    
            averageFiveSpeed = averageFiveSpeed + j
            averageFiveSec = averageFiveSec + 1
        if averageOneSec == 10: 
            averageSpeed = averageOneSpeed/10
            print(vehicle,"'s average speed for 1 second: ", averageSpeed)
            averageOneSec = 0
            averageOneSpeed = 0
        if averageFiveSec == 50: 
            averageSpeed = averageFiveSpeed/50
            print(vehicle,"'s average speed for 5 seconds: ", averageSpeed)
            averageFiveSec = 0
            averageFiveSpeed = 0
            continue

def calcSpeed(distances_matrix, vehicle_count, frame_count, speed_matrix, speed, vehicle):
    speed = abs(distances_matrix[vehicle_count][frame_count] - distances_matrix[vehicle_count][frame_count-1]) / (0.1)
    speed_matrix[vehicle_count][frame_count] = round(speed, 4)

    global counter_matrix
    if speed_matrix[vehicle_count][frame_count] != 0:
        counter_matrix[vehicle_count][0] = counter_matrix[vehicle_count][0] + 1
        counter_matrix[vehicle_count][3] = counter_matrix[vehicle_count][3] + 1
        if counter_matrix[vehicle_count][0] == 1:
            counter_matrix[vehicle_count][1] = frame_count
        if counter_matrix[vehicle_count][3] == 1:
            counter_matrix[vehicle_count][4] = frame_count

    if counter_matrix[vehicle_count][0]%10 == 0:
        counter_matrix[vehicle_count][2] = frame_count
        startFrame = counter_matrix[vehicle_count][1]
        endFrame = counter_matrix[vehicle_count][2]
        averageSpeeds(startFrame, endFrame, speed_matrix, vehicle_count,vehicle)
        counter_matrix[vehicle_count][0] = 0
        counter_matrix[vehicle_count][1] = 0
        counter_matrix[vehicle_count][2] = 0
    if counter_matrix[vehicle_count][3]%50 == 0:
        counter_matrix[vehicle_count][5] = frame_count
        startFrame = counter_matrix[vehicle_count][4]
        endFrame = counter_matrix[vehicle_count][5]
        averageSpeeds(startFrame, endFrame, speed_matrix, vehicle_count,vehicle)
        counter_matrix[vehicle_count][3] = 0
        counter_matrix[vehicle_count][4] = 0
        counter_matrix[vehicle_count][5] = 0

    return speed_matrix, speed

def printMethod(distances_matrix, vehicle_count, frame_count, vehicle, x, y, z, speed_matrix):
    print("Vehicle #: ", vehicle_count+1, "\t", vehicle, "\t", x, "\t", y, "\t", z, "\tFrame: ", frame_count, "\tDistances in array: ", distances_matrix[vehicle_count][frame_count], "\tSpeed of vehicle in array: ", speed_matrix[vehicle_count][frame_count])
    return

def multiple_vehicles(folder_path, files, frame_count, distances_matrix, speed_matrix):
    # only look at the first 51 text files, those are the ones I manually checked and updated
    """using 10 files for unit testing"""
    """sedan should appear for frames 2 - 9 and suv should appear for frames 2,3,6 - 9"""
    """frame 6 for suv has completely different x,y, and z values compared to the rest so causes an outlier for speed at frame 7 and distance at frame 6"""
    frame_matrix = [[0.0] * 51 for _ in range(10)]
    for filename in files[:15]:
        file_path = os.path.join(folder_path, filename)

        # read each file, reset sedan_found each time, update count (aka frame #)
        # set current distance index and speed as default "0", will be updated with calculations
        with open(file_path, "r") as file:
            vehicle_found = False
            frame_count = frame_count + 1
            vehicle_count = 0
            distances_matrix[vehicle_count][frame_count] = 0
            frame_matrix[vehicle_count][frame_count] = 0
            line_count = 1

            # read each line and split information into independent values
            for line in file:
                values = line.split()
                speed = 0
                distance = 0
                # if theres an empty line skip it
                if len(values) == 0:
                    continue

                # if there's a vehicle, gather its details
                # currently only focusing on 2 vehicles
                if values[0] != "":
                    vehicle_found = True
                    # this is to separate the vehicles and their distances in the matrix
                    if line_count != 1: 
                        vehicle_count = vehicle_count + 1

                    try:
                        vehicle = values[0]
                        x = float(values[1])
                        y = float(values[2])
                        z = float(values[3])
                    except IndexError:
                        print("ERROR: Missing X, Y, or Z coordinate in ", filename)
                        continue
                    except ValueError:
                        print("ERROR: Invalid value in ", filename)
                        continue

                    # calculate the distance between the vehicle and reference point for current frame and
                    # store distance into distances array for speed calculation later
                    calcDist (x,y,z, distances_matrix, vehicle_count, frame_count, distance)

                    frame_matrix[vehicle_count][frame_count] = frame_count;

                    #print("Current frame:", count)
                    #print("Previous frame distance:", distances_array[count-2])
                    # this is checking that the vehicle was in the previous frame, if not don't calculate the speed
                    if(frame_count != 0):
                        in_previous_frame = frame_count - frame_matrix[vehicle_count][frame_count-1]
                        #print("previous frame ", in_previous_frame)
                    # if currently frame 1 do not calculate speed of vehicle for that frame or if vehicle was not in the previous frame
                    if (frame_count == 0 or in_previous_frame != 1):
                        printMethod(distances_matrix, vehicle_count, frame_count, vehicle, x, y, z, speed_matrix)
                        line_count = 2
                        continue
                    # else if vehicle was in previous frame and current frame then calculate speed 
                    else: 
                        calcSpeed(distances_matrix, vehicle_count, frame_count, speed_matrix, speed, vehicle)

                    printMethod(distances_matrix, vehicle_count, frame_count, vehicle, x, y, z, speed_matrix)
                    line_count = 2
                    
            # since im only focusing on 1 Sedan currently use this to skip other vehicle types like SUV
            if not vehicle_found:
                continue

# my real folder path C:\Users\Matthew\Desktop\Runs_ Mahfuz March 28th\run_20260406_015653_7856\exports\labels_txt_reviewed
# folder_path = input("Copy and paste your folder path containing extracted frame details: ")
folder_path = r"C:\Users\Matthew\Desktop\Runs_ Mahfuz March 28th\run_20260406_015653_7856\exports\labels"
folder_path_2 = r"C:\Users\Matthew\Desktop\Runs_ Mahfuz March 28th\run_20260406_015653_7856\exports\labels_txt_reviewed"
folder_path_3 = r"C:\Users\Matthew\Desktop\test"

#Test case 1 for method 1, folder path does not exist
try:
    folder_path, files, frame_count, distances_matrix, speed_matrix = initialize(folder_path)
    calc_dist_and_speed(folder_path, files, frame_count)
except FileNotFoundError:
    print("ERROR: File path does not exist or no txt files in folder")

#Test case 2 for method 1, correct folder path
#and Test case 2 for method 2, files contain necessary information such as x, y, and z coordinates
try:
    folder_path, files, frame_count, distances_matrix, speed_matrix = initialize(folder_path_2)
    calc_dist_and_speed(folder_path, files, frame_count)
except FileNotFoundError:
    print("ERROR: File path does not exist or no txt files in folder")

#Test case 1 for method 2, files does not contain all necessary information such as x, y, and z coordinates
try:
    folder_path, files, frame_count, distances_matrix, speed_matrix = initialize(folder_path_3)
    calc_dist_and_speed(folder_path, files, frame_count)
except FileNotFoundError:
    print("ERROR: File path does not exist or no txt files in folder")

# multiple vehicles test
try:
    folder_path, files, frame_count, distances_matrix, speed_matrix = initialize(folder_path_2)
    multiple_vehicles(folder_path, files, frame_count, distances_matrix, speed_matrix)
except FileNotFoundError:
    print("ERROR: File path does not exist or no txt files in folder")