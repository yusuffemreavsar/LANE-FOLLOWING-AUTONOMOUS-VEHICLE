# Lane-Following-Autonomous-Vehicle

Autonomous lane following vehicle project developed with image processing methods using Python and Rasperry Pi development board.


## Project Summary
As humans are intelligent, have the ability to think and develop their thoughts, they have been making progress by always developing themselves from the past to the present day. Humans developed simple tools at the beginning. Afterwards, machines run by humans without the need of human power started to be used as a result of the improvement of electric and motor technology. Humans are doing research and making development about machines which work on their own without the necessity of human’s mind and management. As a result, the word of  “Autonomous” is in our lives now. Semi-autonomous technologies are often being used today. Actually, bringing fully autonomous vehicles into people’s lives is what is intended. Some big companies have already produced autonomous vehicles and introduced them to the market. However, we still haven’t fully managed a transition to autonomous vehicles. Autonomous vehicles have advantages and disadvantages. What kind of problems machines that are not controlled by humans might create in the future is not known precisely. Technology advances every day. These ideas that exist are developing with research. Even though we cannot fully achieve a transition to fully autonomous systems, autonomous systems which do not require human mind and control will be developed in the future. This thesis which is formed by taking into account of the autonomous systems’ importance is carried out with the purpose of evaluating the principle of the way autonomous tools work and examining the projects. History of autonomous vehicles, image processing and materiels used in this project are explained. Autonomous vehicles project which is capable of lane keeping is performed.
## Construction Stages of the Project

We first included the libraries we use in our project. Then we determined our motor and steering pins, then we set the input and output pins. We wrote in our code how many PWM signals our steering and motor pins will be. After making the necessary adjustments, our next step will be to write the functions we will use in our code with image processing methods. Our first function is the function that will allow the vehicle to recognize the edge. This function converts the video recording we receive as frames from our camera module on the Raspberry Pi into (HSV) color space. After converting the image we received into HSV color space, we determined the RGB color parameters of the red color we will use in the strip. The reason for doing this is to distinguish colors according to their brightness levels. Then, using the Canny function, we identified the edges by determining the color transitions in our image. We set our camera view to see the road and the lanes by drawing a polygon. We selected a Region of Interest (ROI) region for our camera to focus on the region of interest. This is to ensure that it focuses only on the road without detecting objects around the road. For this, we used the "bitwise_and" operator to set the regions outside our region of interest to "0" and our region of interest to "1". With this process, the lanes were clearly detected. By performing the Hough transform, it will enable the ROI image in Red-Mask. to perceive the detected points on the strip in the ROI image as a line image even if it is distorted. We then calculated the slope and intersection mean of the detected lane lines using the Hough transform. If the slope is less than zero and less than the limit we set, we defined it as the left lane; if the slope is greater than zero and greater than the limit we set, we defined it as the right lane. If the slope is zero, it will be perceived as straight. In order not to make calculations outside the area we have determined, we have determined limited coordinates (from the bottom to the center of the image) to ensure that the operation is performed within our area of interest. We displayed the determined lane lines on the screen. After determining the lane lines, we used the trigonometric function (tan^-1) to determine the direction of rotation of the motors. If our steering angle value is equal to 90 degrees, it will go straight, if the steering value is greater than 90 degrees, it will go to the right and if it is less than 90 degrees, it will go to the left. Finally, we determined a direction line to be located in the middle. We completed the code part of our project by calling each function in a while loop.
## Result
The result of the project titled 'AUTONOMOUS CAR THAT CAN FOLLOW THE LANE', which we wrote the graduation thesis, is as follows. The aim of our project was a study to ensure that an autonomous car recognizes the lane and drives consistently within the lane without human mind and intervention. Finally, it was observed that the autonomous vehicle perceived the lanes correctly with the Python codes we wrote in our project, which we completed the experiment. As a result, it was observed that it moved consistently within the lane and did not move out of the lane. 
## Technologies And Libraries
-Math

-OpenCV

-NumPy

-Time and Sys

-Rasperry Pi Libraries
## Project Images

Vehicle

![arac4](https://github.com/yusuffemreavsar/Lane-Following-Autonomous-Vehicle/assets/100023813/53a518ef-2627-4d31-a7d7-45bdd548fb3f)

HSV Filter

![arac2](https://github.com/yusuffemreavsar/Lane-Following-Autonomous-Vehicle/assets/100023813/1629e673-2392-4cbb-bf9b-7dcee14960ed)

Headline  

![arac3](https://github.com/yusuffemreavsar/Lane-Following-Autonomous-Vehicle/assets/100023813/7b2b4cb8-8c96-4bef-b5fd-3f354d730e0f)

Red Mask

![redmask](https://github.com/yusuffemreavsar/Lane-Following-Autonomous-Vehicle/assets/100023813/5b8c4dba-5f8e-4502-b22f-bc8fc97bde31)


  
