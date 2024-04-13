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
# %matplotlib inline

from torchvision.transforms import ToTensor
from torch.utils.data import Dataset, DataLoader
from PIL import Image


def predict(img):
    return "HELLO"