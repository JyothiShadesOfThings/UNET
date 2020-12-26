#pip install git+https://github.com/tensorflow/examples.git
#pip install -U tfds-nightly
#pip install tensorflow_addons

from glob import glob

import IPython.display as display
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import datetime, os
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from IPython.display import clear_output
import tensorflow_addons as tfa

from tensorflow_examples.models.pix2pix import pix2pix
import tensorflow as tf
import tensorflow.keras.backend as backend
import tensorflow_datasets as tfds

import json
from sklearn.metrics import confusion_matrix