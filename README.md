# Find2Trace Readme

Napari program to automatically detect spacially static features in a stack. The program can plot the time-traces of the detected features. The traces can be clicked individually to be hand-picked and selected, which will create a new layer of hand-picked features. The traces of the hand-picked features can be visualized again separately. The active layer traces can be saved as a .csv file. 

The automatic detection of features can be fine-tuned by filtering features by minimum and maximum size. For optimized detection of dim features across a stack, a sum projection of the stack can be used to detect the features. For debugging purposes, the threshold, detected features and the projection can be shown. It is important to remove all images besides the stack before plotting the traces.

Automatic feature detection occurs with a simple intensity threshold, which can be fine tuned with the sigma parameter. The ROI-width parameter determines the size of the region of interest surrounding the detected features. 

An example stack can be found in the /TestData directory. 

!Warning! --> when using small screens, the widgets of the Napari program might overlap, covering up some of the sliders/buttons. To fix this, just release and dock one of the widgets again. 

## Required Python packages: 
napari
numpy
opencv-python (cv2)
csv
matplotlib
tkinter
pyqtgraph
PyQt5
