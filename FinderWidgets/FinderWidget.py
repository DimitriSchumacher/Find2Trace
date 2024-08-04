import PyQt5.QtCore as Qt
import FinderFunctions.FinderFunctions as ff
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QSlider, QVBoxLayout, QWidget, QLabel

class FinderWidget(QMainWindow):
    def __init__(self, viewer):
        super().__init__()
        
        self.setWindowTitle("Finder Widget")
        
        layout = QVBoxLayout()
        label = QLabel("Finder Widget")
        check_show_thresh = QCheckBox("Show Threshold")
        check_show_projection = QCheckBox("Show Projection")
        check_use_projection= QCheckBox("Use Projection")
        check_show_detect = QCheckBox("Show Detected")
        threshold_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        area_min_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        area_max_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        roi_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        button1 = QPushButton("Find Features")
        
        threshold_slider.setMinimum(0)
        threshold_slider.setMaximum(5)
        threshold_slider.setValue(2)
        thresh_slider_value = threshold_slider.value()
        label_thresh_slider = QLabel("Sigma = " + str(thresh_slider_value))
        
        area_min_slider.setMinimum(0)
        area_min_slider.setMaximum(100)
        area_min_slider.setValue(20)
        area_min_slider_value = area_min_slider.value()
        label_area_min_slider = QLabel("Minimum Area = " + str(area_min_slider_value))
        
        area_max_slider.setMinimum(0)
        area_max_slider.setMaximum(5000)
        area_max_slider.setValue(2000)
        area_max_slider_value = area_max_slider.value()
        label_area_max_slider = QLabel("Maximum Area = " + str(area_max_slider_value))
        
        roi_slider.setMinimum(0)
        roi_slider.setMaximum(100)
        roi_slider.setValue(20)
        roi_slider_value = roi_slider.value()
        label_roi_slider = QLabel("Roi Width = " + str(roi_slider_value))
        
        widgets = [label, 
                   check_show_thresh, 
                   check_show_detect, 
                   check_use_projection,
                   check_show_projection,
                   label_thresh_slider, 
                   threshold_slider, 
                   label_area_min_slider,
                   area_min_slider,
                   label_area_max_slider,
                   area_max_slider,
                   label_roi_slider,
                   roi_slider,
                   button1]
        
        for w in widgets:
            layout.addWidget(w)
            
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        def updateLabel():
            
            thresh_slider_value = threshold_slider.value()
            area_min_slider_value = area_min_slider.value()
            area_max_slider_value = area_max_slider.value()
            roi_slider_value = roi_slider.value()
            
            label_thresh_slider.setText("Sigma = " + str(thresh_slider_value))
            label_area_min_slider.setText("Minimum Area = " + str(area_min_slider_value))
            label_area_max_slider.setText("Maximum Area = " + str(area_max_slider_value)) 
            label_roi_slider.setText("Roi Width = " + str(roi_slider_value))
    
        threshold_slider.valueChanged.connect(updateLabel)
        area_min_slider.valueChanged.connect(updateLabel)
        area_max_slider.valueChanged.connect(updateLabel)
        roi_slider.valueChanged.connect(updateLabel)
        
        button1.clicked.connect(lambda: ff.find(viewer,
                                                    area_min=area_min_slider.value(),
                                                    area_max=area_max_slider.value(),
                                                    roi_size=roi_slider.value(),
                                                    show_thresh=check_show_thresh.isChecked(),
                                                    show_projection=check_show_projection.isChecked(),
                                                    show_detected=check_show_detect.isChecked(),
                                                    use_projection=check_use_projection.isChecked(),
                                                    sigma=threshold_slider.value()))