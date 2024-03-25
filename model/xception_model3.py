# Importing the necessary module to mount Google Drive
from google.colab import drive

# Mounting Google Drive to access files from Google Drive
# This will prompt you to authorize access to your Google Drive account
drive.mount('/content/drive')

!pip install tensorflow

import os   # Importing os module to navigate into the drive folders and access the images
import matplotlib.pyplot as plt   # Importing matplotlib.pyplot module to make plots
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator  # Importing ImageDataGenerator from Keras to process images in batches and apply transformations
from keras.optimizers import Adam    # Importing the Adam optimizer

from tensorflow.keras.applications import Xception  # Importing the Xception model architecture from TensorFlow's Keras applications
from tensorflow.keras.models import Sequential  # Importing the Sequential model to build a linear stack of layers
from tensorflow.keras.layers import Dense, Dropout, Flatten  # Importing specific layer types (Dense, Dropout, Flatten) from Keras


# Define the base directory where the 'sample' folder is located in your Google Drive
base_dir = '/content/drive/My Drive/Sample'

# Define the paths to the directories containing training, validation, and testing data
train_dir = os.path.join(base_dir, 'train')  # Path to the training data directory
validation_dir = os.path.join(base_dir, 'validation')  # Path to the validation data directory
test_dir = os.path.join(base_dir, 'test')  # Path to the testing data directory


# Rescale the pixel values from [0, 255] to [0, 1] for normalization

train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen  = ImageDataGenerator(rescale=1./255)
test_datagen  = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),   # This is the input size required for the VGG19 model
    batch_size=32,  # It will be iterating from batches of 20 images
    class_mode= 'binary'  # Label the images in a binary way (Fake or Real)
)

Validation_generator = validation_datagen .flow_from_directory(
    validation_dir,
    target_size=(224,224),   # This is the input size required for the VGG19 model
    batch_size=20,  # It will be iterating from batches of 20 images
    class_mode= 'binary'  # Label the images in a binary way (Fake or Real)
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),   # This is the input size required for the VGG19 model
    batch_size=20,  # It will be iterating from batches of 20 images
    class_mode= 'binary',  # Label the images in a binary way (Fake or Real)
    shuffle=False)  # No need to shuffle the test data

# Importing necessary modules
from keras.callbacks import EarlyStopping
from keras.regularizers import l2

# Load the Xception model pre-trained on ImageNet, excluding its top (fully connected) layers
base_model = Xception(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the layers of the base model to prevent them from being updated during training
for layer in base_model.layers:
    layer.trainable = False

# Define the model architecture
model = Sequential([
    base_model,  # Adding the pre-trained Xception base model
    Flatten(),  # Flatten the output of the base model to a 1D vector
    Dense(256, activation='relu', kernel_regularizer=l2(0.01)),  # Add a fully connected layer with 256 units and ReLU activation, applying L2 regularization
    Dropout(0.2),  # Add dropout for regularization (reduce overfitting)
    Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01))  # Add the output layer with sigmoid activation for binary classification, applying L2 regularization
])

# Model compilation with Adam optimizer, binary_crossentropy loss function, and accuracy metric
model.compile(optimizer=Adam(learning_rate=1e-3),
               loss='binary_crossentropy',
               metrics=['accuracy'])

# Model training
num_epochs = 20

# Early stopping callback to prevent overfitting and restore the best weights
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Fit the model on the training data generator
history = model.fit(
    train_generator,
    steps_per_epoch=86,   # Batch size is 20, 20 times 40 is 800, the size of the training data
    epochs=num_epochs,
    validation_data=Validation_generator,
    validation_steps=5,
    callbacks=[early_stopping]  # Include early stopping callback for preventing overfitting
)


training_accuracy = history.history['accuracy']
max_accuracy3 = max(training_accuracy)
min_accuracy3 = min(training_accuracy)

print("Model 3 - Maximum training accuracy:", max_accuracy3)
print("Model 3 - Minimum training accuracy:", min_accuracy3)


# Evaluate the model's performance on the test set
test_loss, test_accuracy = model.evaluate(test_generator)
print('Test loss for model:', test_loss)
print('Test accuracy for model:', test_accuracy)

# Extract the accuracy and loss values from the training history
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

# Define the range of epochs
epochs = range(1, len(acc) + 1)

# Plot the training and validation accuracy
plt.plot(epochs, acc, label='Training accuracy', color='lightgreen', linestyle='-')
plt.plot(epochs, val_acc, label='Validation accuracy', color='lightcoral', linestyle='-')
plt.title('Model 3 - Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plot the training and validation loss
plt.plot(epochs, loss, label='Training loss', color='lightgreen', linestyle='-')
plt.plot(epochs, val_loss, label='Validation loss', color='lightcoral', linestyle='-')
plt.title('Model 3 - Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()



