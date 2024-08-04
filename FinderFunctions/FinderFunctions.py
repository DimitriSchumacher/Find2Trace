import CoreFunctions.CoreFunctions as cf
import numpy as np
import cv2 as cv

def project(image): 
    # Does sum projection over stack
    projection = np.zeros(image[0].shape)
    
    # Sum all slices
    for i in image:
        projection += i
    
    # Normalize to max
    projection_max = np.max(projection)
    projection = (projection / projection_max)*255
    
    return projection

def threshold(image, img_name, viewer, show_thresh, show_projection, use_projection, sigma):
    
    img = image[0]
    
    img_projection = project(image)
    
    if use_projection == True:
        
        mean_value = np.mean(img_projection)
        std_dev = np.std(img_projection)
        threshold_value = mean_value+std_dev*sigma
        
        blur = cv.GaussianBlur(img_projection,(3,3),3)
        
    elif use_projection == False:
        
        mean_value = np.mean(img)
        std_dev = np.std(img)
        threshold_value = mean_value+std_dev*sigma
        
        blur = cv.GaussianBlur(img,(3,3),3)

    ret_, th_ = cv.threshold(blur, threshold_value, 255, cv.THRESH_BINARY)
    th_ = th_.astype('uint8')
    
    if show_thresh == True: 
        viewer.add_image(th_, name="Threshold")
    
    if show_projection == True: 
        viewer.add_image(img_projection, name="Projection")

    message = str(img_name) + " thresholded successfully: Sigma = " + str(sigma)
    viewer.status = message
    print(message)
    
    return th_

def detect(image, viewer, show_detected):
    
    detection = cv.connectedComponentsWithStats(image) 
    
    if show_detected == True:
        
        viewer.add_image(detection[1], name="Detected Particles")
    
    message = "Particles detected successfully"
    viewer.status = message
    print(message)
    
    return detection

def sort_and_select(viewer, image, stats, area_min, area_max, roi_size):
    # roi_size --> roi is a square of roi_size x roi_size

    amt = stats[0]
    area = stats[2][:,4]
    centroid = stats[3]
        
    image_width, image_height = image[0].shape
    
    roi_layer = viewer.add_shapes(name="Selected Features")
    
    # Iterate over detected features 
    for i in range(amt):
        # Check that amt is not empty
        if i > 0:
            
            # Check for area criterium
            if area[i] >= area_min and area[i] <= area_max:
                centroid_x = int(centroid[i][0])
                centroid_y = int(centroid[i][1])
                
                # Check if roi would be outside of image bounds 
                if centroid_y+roi_size < image_height and centroid_y-roi_size > 0 and  centroid_x-roi_size > 0 and centroid_x+roi_size < image_width:
                    
                    top_left = [centroid_y+roi_size, centroid_x-roi_size]
                    bottom_right = [centroid_y-roi_size, centroid_x+roi_size]
                    coordinates = [top_left, bottom_right]
                    
                    roi_layer.add_rectangles(coordinates, face_color="#ffffff00", edge_width=3, edge_color="yellow")

 
def find(viewer, area_min, area_max, roi_size, show_thresh, show_projection, show_detected, use_projection, sigma):
    
    img, image_name = cf.get_img(viewer)
    
    thresh = threshold(image=img, img_name=image_name, viewer=viewer, show_thresh=show_thresh, show_projection=show_projection, use_projection=use_projection, sigma=sigma)    

    detection = detect(image=thresh, viewer=viewer, show_detected=show_detected)

    sort_and_select(viewer, image=img, stats=detection, area_min=area_min, area_max=area_max, roi_size=roi_size)