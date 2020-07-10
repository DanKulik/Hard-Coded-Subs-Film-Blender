import cv2
import time
import numpy as np

def hc_fix(**kwargs):

    '''Blends hardcoded subs by applying an user-defined aperture around the
       text and identifying pixels of RGB defined range (double pass to refine
       text region only). A mask is created, Gaussian blurred, and applied
       to the Navier-Stokes inpainting function to approximate colors for
       the masked region. This is then written out to an image/video file.

       **kwargs include:
         in_name: provide input name with extension mkv/mp4/avi (if file is not in the,
                  working directory provide root to file
         out_name: provide output name with extension mp4 (fourcc set to mp4)
         width: provide output width size
         height: provide output height size
         fps: declare the framerate
         lower_bound: provide RGB list of lower bound to mask eg: [252, 245, 252]
                      or [252, 245, 252, 0, 0, 0] for a double pass filter
         upper_bound: provide RGB list of higher bound to mask eg: [255, 255, 255]
                      or [255, 255, 255, 25, 35, 25] for a double pass filter
         xrange: provide list of xrange for apperture eg: [300, 800]
         yrange: provide list of yrange for apperture eg: [400, 900]
         window: pixel distance used in the Navier-Stokes inpainting function
         start_frame: provide frame number to start blend process
         conv_rate: time between frame conversions (This is to reduce cpu
                    load, default uses approx less than one core)

    '''

    #list of defaults
    lower_bound = np.array([252, 245, 252])
    upper_bound= np.array([255, 255, 255])
    width = False
    height = False
    fps = False
    #fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4') #for avi output
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    xranges = [1,2]
    yranges = [1,2]
    start_frame = 0
    conv_rate = 0.03

    for key, component in kwargs.items():
        if key == 'in_name':
            input_name = str(component) #must be a string
        elif key == 'out_name':
            output_name = str(component) #must be a string
        elif key == 'width':
            width = int(component)
        elif key == 'height':
            height = int(component)
        elif key == 'fps':
            fps = float(component)
        elif key == 'l_bound':
            lower_bound = np.array(component) #must be a list of 3 or 6 vals
        elif key == 'h_bound':
            upper_bound = np.array(component) #must be a list of 3 or 6 vals
        elif key == 'xrange':
            xranges = component #must be a list
        elif key == 'yrange':
            yranges = component #must be a list
        elif key == 'window':
            window = int(component)
        elif key == 'startframe':
            start_frame = int(component)
        elif key == 'conv_rate': #time between frame conversion 
            conv_rate = float(component)
            
    vs = cv2.VideoCapture(input_name)

    if not width:
        width  = int(vs.get(3))
    if not height:
        height = int(vs.get(4))
    if not fps:
        fps = float(vs.get(5))

    print('Width is: ', width, '\nHeight is: ', height, '\nFPS is: ', fps)

    out = cv2.VideoWriter(output_name, fourcc, fps, (width,height))
    i = 0

    while True:

        ret, image = vs.read()

        if ret:
        
            img = image[yranges[0]:yranges[1],xranges[0]:xranges[1]]


            if i>=start_frame:

                mask1 = cv2.inRange(img, lower_bound[:3], upper_bound[:3])
                mask1 = cv2.GaussianBlur(mask1, (15,15),3)

                if len(lower_bound)>3:
                    mask2 = cv2.inRange(img, lower_bound[3:], upper_bound[3:])
                    mask2 = cv2.GaussianBlur(mask2, (15,15),3)

                    mask = mask1 * mask2
                    mask = cv2.GaussianBlur(mask, (3,3),3)
                else:
                    mask = mask1
                
                img = cv2.inpaint(img,mask,window,cv2.INPAINT_NS)


            image[yranges[0]:yranges[1],xranges[0]:xranges[1]] = img
            #Use this to write out test images to find where the text is located
            #cv2.imwrite('image' + str(i-start_frame) + '.jpg', image) 
            i += 1
            out.write(image)
    
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        else:
            break
        
        time.sleep(conv_rate)

    vs.release()
    out.release()
    cv2.destroyAllWindows()

#example
'''hc_fix(in_name='test5.mp4', out_name='output2.mp4', fps=23.976, \
       l_bound=[0,0,0,252,245,252], h_bound=[25,35,25,255,255,255], \
       xrange=[100,650], yrange=[200,500], window=2)'''
