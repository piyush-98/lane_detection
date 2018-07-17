import cv2
import numpy as np
cap = cv2.VideoCapture('/home/piyush/Desktop/lane.mp4')
def region_of_interest(img, vertices):
   
    mask = np.zeros_like(img)   
    match_mask_color = 255
      
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
      if lines is None:
          return
      img = np.copy(img)
      line_image = np.zeros(
         (
             img.shape[0],
             img.shape[1],
             3
         ),
      dtype=np.uint8,
      )
         
      for line in lines:
          for x1, y1, x2, y2 in line:
             cv2.line(line_image, (x1, y1), (x2, y2), color, thickness)

    
      img = cv2.addWeighted(img, 0.8, line_image, 1.0, 0.0)

   
      return img



frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
region_of_interest_vertices = [
    	(0,frame_height ),
    	(0,45),
        (frame_width,45),
    	(frame_width,frame_height),
]


if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 



 

out = cv2.VideoWriter('/home/piyush/Desktop/outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
 
while(True):
  ret, image = cap.read()
 
  if ret == True: 
     
    # Write the frame into the file 'output.avi'
    out.write(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Display the resulting frame
    cannyed_image = cv2.Canny(gray_image, 200, 300)

    cropped_image = region_of_interest(
    	   cannyed_image,
           np.array(
               [region_of_interest_vertices],
               np.int32
    	   ),
    )
    lines = cv2.HoughLinesP(
    		cropped_image,
    		rho=6,
    		theta=np.pi /180,
    		threshold=160,
    		lines=np.array([]),
    		minLineLength=25,
   		 maxLineGap=30)

    
    line_image = draw_lines(image, lines)
	    
    cv2.imshow('line_image',line_image)
    
 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows()
