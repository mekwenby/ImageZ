from PIL import Image
import os
import shutil
import multiprocessing


def compress_and_copy_jpg_file(input_file_path, output_file_path, target_size):
    # 设置最大像素
    Image.MAX_IMAGE_PIXELS = 1000000000
    # 打开图片
    image = Image.open(input_file_path)

    # 获取原始图片大小
    original_size = os.path.getsize(input_file_path)

    # 获取目录路径
    output_dir = os.path.dirname(output_file_path)

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 如果图片大小已经小于目标大小，无需压缩
    if original_size <= target_size:
        image.save(output_file_path)
        return

    # 计算压缩质量
    quality = 95
    while original_size > target_size and quality > 0:
        image.save(output_file_path, format='webp', quality=quality)
        quality -= 5
        compressed_size = os.path.getsize(output_file_path)
        original_size = compressed_size


def process_file(file_info):
    input_file, output_file, target_size = file_info
    output_file = output_file.replace('.jpg', '.webp')
    compress_and_copy_jpg_file(input_file, output_file, target_size)
    print(f"处理文件: {input_file}，压缩后保存到 {output_file}")


def main(input_dir, output_dir, target_size):
    files_to_process = []

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录下的所有文件和子目录
    for root, _, files in os.walk(input_dir):
        for file in files:
            # 检查文件扩展名是否为.jpg
            if file.lower().endswith('.jpg'):
                input_file_path = os.path.join(root, file)
                # 构建输出文件路径，保留相对目录结构
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)
                files_to_process.append((input_file_path, output_file_path, target_size))

    # 使用进程池并行处理文件
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_file, files_to_process)

    pool.close()
    pool.join()


if __name__ == "__main__":
    '''todo'''
    input_dir = "input_directory"  # 输入目录的路径
    output_dir = "output_directory"  # 输出目录的路径
    # 目标大小 1024 * 1024 = 1MB
    target_size = 1024 * 1524
    ''''''''''''''''''
    main(input_dir, output_dir, target_size)
