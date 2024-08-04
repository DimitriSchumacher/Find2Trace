import DataFunctions.DataFunctions as dF
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class Data_Widget(QMainWindow):
    def __init__(self, viewer):
        super().__init__()
        
        self.setWindowTitle("Data Widget")
        
        layout = QVBoxLayout()
        label = QLabel("Data Widget")
        trace_button = QPushButton("Plot Active Layer Traces")
        save_button = QPushButton("Save Active Layer Traces")

        widgets = [label, 
                   trace_button,
                   save_button]
        
        for w in widgets:
            layout.addWidget(w)
            
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
        trace_button.clicked.connect(lambda: dF.plot_stack(viewer))
        save_button.clicked.connect(lambda: dF.save_traces_active_layer(viewer))