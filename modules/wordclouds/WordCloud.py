import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# WordClouds
# illustrates the most frequently words in a text


def join_list_of_strings(_list):
    return ' '.join(i for i in _list)


def create_cloud(text):
    cloud = WordCloud(background_color="white", max_words=75)
    cloud.generate(text)
    return cloud


# shows a cloud in the shape of the image
def show_image_cloud(text, image_path):
    cloud_mask = np.array(Image.open(image_path))
    cloud = WordCloud(mask=cloud_mask, background_color="white", max_words=75)
    cloud.generate(text)
    return cloud


def show_cloud(cloud):
    plt.imshow(cloud) # creates an image from a 2-dimensional numpy array
    plt.axis('off') # don't show axies
    plt.show()


def save_cloud(cloud, file_path):
    cloud.to_file(file_path) # save file local
