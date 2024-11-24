import os
import logging
from tqdm import tqdm
from ..video_utils.index import is_video_file

def generate_file_list(args):
    """
    生成需要处理的视频文件列表。

    参数：
    args: 命令行参数。

    返回：
    包含所有符合条件的视频文件信息的列表。
    """
    file_list = []
    logging.info(f"开始扫描文件路径: {args.file_path} (递归: {'是' if args.recursive else '否'})")
    
    try:
        # 使用 tqdm 显示进度条
        for dir_path, _, file_names in tqdm(os.walk(args.file_path), desc="扫描文件夹中"):
            # 如果不递归处理子目录且当前路径不是起始路径，则跳过
            if not args.recursive and dir_path != args.file_path:
                continue
            for index, name in enumerate(file_names):
                if is_video_file(name, args.video_extensions):
                    file_list.append((dir_path, name, len(file_list) + 1))
    except PermissionError as e:
        logging.error(f"权限错误，无法访问目录: {e}")
    except Exception as e:
        logging.error(f"扫描文件夹时发生错误: {e}")

    total_files = len(file_list)
    if total_files > 0:
        logging.info(f"共找到 {total_files} 个视频文件。")
    else:
        logging.warning("未找到任何符合条件的视频文件。")

    return file_list
