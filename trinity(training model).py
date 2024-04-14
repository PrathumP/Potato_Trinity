# -*- coding: utf-8 -*-
"""Trinity.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1osrMW48W9GtRw9PFYsTR6yCRmzBY5YYH
"""

# from google.colab import drive
# drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.

import torch

import os
import torchvision
import numpy as np
import matplotlib
import torch
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
from torchvision.datasets import DatasetFolder
import torchvision.transforms as transforms
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchvision.utils import make_grid
from torch.utils.data.dataloader import DataLoader
from torch.utils.data import random_split
import torchvision.transforms as tt
# %matplotlib inline

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

from torchvision.transforms import ToTensor
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os

# Define the data path and label mapping
data_path = 'drive/MyDrive/Potato'
label_map = {
    'Potato___healthy': 0,
    'Potato___Early_blight': 1,
    'Potato___Late_blight': 2
}

# Initialize empty lists to store images and labels
images = []
labels = []

# Iterate through each folder in the data path
for folder_name in os.listdir(data_path):
    if folder_name in label_map:
        folder_path = os.path.join(data_path, folder_name)
        for file_name in os.listdir(folder_path):
                # Construct the full path to the image file
                image_path = os.path.join(folder_path, file_name)

                # Load the image using PIL (Pillow)
                # image = Image.open(image_path).convert('RGB')
                # can do above too , like idk tbh
                image = Image.open(image_path)

                # Append the image and corresponding label to the lists
                images.append(image)
                labels.append(label_map[folder_name])

# Define a custom dataset class
class CustomDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

# Create an instance of CustomDataset with transformations
transform = ToTensor()  # Convert PIL image to PyTorch tensor
#Data augmentation

custom_dataset = CustomDataset(images, labels, transform=transform)

# # Create a DataLoader for the custom dataset
# batch_size = 32
# data_loader = DataLoader(custom_dataset, batch_size=batch_size, shuffle=True)

# # Test the DataLoader by iterating through a few batches
# for batch_images, batch_labels in data_loader:
#     print("Batch images shape:", batch_images.shape)
#     print("Batch labels:", batch_labels)
#     break  # Stop after processing the first batch for demonstration

print(isinstance(custom_dataset, Dataset)) #custom_dataset is a Dataset instance and not a tensor.

len(custom_dataset)

image,label=custom_dataset[0]
print(image.shape)
# Assuming 'image_tensor' is the tensor with shape [3, 256, 256]
# You can replace 'image_tensor' with your specific tensor variable

# Convert the tensor image to a numpy array
image_np = image.permute(1, 2, 0).cpu().numpy()  # Permute dimensions for matplotlib (HWC)

# Clip the pixel values to be within [0, 1] (assuming RGB image)
image_np = image_np.clip(0, 1)

# Display the image using matplotlib
plt.imshow(image_np)
plt.axis('off')  # Turn off axis labels
plt.show()
print(label)

def show_example(img, label):   #printing the images
    print('Label: ', custom_dataset.classes[label], "("+str(label)+")")
    plt.imshow(img.permute(1, 2, 0))

random_seed = 42
torch.manual_seed(random_seed);

val_size = 450
train_size = len(custom_dataset) - val_size

train_ds, val_ds = random_split(custom_dataset, [train_size, val_size])

len(train_ds), len(val_ds)

import torchvision.transforms as transforms
from torch.utils.data import ConcatDataset

train_transform = tt.Compose([tt.RandomCrop(256, padding=4, padding_mode='reflect'),
                         tt.RandomHorizontalFlip(),
                         tt.RandomRotation(degrees=20),
                         # tt.RandomResizedCrop(256, scale=(0.5,0.9), ratio=(1, 1)),
                         tt.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1)
                        ])

augmented_datasets = []

# Apply transformations to each sample in train_ds
for image, label in train_ds:
    augmented_samples = []
    for _ in range(4):  # Define the number of augmented samples per original sample
        augmented_image = train_transform(image)
        augmented_samples.append((augmented_image, label))
    # Convert augmented samples to tensors
    augmented_images, augmented_labels = zip(*augmented_samples)
    augmented_images = torch.stack(augmented_images)  # Convert list of tensors to a single tensor
    augmented_labels = torch.tensor(augmented_labels)  # Convert list of labels to a tensor
    augmented_datasets.append(torch.utils.data.TensorDataset(augmented_images, augmented_labels))

