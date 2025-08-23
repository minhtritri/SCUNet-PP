import os
import pydicom
import numpy as np
import cv2
from tqdm import tqdm  # Hiển thị tiến trình

# Đường dẫn thư mục gốc chứa các thư mục bệnh nhân
dicom_root = r"/home/vmtri/project/SCUNet-plusplus/dataset_original/CT_scans"  # Thay đường dẫn theo dữ liệu của bạn
output_dir = r"/home/vmtri/project/SCUNet-plusplus/dataset_original/CT_scan_PNG"  # Thư mục lưu PNG

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# Duyệt qua từng thư mục bệnh nhân (PAT001, PAT002, ...)
for patient_folder in tqdm(sorted(os.listdir(dicom_root))):
    patient_path = os.path.join(dicom_root, patient_folder)
    
    # Kiểm tra nếu không phải thư mục thì bỏ qua
    if not os.path.isdir(patient_path):
        continue

    # Tạo thư mục tương ứng trong output
    patient_output_dir = os.path.join(output_dir, patient_folder)
    os.makedirs(patient_output_dir, exist_ok=True)

    # Duyệt qua tất cả file DICOM trong thư mục bệnh nhân
    for dicom_file in sorted(os.listdir(patient_path)):
        if dicom_file.endswith(".dcm"):
            dicom_path = os.path.join(patient_path, dicom_file)
            output_path = os.path.join(patient_output_dir, dicom_file.replace(".dcm", ".png"))

            # Đọc file DICOM
            dicom_data = pydicom.dcmread(dicom_path)
            image_array = dicom_data.pixel_array.astype(np.float32)

            # Chuẩn hóa ảnh (đưa về khoảng 0-255)
            image_array = (image_array - image_array.min()) / (image_array.max() - image_array.min()) * 255.0
            image_array = image_array.astype(np.uint8)  # Chuyển thành kiểu uint8

            # Lưu ảnh PNG
            cv2.imwrite(output_path, image_array)

print("✅ Chuyển đổi DICOM sang PNG hoàn tất!")