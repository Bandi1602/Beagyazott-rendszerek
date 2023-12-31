from sense_hat import SenseHat
import matplotlib.pyplot as plt
import math
import time

calibration = True
sense = SenseHat()

def stop():
    global calibration
    calibration = False

def plot(filename):
    x_list = []
    y_list = []

    try:
        file = open(filename, "r")
        lines = file.readlines()

        for line in lines:
            values = line.split(",")
            x_list.append(float(values[0]))
            y_list.append(float(values[1]))
    
    finally:
        file.close()

    xmax = max(x_list)
    xmin = min(x_list)
    ymax = max(y_list)
    ymin = min(y_list)
    print("Max x: ", xmax, "Min x: ", xmin)
    print("Max y: ", ymax, "Min y: ", ymin)

    line1, = plt.plot(range(1, len(x_list) + 1), x_list, "r-", label="x")
    line2, = plt.plot(range(1, len(y_list) + 1), y_list, "b--", label="y")
    plt.xlabel("Measurements")
    plt.ylabel("Value")
    plt.legend(handles=[line1, line2])
    plt.show()
    return xmax, xmin, ymax, ymin

def main():
    
    filename = "compass.txt"
    file = open(filename, "w")

    sense.stick.direction_middle = stop
    print("Start data acquisition")

    # calibration process
    while calibration:
        magnet = sense.get_compass_raw()
        x = magnet["x"]
        y = magnet["y"]
        file.write(str(x) + "," + str(y) + "\n")
    
    file.close()
    xmax, xmin, ymax, ymin = plot(filename)

    while True:
        magnet = sense.get_compass_raw()
        x = magnet["x"]
        y = magnet["y"]

        # range transform
        xz = -1 + ((1-(-1)) / (xmax - xmin)) * (x - xmin)
        yz = -1 + ((1-(-1)) / (ymax - ymin)) * (y - ymin)
        # degree (a) calculation
        if xz == 0 and yz < 0:
            deg = 90
        elif xz == 0 and yz > 0:
            deg = 270
        elif yz < 0:
            deg = 360 + math.atan2(yz, xz) * (180 / 3.14159)
        else:
            deg = math.atan2(yz, xz) * (180 / 3.14159)

        # cardinal points
        if deg < 45 or deg > 315:
            sense.show_letter("N")
        elif deg < 135:
            sense.show_letter("E")
        elif deg < 225:
            sense.show_letter("S")
        else:
            sense.show_letter("W")
        
        time.sleep(0.2)
        sense.clear()

# esetleg innen kivenni a köv sort és csak simán main ????
if __name__ == "__main__":
    main()