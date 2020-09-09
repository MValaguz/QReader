import cv2
import numpy as np

def main():
    # Create a black image
    img = np.zeros((512,512,3), np.uint8)        
        
    # disegna un cerchio
    #cv2.circle(img,(0,0),100,(255,0,0),-1)
    # Draw a diagonal blue line with thickness of 5 px
    #cv2.line(img,(0,0),(511,511),(255,0,0),5)    
    # disegna una scritta
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Read QRcode',(10,500), font, 2,(255,255,255),2,cv2.LINE_AA)        
            
    y = 180
    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
      
        #cv2.rectangle(img,(150,200),(250,400),(0,255,0),2)      
        cv2.line(img,(180,y-1),(320,y-1),(0,0,0),1)
        cv2.line(img,(180,y),(320,y),(0,255,0),1)
        y += 1
        
        if y > 280:
            y = 180
        
        # Displays the current frame
        cv2.imshow('Current', img)                    
    
if __name__ == "__main__":
    main()