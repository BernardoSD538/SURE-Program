import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader

class Patch_MLP_ZEUS(nn.Module):
  def __init__(self, patch_size = 100, stride_size = 200, num_patches = 20, emmbedding_dim = 256):
    super(Patch_MLP_ZEUS, self).__init__()
    self.patch_size = patch_size
    self.stride_size = stride_size
    self.num_patches = num_patches
    self.emmbedding_dim = emmbedding_dim

    #Linar Embbeding Layer 
    self.emmbedding = nn.Linear(self.patch_size*2, self.emmbedding_dim)

    #Intra-Patch Mixing Layer
    self.intra_patch_mlp = nn.Sequential(
        nn.Linear(self.emmbedding_dim, self.emmbedding_dim),
        nn.ReLU(),
        nn.Linear(self.emmbedding_dim, self.emmbedding_dim)
        )
    
    #Inter-Patch Mixing Layer
    self.inter_patch_mlp = nn.Sequential(
      nn.Linear(self.num_patches, self.num_patches),
      nn.GELU(),
      nn.Linear(self.num_patches, self.num_patches)
    )

    #Flatten
    self.flatten = nn.Flatten()
    self.output_layer = nn.Linear(self.num_patches*self.emmbedding_dim,2)
  def forward(self, x):
    batch_size = x.size(0)

    patches = []
    for i in range(self.num_patches):
        start_idx = i*self.stride_size
        end_idx = start_idx + self.patch_size
        patch = x[:, start_idx:end_idx, :].reshape(batch_size, -1)
        patches.append(patch)

    x = torch.stack(patches, dim=1)
    x = self.emmbedding(x)

    x = x + self.intra_patch_mlp(x)
    x = x.permute(0, 2, 1)

    x = x + self.inter_patch_mlp(x)
    x = x.permute(0, 2, 1)

    x = self.flatten(x)
    predicted_pos = self.output_layer(x)
    return predicted_pos


class ZEUS_Dataset(Dataset):
    def __init__(self, csv_file, window_size, split = 'train', train_ratio = 0.8):
        df = pd.read_csv(csv_file)

        coords = df[['x', 'y']].values
        self.data = torch.tensor(coords, dtype = torch.float32)
        self.window_size = window_size
        self.split = split

        self.total_windows = len(self.data) - self.window_size
        self.split_index = int(self.total_windows * train_ratio)

    def __len__(self):
        if self.split == 'train':
            return self.split_index
        else:
            return self.total_windows - self.split_index

    def __getitem__(self, idx):
        if self.split != 'train':
            idx += self.split_index
            
        x_history = self.data[idx: idx + self.window_size]

        y_target = self.data[idx + self.window_size]

        return x_history, y_target
    
train_dataset = ZEUS_Dataset('C:/Users/genyd/OneDrive/Documentos/Trabajos/Personales/SURE/ZEUS/Time_series_5min_data.csv', window_size=3900, split='train')
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = ZEUS_Dataset('C:/Users/genyd/OneDrive/Documentos/Trabajos/Personales/SURE/ZEUS/Time_series_5min_data.csv', window_size=3900, split='test')
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False) #Remember to never shuffle test

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = Patch_MLP_ZEUS().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)


epochs = 10 
for epoch in range(epochs):
    model.train()
    running_train_loss = 0.0

    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        predictions = model(batch_x)

        loss = criterion(predictions, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) #Gradient clipping to prevent exploding gradients
        optimizer.step()

        running_train_loss += loss.item()

    #Calculated average train loss for the epoch
    epoch_train_loss = running_train_loss / len(train_loader)

    model.eval()
    running_test_loss = 0.0

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            predictions = model(batch_x)
            loss = criterion(predictions, batch_y)

            running_test_loss += loss.item()

    #Calculated average test loss for the epoch        
    epoch_test_loss = running_test_loss / len(test_loader)

    #Printing results
    print(f'Epoch {epoch+1}/{epochs} - Train Loss: {epoch_train_loss:.4f} - Test Loss: {epoch_test_loss:.4f}')