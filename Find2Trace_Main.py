import napari
import FinderWidgets.DataWidget as dw
import FinderWidgets.FinderWidget as fw

#----------------------------------------
# Napari Program with widgets to find features
# and plot the intensity time traces.
# Selected time traces can be hand picked from the plot
# to create a new layer. Time traces can be saved. 
#----------------------------------------

viewer = napari.Viewer()

widget1 = fw.FinderWidget(viewer)
widget2 = dw.Data_Widget(viewer)

viewer.window.add_dock_widget(widget1)
viewer.window.add_dock_widget(widget2)

napari.run()

print("FINISHED")