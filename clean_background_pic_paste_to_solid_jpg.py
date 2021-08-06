import cv2
from PIL import Image
import numpy
covered = cv2.imread(r"front_cover's_path", cv2.IMREAD_UNCHANGED)#front
background = cv2.imread(r"back_ground's_path")#back
b, g, r, a = cv2.split(covered)
foreground = cv2.merge((b, g, r))
alpha = cv2.merge((a, a, a))
ret, alpha = cv2.threshold(alpha, 254, 1, cv2.THRESH_BINARY)
foreground = cv2.multiply(alpha, foreground)
background_temp = background[0:foreground.shape[0], 0:foreground.shape[1], :]
background_temp = cv2.multiply(1-alpha, background_temp)
outImage = foreground + background_temp
image = Image.fromarray(cv2.cvtColor(outImage, cv2.COLOR_BGR2RGB))
background=Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
background.paste(image,(0,0),None)
background = cv2.cvtColor(numpy.asarray(background),cv2.COLOR_RGB2BGR)  
cv2.imshow("OpenCV",background)  
cv2.waitKey() 
