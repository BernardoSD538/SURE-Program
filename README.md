# Development of a Machine Learning–Based Laser Pointing Stabilization System for ZEUS

## Creation of LabVIEW porgrams capable of using already trained AI model to predict X and Y coordinates, as well as LabVIEW program for training model via Python. 

This project has the objetive of implementing the use of an AI model to predcit values and be able to use them within LabVIEW. To achieve this purpuse two LabVIEW VIs were made as options: The Python Node method, and Ivans method. Both are able to use an ONNX file of an already created model to predict X and Y values and show them in LabVIEW. A third LabVIEW VI was made with the purpuse of also being able to train AI model within LabVIEW and view performance results of the same. In the following text, a brief explanation of each VI will be given for general understanding of how each one works, but a more detailed Guide on how to make them is available for each VI inside their folder. 

- Python Node method 

This method uses LabVIEW's built in blocks to use python code. This are the Open Python Session, Python Node, and Close Python Session blocks. The logic in LabVIEW is simple, you just need to open a python session, call the python code and its desired function via the Python Node, store the return values given by the python code somewhere, and finally close the python session. The image below shows the general working of this method. For this example, an ONNX file model was used. As you can see on the Python Node, you call the file path of your python file, and with a string constant you call the function you wish to use. You also need to establish the value type of the return your code is givig, in this case, a 2D array. You also need to wire your inputs for the code, for this example a csv file was used as input. 

<img width="440" height="191" alt="Image" src="https://github.com/user-attachments/assets/63d4724c-cf88-4c5b-b4cd-a77c1842d038" />