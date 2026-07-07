import numpy as np
import onnxruntime as ort
import os
import time  # <--- STEP 1: Import the time module

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Initialize the ONNX session
onnx_path = os.path.join(script_dir, "zeus_laser_tracker.onnx")
session = ort.InferenceSession(onnx_path)

# 2. Load the scaling parameters
scaling_path = os.path.join(script_dir, "scaling_params.npz")
scaling_data = np.load(scaling_path)
mean = scaling_data['mean']  # [mean_x, mean_y]
std = scaling_data['std']    # [std_x, std_y]

def predict_coordinates(lv_array_2d):
    """
    lv_array_2d: Raw X and Y coordinates directly from LabVIEW
    """
    start_time = time.perf_counter()  # <--- STEP 2: Start high-resolution timer
    
    # 1. Reconstruct the 2D matrix layout from LabVIEW
    raw_flat = np.array(lv_array_2d, dtype=np.float32).flatten()
    reconstructed_2d = raw_flat.reshape(-1, 2)
    current_rows = reconstructed_2d.shape[0]
    
    # 2. Dynamic padding
    repeats = int(np.ceil(2000 / current_rows))
    padded_data = np.tile(reconstructed_2d, (repeats, 1))
    truncated_data = padded_data[:2000, :]
        
    # 3. STANDARDIZE THE INCOMING DATA
    standardized_data = (truncated_data - mean) / std
    
    # 4. Reshape to 3D Tensor format: (1, 2000, 2)
    input_tensor = np.expand_dims(standardized_data, axis=0).astype(np.float32)
    
    # 5. Execute ONNX Inference
    outputs = session.run(['predicted_xy'], {'input_timeline': input_tensor})
    
    # 6. UN-STANDARDIZE THE PREDICTION
    scaled_pred = outputs[0][0] 
    real_x = float((scaled_pred[0] * std[0]) + mean[0])
    real_y = float((scaled_pred[1] * std[1]) + mean[1])
    
    end_time = time.perf_counter()  # <--- STEP 3: Stop timer
    elapsed_ms = (end_time - start_time) * 1000.0  # Convert to milliseconds
    
    # 7. Format as a 2D nested list containing: [[X, Y, Time_ms]]
    prediction_2d = [[real_x, real_y, elapsed_ms]]  # <--- STEP 4: Add time to output
    
    return prediction_2d