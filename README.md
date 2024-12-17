In case you want to test the pipeline, the following steps need to be taken:

1) Extract CNN training patches: as shown in `extract_patches.py`

2) Train CNN: open the `train_net.py` and change DATA_DIR to point to the patches path extracted from the previous step. Run the script, it will save the trained network as shown [here](https://github.com/pardhu-B-chowdary/Image-Forgery-Detection/blob/main/train_net.py)

3) Compute image features: as shown in `feature_extraction.py`. Here you will need to provide the trained CNN as input from the previous step. Change the path in the following [line](https://github.com/pardhu-B-chowdary/Image-Forgery-Detection/blob/main/feature_extraction.py)

4) Run SVM cross-validation: change the features path in `svm_classification.py` at line 5 to point to the latest feature extraction. Run the script.
