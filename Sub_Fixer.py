import cv2
import time
import numpy as np

def hc_fix(**kwargs):

    '''Blends hardcoded subs by applying an user-defined aperture around the
       text and identifying pixel of RGB defined range. A mask is created,
       Gaussian blurred(very tricky param) and an average RGB color from the
       appeture is applied to the masked area

       **kwargs include:
         in_name: provide input name with extension mkv/mp4/avi (if file is not in the,
                working directory provide root to file
         out_name: provide output name with extension mp4 (fourcc set to mp4)
         width: provide output width size
         height: provide output height size
         fps: declare the framerate
         l_bound: provide RGB list of lower bound to mask eg: [252, 245, 252]
         h_bound: provide RGB list of higher bound to mask eg: [255, 255, 255]
         xrange: provide list of xrange for apperture eg: [300, 800]
         yrange: provide list of yrange for apperture eg: [400, 900]
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
    #fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4') #for avi
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    width = 1920
    height = 1080
    fps = 24
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
            width = np.int(component)
        elif key == 'height':
            height = np.int(component)
        elif key == 'fps':
            fps = np.float(component)
        elif key == 'l_bound':
            lower_bound = np.array(component) #must be a list
        elif key == 'h_bound':
            higher_bound = np.array(component) #must be a list
        elif key == 'xrange':
            xranges = component #must be a list
        elif key == 'yrange':
            yranges = component #must be a list
        elif key == 'startframe':
            start_frame = component
        elif key == 'conv_rate': #time between frame conversion 
            conv_rate = float(component)
            
    vs = cv2.VideoCapture(input_name)

    if not width:
        width  = int(vs.get(3))
    if not height:
        height = int(vs.get(4))
    if not fps:
        fps = vs.get(5)

    print('Width is: ', width, '\nHeight is: ', height, '\nFPS is: ', fps)

    out = cv2.VideoWriter(output_name, fourcc, fps, (width,height))
    i = 0

    while True:

        ret, image = vs.read()

        if ret:
        
            img = image[yranges[0]:yranges[1],xranges[0]:xranges[1]]


            if i>=start_frame:

                avg_color_per_row = np.average(img, axis=0)
                avg_color = np.average(avg_color_per_row, axis=0)

                mask = cv2.inRange(img, lower_bound, upper_bound)
                mask1 = cv2.GaussianBlur(mask, (19,19),5)
                img[mask1>0]=avg_color
                img_blur = cv2.GaussianBlur(img, (25,25),55)

                img[mask1>0]=img_blur[mask1>0]

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
'''hc_fix(in_name='input.mkv', out_name='output.mp4', fps=23.976, \
       l_bound=[100,100,100], h_bound=[110,110,110], \
       xrange=[600,800], yrange=[300,500])'''
