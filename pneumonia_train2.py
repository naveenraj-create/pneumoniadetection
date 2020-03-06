from keras.preprocessing.image import ImageDataGenerator 
from keras.models import Sequential 
from keras.layers import Conv2D, MaxPooling2D 
from keras.layers import Activation, Dropout, Flatten, Dense 
from keras import backend as K 

  
img_width, img_height = 128, 128
  
train_data_dir = 'chest_xray/train'
validation_data_dir = 'chest_xray/test'
nb_train_samples = 5218 
nb_validation_samples = 634
epochs = 10
batch_size = 64
  
if K.image_data_format() == 'channels_first': 
    input_shape = (1, img_width, img_height) 
else: 
    input_shape = (img_width, img_height, 1) 
  
model = Sequential() 
model.add(Conv2D(32, (2, 2), input_shape = input_shape)) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2))) 
  
model.add(Conv2D(32, (2, 2))) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2)))
#
#  
model.add(Conv2D(64, (2, 2))) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2))) 
  
model.add(Flatten()) 
model.add(Dense(64)) 
model.add(Activation('relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(1)) 
model.add(Activation('sigmoid')) 
  
model.compile(loss ='binary_crossentropy', 
                     optimizer ='rmsprop', 
                   metrics =['accuracy']) 
  
train_datagen = ImageDataGenerator( 
                rescale = 1. / 255, 
				featurewise_std_normalization=True,
                 #shear_range = 0.2, 
                  #zoom_range = 0.2, 
            #horizontal_flip = True,
			zca_epsilon=1e-06,
			zca_whitening=True,
			brightness_range=(0.5,1.5)
			) 
  
test_datagen = ImageDataGenerator(rescale = 1. / 255) 
  
train_generator = train_datagen.flow_from_directory(train_data_dir, 
                              target_size =(img_width, img_height), 
                     batch_size = batch_size,color_mode='grayscale', class_mode ='binary') 
  
validation_generator = test_datagen.flow_from_directory( 
                                    validation_data_dir, 
                   target_size =(img_width, img_height), 
          batch_size = batch_size,color_mode='grayscale', class_mode ='binary') 
  
model.fit_generator(train_generator, 
    steps_per_epoch = nb_train_samples // batch_size, 
    epochs = epochs, validation_data = validation_generator, 
    validation_steps = nb_validation_samples // batch_size) 
  
model.save('model_saved_v.h5')