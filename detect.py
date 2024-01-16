import paddle
import paddle.fluid as fluid
import numpy as np
import hashlib
import os
import subprocess
import sys
paddle.enable_static()
class_detail = [{'class_name': 'zhaoliying', 'class_label': 0, 'class_test_images': 11, 'class_trainer_images': 94}, {'class_name': 'baijingting', 'class_label': 1, 'class_test_images': 11, 'class_trainer_images': 93}, {'class_name': 'jiangwen', 'class_label': 2, 'class_test_images': 11, 'class_trainer_images': 92}, {'class_name': 'pengyuyan', 'class_label': 3, 'class_test_images': 12, 'class_trainer_images': 102}, {'class_name': 'zhangziyi', 'class_label': 4, 'class_test_images': 10, 'class_trainer_images': 90}, {'class_name': 'zhaoliangchen', 'class_label': 5, 'class_test_images': 11, 'class_trainer_images': 93}]

# Function to load and preprocess the image
def load_image(path):
    img = paddle.dataset.image.load_and_transform(path, 100, 100, False).astype('float32')
    img = img / 255.0 
    return img

def compress_file(path, password, username):
    hashed_password = hashlib.sha256((username + password).encode('utf-8')).hexdigest()
    
    rar_filename = path + "_" + username + ".rar"
    
    if os.path.isdir(path):
        # Compress folder
        subprocess.run(["C:\Program Files\WinRAR\WinRAR.exe", 'a', '-p' + hashed_password, rar_filename, path])
    elif os.path.isfile(path):
        # Compress file
        subprocess.run(["C:\Program Files\WinRAR\WinRAR.exe", 'a', '-p' + hashed_password, rar_filename, path])
    else:
        print(f"Unable to find the specified path: {path}")

    return rar_filename




# Function to perform image recognition and prediction
def perform_image_recognition(username, image_path):
    infer_imgs = [load_image(image_path)]

    # Set up the inference environment
    place = fluid.CPUPlace()
    infer_exe = fluid.Executor(place)
    inference_scope = fluid.core.Scope()

    # Load the pre-trained model
    params_dirname ='model'
    with fluid.scope_guard(inference_scope):
        [inference_program, feed_target_names, fetch_targets] = fluid.io.load_inference_model(params_dirname, infer_exe)
        
        # Run the inference
        results = infer_exe.run(
            inference_program,
            feed={feed_target_names[0]: infer_imgs},
            fetch_list=fetch_targets
        )

    # Compare the result with the provided username
    predicted_class_index = (np.argmax(results[0])+5)%6
    predicted_username = class_detail[predicted_class_index]['class_name']
    result = predicted_username == username
    return result

    # If the result is True, compress the file and set the password
def extract_file(rar_path,  username, password):
    # Generate hashed password
    hashed_password = hashlib.sha256((username + password).encode('utf-8')).hexdigest()
    output_dir = os.path.dirname(rar_path)
    # Construct the output file path
    output_path = output_dir

    # Check if the RAR file exists
    if os.path.exists(rar_path):
        # Extract the file
        subprocess.run(["C:\Program Files\WinRAR\WinRAR.exe", 'x', '-p' + hashed_password, rar_path, output_path])
        print(f"Extraction succeeded. Extracted files saved to: {output_path}")
    else:
        print(f"Unable to find the specified RAR file: {rar_path}")
    return output_path

# Get user input
username = sys.argv[1]
image_path = sys.argv[2]
file_path = sys.argv[3]
password = sys.argv[4]
option = sys.argv[5]
if perform_image_recognition(username, image_path):
   if int(option)==1:
        compressed_filename = compress_file(file_path, password,username)
        print("Zip succeed. Compressed file:", compressed_filename)

   elif int(option)==2:
    compressed_filename = extract_file(file_path, username,password)
    print("Zip succeed. Compressed file:", compressed_filename)

   else:
      print('输入错误')
else :
    print('非本人操作')