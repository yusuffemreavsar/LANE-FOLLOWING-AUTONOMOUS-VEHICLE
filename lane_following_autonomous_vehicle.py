# Lane Tracking Autonomous Vehicle Graduation Project 2021
# Prepared by: YUSUF EMRE AVŞAR, OZKAN UZEYIROGLU
# Supervisor: Prof.Dr.HAFIZ ALISOY

# We included the libraries we used
import cv2
import math
import sys 
import numpy as np
import time 
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
# We set the motor and steering pins
rotationPin=22
speedPin = 25
in1 = 17
in2 = 27
in3 = 23
in4 = 24
# We defined whether the pins are input or output
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(rotationPin,GPIO.OUT)
GPIO.setup(speedPin,GPIO.OUT)
# We determined the PWM signals of the motor and steering pins
GPIO.output(in3,GPIO.HIGH)
GPIO.output(in4,GPIO.LOW)
speed = GPIO.PWM(speedPin,1000)
speed.stop()
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
rotation= GPIO.PWM(rotationPin,1000)
rotation.stop()
# In this section, we defined functions to perform many tasks in our code
# In the detect_edges function, HSV space filter is applied, red color detection is done, and finally edge detection is done with Canny
def detect_edges(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([160,20,70],dtype = "uint8")
    upper_red = np.array([190,255,255],dtype="uint8")
    mask = cv2.inRange(hsv,lower_red,upper_red)
    edges = cv2.Canny(mask,50,150)
    return edges
# The display_lines function performs the lane display function in each frame
def display_lines(frame, lines):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (0,255,0),6)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image
# The display_heading_line function draws the heading line, detects the direction of the steering wheel, and displays it on the frame
def display_heading_line(frame, rotation_angle):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape
    rotation_angle_radian = rotation_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(rotation_angle_radian))
    y2 = int(height / 2)
    cv2.line(heading_image, (x1, y1), (x2, y2), (0,0,255),5)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
    return heading_image
# The purpose of the region_of_interest function is to focus on the road and ignore objects outside the road 
def region_of_interest(edges):
    height, width = edges.shape
    polygons = np.array([[(0, height),(0,  height/2),(width , height/2),(width , height),]], np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygons, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    cv2.imshow("Region of Interest",masked_image)
    return cropped_edges
# The make_points function sets specific coordinates to ensure no processing is done outside the defined area, allowing processing within these boundaries
def make_points(frame, line):
    height, width, _ = frame.shape
    
    slope, intercept = line
    
    y1 = height  # bottom of the frame
    y2 = int(y1 / 2)  # make points from middle of the frame down
    
    if slope == 0:
        slope = 0.1
        
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]
# The average_slope_intercept function calculates the slope and intercept of the lines and determines whether it is a left lane or a right lane
def average_slope_intercept(frame, line_segments):
    lane_lines = []
    
    if line_segments is None:
        print("no line segments detected")
        return lane_lines

    height, width,_ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary
    
    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines
# The get_rotation_angle function is used to determine which direction the steering wheel should turn and at what speed the motor should go
def get_rotation_angle(frame, lane_lines):
    height,width,_ = frame.shape
    if len(lane_lines) == 2:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
        y_offset = int(height / 2)
    elif len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
        y_offset = int(height / 2)
    elif len(lane_lines) == 0:
        x_offset = 0
        y_offset = int(height / 2)
    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  
    steering_angle = angle_to_mid_deg + 90
    return rotation_angle
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
time.sleep(1)
# The resolution in the live stream is set
hiz = 8
lastTime = 0
lastError = 0
# Deviations and error rates on the vehicle are processed
kp = 0.4
kd = kp * 0.65
# This section is the main part of our code, where all the functions we created are executed sequentially within a while loop by opening a live stream
while True:
    ret,frame = video.read()
    frame = cv2.flip(frame,1)
    cv2.imshow("Normal Goruntu",frame)
    edges = detect_edges(frame)
    roi = region_of_interest(edges)
    line_segments = cv2.HoughLinesP(roi,1,np.pi/180,10,np.array([]),minLineLength=5,maxLineGap=150)
    lane_lines = average_slope_intercept(frame,line_segments)
    lane_lines_image = display_lines(frame,lane_lines)
    rotation_angle = get_rotation_angle(frame, lane_lines)
    heading_image = display_heading_line(lane_lines_image,rotation_angle)
    cv2.imshow("Heading line",heading_image)
    now = time.time()
    dt = now - lastTime
    deviation = rotation_angle - 90
    error = abs(deviation)    
    if deviation < 5 and deviation > -5:
        deviation = 0
        error = 0
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        rotation.stop()
    elif deviation > 5:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        rotation.start(100)
    elif deviation < -5:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        rotation.start(100)
    derivative = kd * (error - lastError) / dt
    proportional = kp * error
    PD = int(hiz + derivative + proportional)
    spd = abs(PD)
    if spd > 25:
        spd = 25
    speed.start(spd)
    lastError = error
    lastTime = time.time()        
    key = cv2.waitKey(1)
    if key == 27:
        break
#Finally, the pins and live streams we use are deactivated
video.release()
cv2.destroyAllWindows()
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
speed.stop()
rotation.stop()
