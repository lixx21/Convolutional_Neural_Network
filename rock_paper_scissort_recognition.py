# -*- coding: utf-8 -*-
"""Rock_Paper_Scissort_Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10R8lWlZz1QtUjh_kj_kKfRaRUBU2b4S3

Nama : Felix Pratamasan

Username : felix_pratamasan

Email : felixpratama242@gmail.com
"""

import tensorflow as tf
import zipfile,os

!wget --no-check-certificate \
https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip

#ekstrak data
local_zip = '/content/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

dir = os.path.join('/content/rockpaperscissors/rps-cv-images')

from tensorflow.keras.preprocessing.image import ImageDataGenerator
#split dan augmentasi train dan validation
datagenerator = ImageDataGenerator(rescale = 1./255,
                           rotation_range = 20,
                           width_shift_range = 0.3,
                           height_shift_range =0.3,
                           zoom_range = 0.2,
                           horizontal_flip = True,
                           shear_range = 0.2,
                           fill_mode = 'wrap',
                           validation_split = 0.4)


#Image generator
train_generator = datagenerator.flow_from_directory(dir, 
                                           target_size = (150, 150),
                                           batch_size = 32,
                                           shuffle = True,
                                           subset = 'training',
                                           class_mode = 'categorical'
                                           )

validation_generator = datagenerator.flow_from_directory(dir,
                                                 target_size = (150, 150),
                                                 batch_size = 32,
                                                 shuffle = True,
                                                 subset = 'validation',
                                                 class_mode = 'categorical'
                                                 )

from keras.callbacks import EarlyStopping

callback = EarlyStopping(monitor = 'val_loss',
                        patience = 3,
                        verbose = 1)

#compile
model = tf.keras.models.Sequential([
      tf.keras.layers.Conv2D(16,(3,3), activation ='relu', input_shape=(150,150,3)),
      tf.keras.layers.MaxPooling2D(2,2),
      tf.keras.layers.Conv2D(32,(3,3), activation ='relu'),
      tf.keras.layers.MaxPooling2D(2,2),
      tf.keras.layers.Conv2D(64,(3,3), activation ='relu'),
      tf.keras.layers.MaxPooling2D(2,2),
      tf.keras.layers.Conv2D(128,(3,3), activation ='relu'),
      tf.keras.layers.MaxPooling2D(2,2),

      tf.keras.layers.Flatten(),
      tf.keras.layers.Dropout(0.2),
 
      tf.keras.layers.Dense(512, activation = 'relu'),

      tf.keras.layers.Dense(3, activation='softmax'),

])
model.compile(optimizer = tf.optimizers.Adam(),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

model.fit(train_generator,
          steps_per_epoch = 20,
          epochs = 30,
          validation_data = validation_generator,
          validation_steps = 10,
          verbose = 2,
          callbacks = [callback])

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline


uploaded = files.upload()

for fn in uploaded.keys():

  #predicting images
  path = fn
  img = image.load_img(path, target_size = (150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis =0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)

  print(fn)
  if classes[0][0] == 1:
    print('predict : paper')
  elif classes [0][1] == 1 :
      print('predict : rock')
  else:
      print('predict : scissors')