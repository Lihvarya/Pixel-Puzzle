# p_robust_final.py

from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import os


def generate_all_versions_robust(input_directory, output_base_filename="restored.png", enhance=True, sharpen_radius=1.5,
                                 sharpen_percent=150, contrast_factor=1.1):
    """
    无损拼接图片，并生成三个版本：原图、反色图和增强图。
    此版本极为健壮，能自动处理：
    - 黑白混合背景
    - 不同的图像模式 (如 RGB, P)
    - 1-2像素的微小尺寸差异

    Args:
        input_directory (str): 包含子图片的目录路径。
        output_base_filename (str): 输出图片的基础文件名。
        enhance (bool): 是否生成增强版本。
        sharpen_radius (float): 锐化半径。
        sharpen_percent (int): 锐化强度。
        contrast_factor (float): 对比度增强因子。
    """
    image_files = []
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_files.append(os.path.join(input_directory, filename))

    if not image_files:
        print(f"在目录 '{input_directory}' 中没有找到任何图片文件。")
        return

    # --- 1. 初始化 ---
    try:
        # 以第一张图片为模板获取基准尺寸
        with Image.open(image_files[0]) as img:
            base_width, base_height = img.size

        base_mode = 'RGB'
        restored_image = Image.new(base_mode, (base_width, base_height), (0, 0, 0))

    except Exception as e:
        print(f"无法打开或读取第一张图片 '{image_files[0]}' 的信息：{e}")
        return

    print(f"找到 {len(image_files)} 张子图片，基准尺寸为 {base_width}x{base_height}，处理模式为 {base_mode}。")
    print("开始无损拼接图片（自动处理尺寸差异）...")

    restored_pixels = restored_image.load()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # --- 2. 遍历并合并像素 ---
    for i, img_path in enumerate(image_files):
        try:
            with Image.open(img_path) as current_img:
                # 关键修改：处理尺寸不一致的图片
                if current_img.size != (base_width, base_height):
                    print(
                        f"\n警告：图片 '{os.path.basename(img_path)}' 尺寸 {current_img.size} 与基准不符，将自动调整尺寸至 {(base_width, base_height)}。")
                    # 使用高质量的LANCZOS算法进行重采样
                    current_img = current_img.resize((base_width, base_height), Image.Resampling.LANCZOS)

                # 统一转换为RGB模式进行处理
                if current_img.mode != base_mode:
                    current_img = current_img.convert(base_mode)

                print(f"正在处理第 {i + 1}/{len(image_files)} 张图片: {os.path.basename(img_path)}", end='\r')

                current_pixels = current_img.load()

                for y in range(base_height):
                    for x in range(base_width):
                        pixel_color = current_pixels[x, y]
                        if pixel_color != BLACK and pixel_color != WHITE:
                            restored_pixels[x, y] = pixel_color

        except Exception as e:
            print(f"\n处理图片 '{os.path.basename(img_path)}' 时发生错误：{e}")
            continue

    print("\n图片拼接完成。现在开始生成并保存各个版本...")

    # --- 3. 保存原图和反色图 ---
    name, ext = os.path.splitext(output_base_filename)
    try:
        output_restored_filename = f"{name}_原图{ext}"
        restored_image.save(output_restored_filename)
        print(f"✅ 原图已成功还原并保存为 '{output_restored_filename}'")
    except Exception as e:
        print(f"❌ 保存原图时发生错误：{e}")
        return

    try:
        inverted_image = ImageOps.invert(restored_image)
        output_inverted_filename = f"{name}_反色{ext}"
        inverted_image.save(output_inverted_filename)
        print(f"✅ 反色图已成功生成并保存为 '{output_inverted_filename}'")
    except Exception as e:
        print(f"❌ 生成或保存反色图时发生错误：{e}")

    # --- 4. 生成并保存增强版图片 ---
    if enhance:
        try:
            print("正在生成增强版图片（锐化+对比度）...")
            # ... (这部分逻辑不变) ...
            enhanced_image = restored_image.filter(
                ImageFilter.UnsharpMask(radius=sharpen_radius, percent=sharpen_percent, threshold=3))
            enhancer = ImageEnhance.Contrast(enhanced_image)
            enhanced_image = enhancer.enhance(contrast_factor)
            output_enhanced_filename = f"{name}_增强{ext}"
            enhanced_image.save(output_enhanced_filename)
            print(f"✅ 增强图已成功生成并保存为 '{output_enhanced_filename}'")
        except Exception as e:
            print(f"❌ 生成或保存增强图时发生错误：{e}")


# --- 示例用法 ---
if __name__ == "__main__":
    input_folder = 'sub_images'
    output_base_file = 'image.png'

    generate_all_versions_robust(
        input_folder,
        output_base_file,
        enhance=True,
        sharpen_radius=1.5,
        sharpen_percent=150,
        contrast_factor=1.1
    )