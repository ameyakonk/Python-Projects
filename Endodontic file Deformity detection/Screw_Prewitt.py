import cv2
import numpy as np
from PIL import Image

class Endofile:
    def __init__(self, img):
        self.img = img 
        self.edge_detector()
          
    def edge_detector(self):
        (h, w) = self.img.shape[:2]
        center = (w / 2, h / 2)
        angle90 = 90
        scale = 1.0
        # Perform the counter clockwise rotation holding at the center
        # 90 degrees
        M = cv2.getRotationMatrix2D(center, angle90, scale)
        self.img = cv2.warpAffine(self.img, M, (h, w))
        b,g,r=self.img[100,700]
       # print(b,g,r)
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        img_gaussian = cv2.GaussianBlur(gray,(3,3),0)
        img_median = cv2.medianBlur(gray, 5) # Add median filter to image
        kernel = np.ones((2,2),np.uint8)
        #sobel
        img_sobely = cv2.Sobel(img_gaussian,cv2.CV_8U,0,1,ksize=5)
        img_sobel_med = cv2.Sobel(img_median,cv2.CV_8U,0,1,ksize=5)
        img_sobel_med = cv2.dilate(img_sobel_med,kernel,iterations = 1)
        #self.edge_finder(img_sobel_med)
        self.edge_finder_rec(img_sobel_med)
        
    def edge_finder(self,img_sobel_med):
        count=0
        prev_x=0
        prev_y=0
        i=0
        j=0
        for j in range(1,self.img.shape[0]):
            if img_sobel_med[j-1,i] == 0:
                     count=0
            for i in range(550,750):
             if img_sobel_med[j,i] == 255:
                 count= count+1
            #print(count)     
        self.display(img_sobel_med)
        
    def edge_finder_rec(self,img_sobel_med):
        i_min_arr=[]
        j_min_arr=[]
        i_max_arr=[]
        j_max_arr=[]
 
        img_sobel_med_ec=img_sobel_med
        for j in range(1,self.img.shape[0]):
            for i in range(450,750):
             if img_sobel_med_ec[j,i] <255:
                 img_sobel_med_ec[j,i]=0
        
        count=0
        edge_count=0
        i=0
        j=0
        self.display(img_sobel_med)
        deformation=0
        def_count=0
        min_edges=32
        for j in range(1,img_sobel_med.shape[0]):
             threshold = self.map(edge_count,0,32,200,50)
             max_limit = self.map(edge_count,0,32,600,150)
             for i in range(450,750):
                 if img_sobel_med[j,i] == 255:
                     count,j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j,i,j,i,j,i)
                     j = j_max+2
                     if count > threshold:
                         edge_count = edge_count+1
                     #if edge_count < min_edges:
                      #   deformation=1
                     if count > max_limit:
                         i_min_arr.append(int(i_min))
                         j_min_arr.append(int(j_min))
                         i_max_arr.append(int(i_max))
                         def_count = def_count +1
                         deformation=1
                     break
        for i in range(def_count):
            cv2.rectangle(self.img,(i_min_arr[i],j_min_arr[i]),(i_min_arr[i]-50,j_min_arr[i]+50),(255,0,255),2)
        print("min. edges required: ",min_edges," edge_count: ",edge_count)
        cv2.namedWindow('ERROR_DISPLAY', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('ERROR_DISPLAY', 600, 600)
        cv2.imshow("ERROR_DISPLAY", self.img)
        
        if deformation == 1:
            print("LESS NO. OF EDGES DETECTED")
            print("DEFORMED FILE")
        else:
            print("NO DEFORMATION")
        
    def map(self,x, in_min, in_max, out_min, out_max):

     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    

    def edge_counter(self,img_sobel_med,j,i,j_max,i_max,j_min,i_min):
        i_new=i
        j_new=j
        count_new=1
        if i_new>0 and i_new < self.img.shape[1] and j_new>0 and j_new < self.img.shape[0]:
      
            if img_sobel_med[j_new,i_new]== 255:
                i_max = i_new if i_new > i_max else i_max
                j_max = j_new if j_new > j_max else j_max
                i_min = i_new if i_new < i_min else i_min
                j_min = j_new if j_new < j_min else j_min
                count_new = 1
                img_sobel_med[j_new,i_new]= 0
                count_new=count_new + self.edge_counter(img_sobel_med,j_new-1,i_new-1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new-1,i_new-1,j_max,i_max,j_min,i_min)[1:5]
                #print(j_max,i_max,j_min,i_min)
                count_new=count_new + self.edge_counter(img_sobel_med,j_new,i_new-1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new,i_new-1,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new+1,i_new-1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new+1,i_new-1,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new-1,i_new,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new-1,i_new,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new+1,i_new,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new+1,i_new,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new-1,i_new+1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new-1,i_new+1,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new,i_new+1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new,i_new+1,j_max,i_max,j_min,i_min)[1:5]

                count_new=count_new + self.edge_counter(img_sobel_med,j_new+1,i_new+1,j_max,i_max,j_min,i_min)[0]
                j_max,i_max,j_min,i_min=self.edge_counter(img_sobel_med,j_new+1,i_new+1,j_max,i_max,j_min,i_min)[1:5]
                
            else:
                return 0,j_max,i_max,j_min,i_min
            return count_new,j_max,i_max,j_min,i_min
        else:
            return 0,j_max,i_max,j_min,i_min

    def display(self,img_sobel_med):
        cv2.namedWindow('EDGE DETECTION', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('EDGE DETECTION', 600, 600)
        cv2.imshow("EDGE DETECTION", img_sobel_med)


img = cv2.imread('2.jpg') 
Endofile(img)
if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()    
