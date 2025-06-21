# Image Slice Restorer & Enhancer (图像切片还原与增强工具)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

一个功能强大的 Python 脚本，用于将一个目录下的多个图像“切片”或“碎片”无损地拼接还原成完整的原始图像。该脚本具有极高的鲁棒性，能够自动处理多种常见问题，并提供图像增强选项。

This is a powerful Python script designed to losslessly restore a complete, original image from a directory of image "slices" or "fragments." The script is highly robust, automatically handling a variety of common issues and providing options for post-enhancement.

## ✨ 功能特性 (Features)

-   **无损拼接 (Lossless Restoration)**: 通过像素级替换，100% 还原原始图像的每一个细节，无任何质量损失。
-   **鲁棒性强 (Highly Robust)**:
    -   **处理混合背景**: 能够正确处理背景为纯黑 (`#000000`) 或纯白 (`#FFFFFF`) 的混合切片。
    -   **自动模式转换**: 自动将不同模式（如 `P` 模式/调色板模式）的图片统一转换为 `RGB` 模式进行处理。
    -   **自动尺寸校正**: 能够自动处理有 1-2 像素微小尺寸差异的图片，将其高质量地调整为基准尺寸，而不会跳过。
-   **多种输出 (Multiple Outputs)**: 一次运行，生成三个有用的图像版本：
    1.  **还原图 (`_restored.png`)**: 完美拼接的原始图像。
    2.  **反色图 (`_inverted.png`)**: 还原图的反色版本。
    3.  **增强图 (`_enhanced.png`)**: 对还原图进行锐化和对比度增强，使其在视觉上更清晰。
-   **易于配置 (Easy to Configure)**: 增强效果（锐化度、对比度等）的参数可以在脚本中轻松调整。

## 🔧 环境要求 (Prerequisites)

-   Python 3.7 或更高版本
-   Pillow (Python Imaging Library)



## 🚀 使用方法 (Usage)

1.  **准备文件结构**

    将您的所有图像切片文件放入一个文件夹（例如 `sub_images`）。然后将主脚本 `p_robust_final.py` 放在该文件夹的外部。

    ```
    my_project/
    ├── p.py       # <-- 主脚本
    └── sub_images/             # <-- 存放图像切片的文件夹
        ├── slice_1.png
        ├── slice_2.png
        ├── slice_3.png
        └── ...
    ```

2.  **配置脚本参数**

    打开 `p.py` 文件，找到文件底部的 `if __name__ == "__main__":` 部分。您可以根据需要修改以下参数：

    ```python
    if __name__ == "__main__":
        # 输入文件夹：包含图像切片的目录
        input_folder = 'sub_images'
        
        # 输出文件的基础名称，脚本会自动添加后缀
        output_base_file = 'my_final_image.png'

        # --- 增强选项 ---
        generate_all_versions_robust(
            input_folder,
            output_base_file,
            enhance=True,  # 设置为 False 可以跳过生成增强图
            
            # 锐化半径：影响锐化的范围，建议 1.0-2.0
            sharpen_radius=1.5,
            
            # 锐化强度：百分比，建议 100-200
            sharpen_percent=150,
            
            # 对比度因子：大于1.0增强，1.0为不变
            contrast_factor=1.1
        )
    ```

3.  **运行脚本**

    在您的终端或命令行中，导航到项目目录并运行脚本：

    ```bash
    python p.py
    ```

## 🖼️ 输出结果 (Output)

脚本运行成功后，您将在项目根目录下看到生成的新文件：

-   `image_restored.png`: 无损还原的原始图像。
-   `image_inverted.png`: 原图的反色版本。
-   `image_enhanced.png`: 经过锐化和对比度增强的版本，视觉上更清晰。

## 🔬 工作原理 (How It Works)

1.  **初始化**: 脚本首先读取第一张图片以确定基准尺寸，然后创建一个与基准尺寸相同的纯黑色画布。
2.  **遍历与标准化**: 脚本会遍历输入目录中的每一张图片。
    -   它会检查每张图片的尺寸，如果与基准尺寸有微小差异，则自动将其调整为基准尺寸。
    -   它会将每张图片的模式统一转换为 `RGB` 模式，以确保兼容性。
3.  **像素级拼接**: 对于当前图片中的每一个像素，脚本会判断其颜色。**只有当像素颜色既不是纯黑也不是纯白时**，才将其视为有效内容，并复制到画布的相应位置上。
4.  **后处理与保存**: 拼接完成后，脚本会基于最终的画布生成并保存还原图、反色图和（可选的）增强图。

## 📄 许可证 (License)

本项目采用 [Apache-2.0 license](LICENSE.md) 授权。

---
