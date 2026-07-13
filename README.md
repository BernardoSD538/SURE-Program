# Development of a Machine Learning–Based Laser Pointing Stabilization System for ZEUS

## Creation of LabVIEW porgrams capable of using already trained AI model to predict X and Y coordinates, as well as LabVIEW program for training model via Python. 

This project has the objetive of implementing the use of an AI model to predcit values and be able to use them within LabVIEW. To achieve this purpuse two LabVIEW VIs were made as options: The Python Node method, and Ivan's method. Both are able to use an ONNX file of an already created model to predict X and Y values and show them in LabVIEW. A third LabVIEW VI was made with the purpuse of also being able to train AI model within LabVIEW and view performance results of the same. In the following text, a brief explanation of each VI will be given for general understanding of how each one works, but a more detailed Guide on how to make them is available for each VI inside their folder. 

- Python Node method 
    * Requirements:
        + 2018 LabVIEW version or newer.
        + bit matching LabVIEW and Python (32 or 64 bit)
        + Python libraries: Numpy, PyTorch, onnx, onnxruntime, os, pandas.

This method uses LabVIEW's built in blocks to use python code. This are the Open Python Session, Python Node, and Close Python Session blocks. The logic in LabVIEW is simple, you just need to open a python session, call the python code and its desired function via the Python Node, store the return values given by the python code somewhere, and finally close the python session. The image below shows the general working of this method. For this example, an ONNX file model was used. As you can see on the Python Node, you call the file path of your python file, and with a string constant you call the function you wish to use. You also need to establish the value type of the return your code is givig, in this case, a 2D array. You also need to wire your inputs for the code, for this example a csv file was used as input. 

<div align="center">
  <img alt="Image" src="https://github.com/user-attachments/assets/63d4724c-cf88-4c5b-b4cd-a77c1842d038" />
</div>

- Ivan's method
    * Requirements:
        + [Ivan's repository link](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime)
        + 64 bit LabVIEW
        + ONNX file of your AI model

This method uses LabVIEW libraries created by a Github user called Ivan. While Ivan's libraries have big applications on computer vision, we will only use and concentrate on those that help us open a ONNX file and make an inference with it. The general flow of the LabVIEW program consists of 3 parts: Preprocessing, Inference, and PostProcessing. Just like any prediction with AI models, for this example initial data was normalized, then given into the onnx model for inference, and post processed to get the real X and Y predicted values. The general structure of the VI is show in the image below. The structure of your code will change depending on you pre and post processing, but the Inference stays the same, ussing the Init.vi, PreProcess.vi and RunInference.vi blocks for a library to open the onnx file, read the input data, and do the inference, respectively. 

<div align="center">
    <img width="100%" height="100%" alt="Image" src="https://github.com/user-attachments/assets/4fafdf0d-29af-4362-b2c2-53a9b0a2b8a5" />
</div>

- Training Model
    * Requirements:
        + 64 bit Python
        + Python libraries: PyTorch, os, sys, argparse

This specific code is designed to be able to use 32 bit LabVIEW with 64 bit Python, as the AI training libraries are only available in the 64 bit Python. This code works using a System Exec.vi block, whose purpuse is to send a command line to windows in order to run a desired python code capable of training an AI model and returning performance results, as well as the path of a ONNX file created for the model. It was also designed to be able to select between different arquitectures or models, using an Enum, Format Into String blocks, and argparse in python. The image below shows the expected results from this example (predictions are not correct, as it wasn't the focus for this project)

<div align="center">
    <img width="65%" height="65%" alt="Image" src="https://github.com/user-attachments/assets/6b2ff45c-3589-40b5-b947-0c5c616ee1ae" />
</div>
