import math
import six
import tensorflow as tf
from tensorflow import keras
import shutil
from enum import Enum
from einops.layers.tensorflow import Rearrange
import logging
import numpy as np
from fastprogress import master_bar, progress_bar
import random
import glob
import os
import pickle as pickle
from sklearn.preprocessing import normalize
import _pickle as cPickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
from collections import OrderedDict
import torch.nn.functional as F
from torch.utils.data import Dataset,DataLoader
from sklearn.model_selection import train_test_split
import fnmatch
import os
import random
import re
import threading
import numpy as npx
from six.moves import xrange
import time
import json
import torch as t
from torch.utils.data import Dataset,DataLoader
from torch.utils.data.distributed import DistributedSampler
from time import sleep
import math
import functools
from imblearn.over_sampling import RandomOverSampler
import absl.logging as _logging  # pylint: disable=unused-import
import collections
import re
import six
from os.path import join
from six.moves import zip
from absl import flags
from sklearn.metrics import confusion_matrix,classification_report
from Model import*
from Dataset import*
from Trainer import*

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as input:  # Overwrites any existing file.
        dataset_reload = pickle.load(input)

    return dataset_reload

def main():

    collate_fn = lambda batch: t.stack([t.from_numpy(b) for b in batch], dim=0)

    seconds = 60
    count = 0
    dataset = Dataset_train(seconds, count)
    dataset_test = Dataset_test(seconds, count)

    # sample usage
    # save_object(dataset, '/content/drive/My Drive/EMOTION/loader_60_mix.pkl')
    # dataset = load_object('/content/drive/My Drive/EMOTION/loader_60_mix.pkl')
    # dataset_test = load_object('/content/drive/My Drive/EMOTION/loader_60_mix_test.pkl')

    print("Length of dataset is ", len(dataset))
    print("Length of dataset is ", len(dataset_test))

    train_loader = DataLoader(dataset, batch_size=32, pin_memory=False, shuffle=True)  # collate_fn=collate_fn)
    test_loader = DataLoader(dataset_test, batch_size=32, pin_memory=False, shuffle=False)  # collate_fn=collate_fn)

    logger = logging.getLogger(__name__)

    tconf = TrainerConfig(max_epochs=100, batch_size=32, learning_rate=1e-5)

    # sample model config.
    model_config = {"image_size": 768,
                    "patch_size": 768,
                    "num_classes": 2,
                    "dim": 512,
                    "depth": 6,
                    "heads": 8,
                    "mlp_dim": 1024}

    trainer = Trainer(ViT, model_config, train_loader, len(dataset), test_loader, len(dataset_test), tconf)
    trainer.train()

if __name__ == "__main__":
    main()