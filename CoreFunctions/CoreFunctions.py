import napari
import numpy as np

def layers_(viewer):

    layers = viewer.layers
    
    shape_layers_ = []
    img_layers_ = []
    shapes_info_ = []
    
    for layer in layers:
        
        if type(layer) == napari.layers.image.image.Image:
            
            img_layers_.append(layer)
            
        elif type(layer) == napari.layers.shapes.shapes.Shapes:
            
            if len(layer.data) > 0:
                
                first_shape = layer.data[0]
                
                dimensions = first_shape.shape
                
                if dimensions[1] == 3:
                    
                    shape_data = np.array(layer.data)
                    shape_slice = shape_data[0:, 0:, 1:].astype("int") # take out frame number from shape info
                    
                    shape_layers_.append(layer)
                    shapes_info_.append(shape_slice)
                
                elif dimensions[1] == 2: 
                    
                    layer_data = np.array(layer.data)
                    layer_data = layer_data.astype("int")
                    
                    
                    shape_layers_.append(layer)
                    shapes_info_.append(layer_data)
                
                else: 
                    message = "Weird ROI dimensions: check shapes layer!"
                    viewer.status = message
                    print(message)
                    break 
            else: 
                message = "Empty shapes layer detected!"
                viewer.status = message
                print(message)
                
    return img_layers_, shape_layers_, shapes_info_

    
def get_img(viewer): 
    
    img_layers, shape_layers, shapes_info = layers_(viewer)
                
    for item in img_layers:
        
        img = item.data
        img_name = str(item)
        
    return img, img_name