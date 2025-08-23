import os
import numpy as np
import scipy.io
import cv2
from tqdm import tqdm

# Thư mục chứa các file .mat (Ground Truth)
mat_root = r"/home/vmtri/project/SCUNet-plusplus/dataset_original/GroudTruth"  # Thay bằng đường dẫn của bạn
output_dir = r"/home/vmtri/project/SCUNet-plusplus/dataset_original/GroundTruth_PNG"  # Thư mục lưu ảnh PNG

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# Biến đếm tổng số ảnh để đặt tên theo format Dxxxx.png


# Duyệt qua tất cả các file .mat trong thư mục GroundTruth
for mat_file in tqdm(sorted(os.listdir(mat_root))):
    if mat_file.endswith(".mat"):
        mat_path = os.path.join(mat_root, mat_file)

        # Lấy tên thư mục bệnh nhân (PAT001, PAT002, ...)
        patient_id = mat_file.replace(".mat", "")
        patient_output_dir = os.path.join(output_dir, patient_id)
        os.makedirs(patient_output_dir, exist_ok=True)  # Tạo thư mục cho bệnh nhân nếu chưa có

        # Đọc file .mat
        mat_data = scipy.io.loadmat(mat_path)

        # Tìm mask (giả sử chỉ có 1 biến dạng NumPy array trong file .mat)
        mask = None
        for key in mat_data:
            if isinstance(mat_data[key], np.ndarray):  # Lấy mảng NumPy đầu tiên
                mask = mat_data[key]
                break  

        if mask is None:
            print(f"⚠️ Không tìm thấy mask trong {mat_file}, bỏ qua!")
            continue

        # Kiểm tra số chiều của mask
        if len(mask.shape) == 2:  # Ảnh 2D (H, W)
            slices = [mask]  # Lưu vào danh sách để xử lý đồng bộ
        elif len(mask.shape) == 3:  # Ảnh 3D (H, W, D)
            slices = [mask[:, :, i] for i in range(mask.shape[2])]  # Tách từng slice
        else:
            print(f"⚠️ Dữ liệu {mat_file} có shape {mask.shape} không hợp lệ, bỏ qua!")
            continue

        # Biến đếm cho mỗi bệnh nhân
        image_counter = 1

        # Lưu từng slice thành PNG trong thư mục bệnh nhân
        for slice_mask in slices:
            # 🛠 Chuyển về uint8 (0-255)
            slice_mask = slice_mask.astype(np.float32)
            slice_mask = (slice_mask - slice_mask.min()) / (slice_mask.max() - slice_mask.min()) * 255  # Chuẩn hóa
            slice_mask = slice_mask.astype(np.uint8)

            # Định dạng tên file: D0001.png, D0002.png, ..., D9999.png
            output_filename = f"D{image_counter:04d}.png"
            output_path = os.path.join(patient_output_dir, output_filename)

            # Lưu ảnh PNG
            cv2.imwrite(output_path, slice_mask)

            # Tăng biến đếm
            image_counter += 1  

print("✅ Chuyển đổi GroundTruth từ .mat sang nhiều PNG hoàn tất!")
