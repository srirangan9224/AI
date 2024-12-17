# Experimentations

## initial setup
I started the model with one convolutional layer and one pooling layer.The initial setup had a dropout rate of 0.5 (50%) and the number of hidden layers was 1000. Moreover the images were tested with 10 different patterns.This setup had a success rate of 95% on testing data and 93% on training data.All the activation functions used were "relu".

## experiment-1
In this experiment, I changed the number of hidden layers to 100.This change drastically reduced the accuracy rate.The accuracy had reduced by almost 88%.The remaining values were kept constant for this experiment.

## experiment-2
In this experiment,I reverted to the old number of hidden layers and changed the dropout rate from 0.5 to 0.75.This reduced the accuracy rate to 51% in the training data. However, the accuracy rate of the testing data was almost 20% more than that of the training data.

## experiment-3
In this experiment, I increased the number of filters used in the convolution of the image from 10 to 100 while changin all remaining value to their original value. This slowed the time taken for the code to run. However, this increased the accuracy of the model. which became almost 96%

## experiment-4
In this experiment, I increased the number of convolutions and pooling to 2 instead of one and reduced the number of units to 500.I also changed the number of filters on the convoulution of the image to 80. This increased the accuracy to almost 98% and the time taken for the model to run the code was also reduced. This code also had a 97% accuracy in the training set. This is the version that best reflects my final code.