# Concatenate the augmented datasets
augmented_train_ds = ConcatDataset(augmented_datasets)

len(augmented_train_ds)

image,label=augmented_train_ds[0]
print(image.shape)
# Assuming 'image_tensor' is the tensor with shape [3, 256, 256]
# You can replace 'image_tensor' with your specific tensor variable

# Convert the tensor image to a numpy array
image_np = image.permute(1, 2, 0).cpu().numpy()  # Permute dimensions for matplotlib (HWC)

# Clip the pixel values to be within [0, 1] (assuming RGB image)
image_np = image_np.clip(0, 1)

# Display the image using matplotlib
plt.imshow(image_np)
plt.axis('off')  # Turn off axis labels
plt.show()
print(label)

from torch.utils.data.dataloader import DataLoader

batch_size=32

train_loader = DataLoader(augmented_train_ds, batch_size, shuffle=True, num_workers=4, pin_memory=True)
val_loader = DataLoader(val_ds, 48, num_workers=4, pin_memory=True)

len(train_loader)

len(val_loader)

import torch.nn as nn
import torch.nn.functional as F

class Potato(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss

    def validation_step(self, batch):
        images, labels = batch
        out = self(images)                    # Generate predictions for each batch
        loss = F.cross_entropy(out, labels)   # Calculate loss for each batch
        acc = accuracy(out, labels)           # Calculate accuracy for each batch
        return {'val_loss': loss.detach(), 'val_acc': acc}

    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}

    def epoch_end(self, epoch, result):
        print("Epoch [{}], train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['train_loss'], result['val_loss'], result['val_acc']))

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

def conv_block(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]
    if pool: layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)

class ResNet9(Potato):
    def __init__(self, in_channels, num_classes):
        super().__init__()

        self.conv1 = conv_block(in_channels, 64)  #46 x 256 x 256
        self.conv2 = conv_block(64, 128, pool=True) #128 x 128 x 128
        self.res1 = nn.Sequential(conv_block(128, 128), conv_block(128, 128)) #128 x 128 x 128

        self.conv3 = conv_block(128, 256, pool=True)
        self.conv4 = conv_block(256, 512, pool=True)
        self.res2 = nn.Sequential(conv_block(512, 512), conv_block(512, 512))  #512 x 32 x 32
        self.classifier = nn.Sequential(nn.MaxPool2d(4),                       #512 x 8 x 8
                                        nn.Flatten(),
                                        nn.Dropout(0.3),
                                        nn.Linear(512*8*8, num_classes))

    def forward(self, xb):
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out

def get_default_device():         
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device

    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl:
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)

device = get_default_device()
device

model = to_device(ResNet9(3,3), device)
model

torch.cuda.is_available()

train_loader = DeviceDataLoader(train_loader, device) #moves the train,val data and model to the GPU
val_loader = DeviceDataLoader(val_loader, device)
to_device(model, device)

@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def fit_one_cycle(epochs, max_lr, model, train_loader, val_loader,
                   grad_clip=None, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []

    # Set up cutom optimizer with weight decay
    optimizer = opt_func(model.parameters(), max_lr)#, weight_decay=weight_decay)
    # Set up one-cycle learning rate scheduler
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr, epochs=epochs,
                                                steps_per_epoch=len(train_loader))

    for epoch in range(epochs):
        # Training Phase
        model.train()
        train_losses = []
        lrs = []
        for batch in train_loader:
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()

            # # Gradient clipping
            # if grad_clip:
            #     nn.utils.clip_grad_value_(model.parameters(), grad_clip)

            optimizer.step()
            optimizer.zero_grad()

            # Record & update learning rate
            lrs.append(get_lr(optimizer))
            sched.step()

        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['lrs'] = lrs
        model.epoch_end(epoch, result)
        history.append(result)
    return history

evaluate(model, val_loader)

num_epochs = 10
opt_func = torch.optim.Adam
lr = 0.1

history = fit_one_cycle(num_epochs, lr, model, train_loader, val_loader, opt_func)

torch.save(model.state_dict(), 'PotatoWeights.pth')

