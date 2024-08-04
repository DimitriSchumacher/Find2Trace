import CoreFunctions.CoreFunctions as cf
import numpy as np
import pyqtgraph as pg
import csv
from matplotlib import colors
from tkinter import Tk
from tkinter import filedialog

curves = []

def get_traces(viewer):
    
    img_layers, shape_layers, shapes_info = cf.layers_(viewer)
    
    mean_roi = []
    
    shape_layer = viewer.layers.selection.active.data

    for shape in shape_layer:
        
        dimensions = shape.shape
        
        if dimensions[1] == 3:
            
            top_left = shape[0][1:].astype("int")
            bottom_right = shape[2][1:].astype("int")    
        
        elif dimensions[1] == 2:
                
            top_left = shape[0].astype("int")
            bottom_right = shape[2].astype("int")
        
        else: 
            message = "Weird ROI dimensions: check shapes layer!"
            viewer.status = message
            print(message)
            break 
        
        for img in img_layers:
            
            if len(img.data.shape) > 2:
            
                mean_roi_i = []
                
                img_data = img.data
                
                cropped = img_data[:, top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
                
                for frame in cropped:
                    
                    mean_roi_i_frame = np.mean(frame)
                    mean_roi_i.append(mean_roi_i_frame)
                    
            else: 
                
                message = "Image must be a stack, unable to compute from image: " + str(img)
                viewer.status = message
                print(message)

            if len(mean_roi_i) > 0:
                mean_roi.append(mean_roi_i)
    
    return np.array(mean_roi)

def plotClicked(curve, viewer):
            
    global curves
        
    img_layers, shape_layers, shapes_info = cf.layers_(viewer)
    
    print(curve)

    layer_exists = False
        
    for layer in shape_layers:
        
        if "Hand-picked" in str(layer.name):
                
            layer_exists = True
            break 
                
    if layer_exists:
        picked_layer = viewer.layers["Hand-picked"]
    else: 
        picked_layer = viewer.add_shapes(name="Hand-picked")
        picked_layer = viewer.layers["Hand-picked"]
        
    for i,c in enumerate(curves):
        if c is curve:
            c.setPen("y", width=3)

            picked_layer.add_rectangles(shapes_info[0][i], face_color="#ffffff00", edge_width=3, edge_color="magenta")
        else:
            c.setPen("b", width=1)
        
def plot_stack(viewer):
        
    global curves
    
    curves = [] # empties curves variable in case it was already used before
    
    traces = get_traces(viewer)
    
    baseline = 0
    gradient = np.linspace(0, 1, len(traces))
    count = -1
    
    plt = pg.plot()
    plt.setLabel(axis='left', text='Intensity [a.u.]')
    plt.setLabel(axis='bottom', text='Frames')
    
    for trace in traces: 
        
        count += 1
        
        trace_max = np.max(trace)
        norm_trace = trace/trace_max
        max_to_base = np.abs(np.mean(norm_trace)-1)
        baseline += max_to_base + 0.05
        norm_trace = baseline + norm_trace
        
        color_rgba = [1, gradient[count], 0, 1]
        
        color_hex = colors.to_hex(color_rgba, keep_alpha=True)
        
        curves.append(pg.PlotCurveItem(norm_trace, pen=color_hex, clickable=True))
        
        plt.addItem(curves[count])
        curves[count].sigClicked.connect(lambda curve: plotClicked(curve, viewer=viewer))        
            
    message = "Stacked traces plot!"    
    viewer.status = message
    print(message) 

def save_traces_active_layer(viewer):  
            
    img_layers, shape_layers, shapes_info = cf.layers_(viewer)

    for item in img_layers:
        
        img = item.data
        img_name = str(item)
        
    root = Tk()
    root.withdraw()

    path = filedialog.askdirectory()
    
    traces = get_traces(viewer)
    
    csv_name = "/"+ img_name + ".csv"
    
    header = [i for i in range (len(traces[0]))]
    
    with open(path + csv_name, 'w', newline='\n') as file:
        
        writer = csv.writer(file)
        
        writer.writerow(header)
        writer.writerows(traces)      
            