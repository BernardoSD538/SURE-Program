# LabVIEW 2017 + ONNX Runtime (x64-1.24.3)
+ YOLOv8n for for coin detection
+ custom neural network for predicting rotation angle
+ EfficientNet-B4 for coin classification

**Video:**
- [rutube.ru](https://rutube.ru/video/b37fe715582c7ebc2089b3c2fe2eeb3a/)
- [youtu.be](https://youtu.be/AT9D4SQ7oe0)


**Tested:**
- Ubuntu 24.04lts - 64bit
- Windows 10 - 64bit

Ubuntu example (Test YOLO):
![FP_Linux](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/FP_lin.png)
![BD_Linux](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/BD_lin.png)

Windows example (Test EfficientNet-B4):
![FP_Linux](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/FP_win.png)
![BD_Linux](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/BD_win.png)

**Version using Classes:**
![BD_Class_YOLO](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/BD_Class_YOLO.png)
![BD_Class_EfficientNet](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/BD_Class_EfficientNet.png)
 
# Логика работы следующая:

**1 этап** детекция (ИНС YOLOv8n):
- преобразование изображения [1024, 1024] в тензор [1, 3, 1024, 1024] и подача его на вход ИНС
- преобразование полученных от ИНС данных в читаемый вид, фильтрация по порогу и NMS
- отображение результата детектирования

**2 этап** компенсация угла поворота (ИНС самодельная):
- сегментация изображения (по результатам 1 этапа)
- изменение размера изображения [х.з] -> [512, 512]
- преобразование изображения [512, 512] в тензор [1, 3, 512, 512] и подача его на вход ИНС
- преобразование полученных от ИНС данных [sin, cos] в угол и его компенсация
- отображение результата (сегментация, масштабирование, поворот)

**3 этап** идентификация (ИНС EfficientNet-B4):
- изменение размера [512, 512] -> [380, 380]
- преобразование изображения [380, 380] в тензор [1, 3, 380, 380] и подача его на вход ИНС
- преобразование полученных от ИНС данных в вероятности для каждого из двух классов [Avers, Revers]
- отображение результата

# Logic:

**Stage 1:** Detection (YOLOv8n ANN):
- Convert the [1024, 1024] image to a [1, 3, 1024, 1024] tensor and feed it to the ANN input
- Convert the data received from the ANN to a readable form, filter by threshold and NMS
- Display the detection result

**Stage 2:** Rotation angle compensation (homemade ANN):
- Image segmentation (based on the results of stage 1)
- Image resizing [x, x] -> [512, 512]
- Convert the [512, 512] image to a [1, 3, 512, 512] tensor and feed it to the ANN input
- Convert the [sin, cos] data received from the ANN to an angle and compensate for it
- Display the result (segmentation, scaling, rotation)

**Stage 3:** Identification (ANN EfficientNet-B4):
- Image resizing [512, 512] -> [380, 380]
- Transform image [380, 380] into tensor [1, 3, 380, 380] and feed it to ANN input
- Transform data received from ANN into probabilities for each of the two classes [Avers, Revers]
- Display result


# New example:
![FP_Test_Xiaolei_Hu](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/FP_Test_Xiaolei_Hu.png)
![BD_Test_Xiaolei_Hu](https://github.com/IvanLisRus/LabVIEW-ONNX_Runtime/blob/main/img_LabVIEW/BD_Test_Xiaolei_Hu.png)

**en:** Thanks to user Xiaolei Hu, who found a bug in the code and shared an ONNX model example, we now have an example of reading multiple outputs (with dynamic dimensions) with different data types.

**ru:** Благодаря пользователю Xiaolei Hu, который обнаружил ошибку в коде и поделился примером модели ONNX, теперь есть пример чтения данных с нескольких выходов разных типов с динамической размерностью.
