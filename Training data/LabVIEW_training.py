import os
import sys
import argparse

# FORCE PYTHON TO USE UTF-8 ENCODING FOR ALL PRINTS
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# --- COMMAND LINE ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description="LabVIEW Time-Forecast Training Pipeline")
parser.add_argument(
    '--model', 
    type=str, 
    default='Standard_MLP', 
    choices=['Standard_MLP', 'Deep_MLP', 'Light_MLP'],
    help='Select the neural network architecture layout'
)
args = parser.parse_args()
CHOSEN_MODEL = args.model

print("\n==================================================")
print(f"[INFO] TIMEFORECAST PIPELINE: Initializing Windowed Training...")
print(f"[INFO] Selected Architecture: {CHOSEN_MODEL}")
print("==================================================")

import torch
import torch.nn as nn
import torch.optim as optim

# 1. Setup paths
WORKING_DIR = r"C:\Users\genyd\OneDrive\Documentos\Trabajos\Personales\SURE\ZEUS\Training data"
INPUT_FILE = os.path.join(WORKING_DIR, "input_data.csv")
OUTPUT_PREDICTIONS = os.path.join(WORKING_DIR, "output_loss.csv") # Kept name intact for LabVIEW path
OUTPUT_STATUS = os.path.join(WORKING_DIR, "output_status.txt")
ONNX_FILE = os.path.join(WORKING_DIR, "trained_model.onnx")

WINDOW_SIZE = 2000

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Cannot find data at {INPUT_FILE}")
        sys.exit(1)
        
    print("[INFO] Reading dataset...")
    raw_data = []
    with open(INPUT_FILE, "r") as f:
        for line in f:
            if line.strip():
                row = [float(val) for val in line.strip().split('\t')]
                raw_data.append(row)

    data_tensor = torch.tensor(raw_data, dtype=torch.float32)
    total_rows = data_tensor.shape[0]
    
    print(f"[DATA] Total raw rows detected: {total_rows}")
    if total_rows <= WINDOW_SIZE:
        print(f"[ERROR] Dataset length ({total_rows}) must be greater than window size ({WINDOW_SIZE}).")
        sys.exit(1)

    # --- VECTORIZED SLIDING WINDOW GENERATION ---
    print(f"[DATA] Generating sliding windows (Size: {WINDOW_SIZE} frames)...")
    num_samples = total_rows - WINDOW_SIZE
    
    # Pre-allocate tensors for speed
    X = torch.zeros((num_samples, WINDOW_SIZE * 2), dtype=torch.float32)
    Y = torch.zeros((num_samples, 2), dtype=torch.float32)
    
    for i in range(num_samples):
        X[i] = data_tensor[i : i + WINDOW_SIZE].flatten() # Flattens 2000x2 into 4000
        Y[i] = data_tensor[i + WINDOW_SIZE]               # Next target point [X, Y]

    NUM_INPUT_FEATURES = WINDOW_SIZE * 2 # 4000
    NUM_TARGET_OUTPUTS = 2               # Predicting both X and Y

    # --- CHRONOLOGICAL 80/20 SPLIT (Standard for Time Series) ---
    train_size = int(0.8 * num_samples)
    
    X_train, Y_train = X[:train_size], Y[:train_size]
    X_test, Y_test = X[train_size:], Y[train_size:]

    print(f"[DATA] Train Split: {X_train.shape[0]} windows | Test Split: {X_test.shape[0]} windows")

    # --- MODEL SELECTIONS ADJUSTED FOR 4000 INPUT FEATURES ---
    if CHOSEN_MODEL == "Deep_MLP":
        model = nn.Sequential(
            nn.Linear(NUM_INPUT_FEATURES, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, NUM_TARGET_OUTPUTS)
        )
    elif CHOSEN_MODEL == "Light_MLP":
        model = nn.Sequential(
            nn.Linear(NUM_INPUT_FEATURES, 64),
            nn.ReLU(),
            nn.Linear(64, NUM_TARGET_OUTPUTS)
        )
    else:  # Standard_MLP
        model = nn.Sequential(
            nn.Linear(NUM_INPUT_FEATURES, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, NUM_TARGET_OUTPUTS)
        )

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    epochs = 20
    print(f"[TRAIN] Training {CHOSEN_MODEL} forecast engine for {epochs} epochs...")
    
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"   Epoch [{epoch+1}/{epochs}] | Train MSE Loss: {loss.item():.6f}")

    # Evaluation
    print("[EVAL] Running predictions on test timeline...")
    model.eval()
    with torch.no_grad():
        test_preds = model(X_test)

    # Export to ONNX
    print("[SAVE] Exporting time-series engine to ONNX format...")
    dummy_input = torch.randn(1, NUM_INPUT_FEATURES)
    torch.onnx.export(
        model, 
        dummy_input, 
        ONNX_FILE, 
        export_params=True, 
        opset_version=18,
        do_constant_folding=True,
        input_names=['input_trajectory'], 
        output_names=['predicted_xy']
    )

    # --- SAVE 4-COLUMN TRACKING DATA FOR LABVIEW ---
    print("[SAVE] Exporting X and Y parallel track data...")
    # Format: X_Real \t X_Pred \t Y_Real \t Y_Pred
    with open(OUTPUT_PREDICTIONS, "w") as f:
        Y_test_list = Y_test.tolist()
        test_preds_list = test_preds.tolist()
        for i in range(len(Y_test_list)):
            f.write(f"{Y_test_list[i][0]}\t{test_preds_list[i][0]}\t{Y_test_list[i][1]}\t{test_preds_list[i][1]}\n")
            
    # Write status and ONNX path
    status_msg = f"{ONNX_FILE}"
    with open(OUTPUT_STATUS, "w") as f:
        f.write(status_msg)
        
    print("[SUCCESS] Time-forecast training finished without errors!")

if __name__ == "__main__":
    main()