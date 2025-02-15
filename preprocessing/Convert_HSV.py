import preprocessing_utils
import dlib
import cv2
import os
import tqdm

dataset_path = "../GeorgiaTechFaces/Crop_1"
maskeddataset_path = "../GeorgiaTechFaces/Maskedcrop_1"
predictor_path = '../shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

X = []
for subject_name in tqdm.tqdm(os.listdir(dataset_path), desc='reading images'):
    if os.path.isdir(os.path.join(dataset_path, subject_name)):
        subject_images_dir = os.path.join(dataset_path, subject_name)
        temp_x_list = []
        for img_name in os.listdir(subject_images_dir):
            # write code to read each 'img'
            if img_name.endswith('.jpg'):
                img_path = os.path.join(subject_images_dir, img_name)
                img = cv2.imread(img_path)
                # add the img to temp_x_list
                temp_x_list.append(img)
        # add the temp_x_list to X
        X.append(temp_x_list)

X_masked = []
for subject_name in tqdm.tqdm(os.listdir(maskeddataset_path), desc='reading images'):
    if os.path.isdir(os.path.join(maskeddataset_path, subject_name)):
        subject_images_dir = os.path.join(maskeddataset_path, subject_name)
        temp_x_list = []
        for img_name in os.listdir(subject_images_dir):
            # write code to read each 'img'
            if img_name.endswith('.jpg'):
                img_path = os.path.join(subject_images_dir, img_name)
                img = cv2.imread(img_path)
                # add the img to temp_x_list
                temp_x_list.append(img)
        # add the temp_x_list to X
        X_masked.append(temp_x_list)

X_ConvertHSV = []
for x_list in tqdm.tqdm(X, desc='convert HSV'):
    temp_X_blured = []
    for x in x_list:
        HSV_face = preprocessing_utils.convert_to_hsv(x)
        temp_X_blured.append(HSV_face)
    X_ConvertHSV.append(temp_X_blured)

X_masked_ConvertHSV = []
for x_list in tqdm.tqdm(X_masked, desc='convert HSV'):
    temp_X_blured = []
    for x in x_list:
        HSV_face = preprocessing_utils.convert_to_hsv(x)
        temp_X_blured.append(HSV_face)
    X_masked_ConvertHSV.append(temp_X_blured)

X_ConvertHSV_dataset_path = '../GeorgiaTechFaces/ConvertHSVprocessedset_1'
for i, subject_images in enumerate(X_ConvertHSV):
    subject_folder = os.path.join(X_ConvertHSV_dataset_path, f"s{str(i + 1).zfill(2)}")
    os.makedirs(subject_folder, exist_ok=True)
    for j, img in enumerate(subject_images):
        cv2.imwrite(os.path.join(subject_folder, f"{str(j + 1).zfill(2)}.jpg"), img)

X_masked_ConvertHSV_dataset_path = '../GeorgiaTechFaces/ConvertHSVMaskprocessedset_1'
for i, subject_images in enumerate(X_masked_ConvertHSV):
    subject_folder = os.path.join(X_masked_ConvertHSV_dataset_path, f"s{str(i + 1).zfill(2)}")
    os.makedirs(subject_folder, exist_ok=True)
    for j, img in enumerate(subject_images):
        cv2.imwrite(os.path.join(subject_folder, f"{str(j + 1).zfill(2)}.jpg"), img)