# identification-and-classification-of-sea-going-vessels-using-satellite-images

The aim of this study was to analyze the possibility of using machine learning and computer vision to identify (indicate the location) of all sea-going vessels located in the selected area of the open sea and to classify the main attributes of the vessel. 
The key elements of the project were to download data from the Sentinel-1 satellite, download AIS data on the sea vessels, then automatically tag data and develop a detection and classification algorithm. 
The results obtained from the YOLOv7 model on the test set were mean Average Precision (mAP@.5) = 91% and F1-score = 93% for the single-class ship detection task. 
When combining the task of ship detection with a ship’s length and width classification, mean Average Precision for all classes was 40%, F1-score was 41%.

Results obtained during the ship detection experiment confirmed the correctness of the collected and processed data along with the neural network training process. 
Mean Average Precision at level of 91% on the test set is similar to the level achieved by Yang et al., Zhang et al. on HRSID dataset, a little bit higher than results obtained by Yu et al. on HRSID dataset and a little bit lower than the results obtained by Ming et al. and Zhang et al. on SSDD dataset. 
However, in terms of F1-score model presented in this work has one of the highest results with the level of 93%. 
It also shows the superiority of YOLOv7 model comparing to its earlier versions and variations.

Results obtained during ship classification experiment are worse than expected. 5-classes ship classification mean Average Precision was at the level of 40%, which is the lowest from the compared solution. 
The reasons for the lower mAP and F1-score (which was at the level of 41%) may be the input size of the tiles.  It was decided to use 120x120 px images, while others like Sannapu et al. or Hou et al. used 512x512 px images.
Broader image contains more context and may be more useful in the ship classifying task.  Another reason may be the data preprocessing steps. 
Preprocessing was done in order to improve the classification results, however, some steps may be added in order to make it even better. 
Last reason is connected with the division into 5 classes based on Length attibute. It was done using k-means clustering, but the boundaries between classes were not sharp, rather smooth. 
Thus, the differences between classes were more difficult to distinguish for the model leading to mistakes in the classification process.

This research was carried out by D. Kobiela and T. Berezowski [[1]](#1) for the conference IGARSS 2023.
Reasearch poster with the summary of the performed work can be seen in the [research project poster](POSTER_IGARSS_2023.pdf).

![research project poster](POSTER_IGARSS_2023.png)

## References
<a id="1">[1]</a> 
Dariusz Kobiela, Tomasz Berezowski. 
Classification of sea going vessels properties using SAR satellite images. 
IEEE Geoscience and Remote Sensing Society and the IGARSS 2023 conference.  
https://2023.ieeeigarss.org/.


