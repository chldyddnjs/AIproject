import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math

#Define Constants
batch_size = 128
epochs = 100
num_classes = 10

#Download MINST dataset
mnist = keras.datasets.mnist
(train_images,train_labels), (test_images,test_labels) = mnist.load_data()

len(train_images),len(test_images)

#Nomalize the input image so that each pixel value is between 0 to 1.
train_images = train_images /255.0
test_images = test_images /255.0

#Helper function to display digit images
def show_sample(images,labels,sample_count=25):
  grid_count = math.ceil(math.ceil(math.sqrt(sample_count)))
  grid_count = min(grid_count,len(images),len(labels))

  plt.figure(figsize=(2*grid_count,2*grid_count))
  for i in range(sample_count):
    plt.subplot(grid_count,grid_count,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(images[i],cmap=plt.cm.gray)
    plt.xlabel(labels[i])
  plt.show()
def show_sample_digit(images,labels,digit,sample_count=25):
  grid_count = math.ceil(math.ceil(math.sqrt(sample_count)))
  grid_count = min(grid_count,len(images),len(labels))
  
  plt.figure(figsize=(2*grid_count,2*grid_count))
  i=0
  digit_count = 0
  while digit_count < sample_count:
    i += 1
    if(digit == labels[i]):
      plt.subplot(grid_count,grid_count,digit_count + 1)
      plt.xticks([])
      plt.yticks([])
      plt.grid(False)
      plt.imshow(images[i],cmap=plt.cm.gray)
      plt.xlabel(labels[i])
    plt.show()
    #Helper function to display specfic digit images
def show_digit_images(image):
  #Draw digit_image
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)

  major_ticks = np.arange(0,29,5)
  minor_ticks = np.arange(0,29,1)
  ax.set_xticks(major_ticks)
  ax.set_yticks(minor_ticks,minor=True)
  ax.set_xticks(major_ticks)
  ax.set_yticks(minor_ticks,minor=True)
  ax.grid(which='both')
  ax.grid(which='minor',alpha=0.2)
  ax.grid(which='major',alpha=0.5)
  ax.imshow(image,cmap=plt.cm.binary)

  plt.show()

model = keras.Sequential([
                          keras.layers.Flatten(input_shape=(28,28)),
                          keras.layers.Reshape(target_shape=(28,28,1)),
                          keras.layers.Conv2D(filters=32,kernel_size=(3, 3), strides=(1,1), activation=tf.nn.relu),
                          keras.layers.Conv2D(filters=64,kernel_size=(3, 3), strides=(1,1),activation=tf.nn.relu),
                          keras.layers.MaxPooling2D(pool_size=(2,2)),
                          keras.layers.Dropout(0.25),
                          keras.layers.Flatten(input_shape=(28,28)),
                          keras.layers.Dense(128,activation=tf.nn.relu),
                          keras.layers.Dropout(0.5),

                          keras.layers.Dense(num_classes, activation='softmax')
])
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

              #Save the best model as digit_model.h5
filepath = '/model/digits_model.h5'
modelCheckpoint = tf.keras.callbacks.ModelCheckpoint(filepath=filepath,save_best_only=True)

history = model.fit(train_images,train_labels,
                   validation_data=(test_images,test_labels),
                   epochs=epochs, batch_size=batch_size,
                   callbacks=[modelCheckpoint])

fig, loss_ax = plt.subplots()
fig, acc_ax  = plt.subplots()
loss_ax.plot(history.history['loss'],'ro', label = 'train_loss')
loss_ax.plot(history.history['val_loss'],'r:',label = 'Validation_loss')
loss_ax.set_xlabel('epochs')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper left')

acc_ax.plot(history.history['accuracy'],'bo', label = 'train_accuracy')
acc_ax.plot(history.history['val_accuracy'],'b:',label='validation_accuracy')
acc_ax.set_xlabel('epochs')
acc_ax.set_ylabel('accuracy')
acc_ax.legend(loc='upper left')
plt.show()