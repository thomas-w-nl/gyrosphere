import cv2
import numpy as np

if __name__ == "__main__":

    def print_val(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,y,frame[y][x])

    # Creating a window for later use
    cv2.namedWindow('result')
    cv2.setMouseCallback('result', print_val)

    # Starting with 100's to prevent error while masking
    # h_min, s, v = 80, 30, 30
    # h_max = 90
    # YCrCb
    y_min, Cr_min, Cb_min = 0, 0, 0
    y_max, Cr_max, Cb_max = 255, 255, 255



    def nothing(x):
        #print("y_min, y_max:", y_min, y_max)
        #print("Cr_min, Cr_max:", Cr_min, Cr_max)
        #print("Cb_min, Cb_max:", Cb_min, Cb_max)
        pass

    #
    cap = cv2.VideoCapture(-1)
    cap.set(3, 320)
    cap.set(4, 240)

    # Creating track bar
    # cv2.createTrackbar('h_min', 'result', 0, 179, nothing)
    # cv2.createTrackbar('h_max', 'result', 0, 179, nothing)
    # cv2.createTrackbar('s', 'result', 0, 255, nothing)
    # cv2.createTrackbar('v', 'result', 0, 255, nothing)
    #
    # cv2.setTrackbarPos('h_min','result',80)
    # cv2.setTrackbarPos('h_max','result',90)
    # cv2.setTrackbarPos('s','result',15)
    # cv2.setTrackbarPos('v','result',40)

    cv2.createTrackbar('y_min', 'result', 0, 255, nothing)
    cv2.createTrackbar('y_max', 'result', 0, 255, nothing)
    cv2.createTrackbar('Cr_min', 'result', 0, 255, nothing)
    cv2.createTrackbar('Cr_max', 'result', 0, 255, nothing)
    cv2.createTrackbar('Cb_min', 'result', 0, 255, nothing)
    cv2.createTrackbar('Cb_max', 'result', 0, 255, nothing)

    cv2.setTrackbarPos('Cr_max', 'result', 255)
    cv2.setTrackbarPos('Cb_max', 'result', 255)
    cv2.setTrackbarPos('y_max', 'result', 255)

    while (1):
        ret_cam, frame = cap.read()
        #frame = cv2.imread('/home/thomas/PycharmProjects/gyrosphere/data/cola.jpg')
        #frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)


        # invert
        # frame = cv2.bitwise_not(frame)


        # converting to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)  # COLOR_BGR2HSV

        # get info from track bar and appy to result
        # h_min = cv2.getTrackbarPos('h_min', 'result')
        # h_max = cv2.getTrackbarPos('h_max', 'result')
        # s = cv2.getTrackbarPos('s', 'result')
        # v = cv2.getTrackbarPos('v', 'result')

        Cr_min = cv2.getTrackbarPos('Cr_min', 'result')
        Cr_max = cv2.getTrackbarPos('Cr_max', 'result')

        Cb_min = cv2.getTrackbarPos('Cb_min', 'result')
        Cb_max = cv2.getTrackbarPos('Cb_max', 'result')

        y_min = cv2.getTrackbarPos('y_min', 'result')
        y_max = cv2.getTrackbarPos('y_max', 'result')

        # if h_min >= h_max:
        #     h_min = h_max - 1

        if Cb_min >= Cb_max:
            Cb_min = Cb_max - 1
        if Cr_min >= Cr_max:
            Cr_min = Cr_max - 1

        # Normal masking algorithm
        # lower_blue = np.array([h_min, s, v])
        # upper_blue = np.array([h_max, 255, 255])
        #
        lower_blue = np.array([y_min, Cr_min, Cb_min])
        upper_blue = np.array([y_max, Cr_max, Cb_max])


        mask = cv2.inRange(hsv, lower_blue, upper_blue)


        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('result', result)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
