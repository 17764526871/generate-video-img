import os
import sys
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from tqdm import tqdm

# 添加模块路径到系统路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.config_loader import load_config
from src.file_list_generator.index import generate_file_list
from src.logging_setup.index import setup_logging
from src.thumbnail_generator.index import make_thumb
from src.video_utils.index import is_video_file, get_video_duration, get_capture_delay_time, get_file_prefix

# 加载配置文件
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
config = load_config(config_path)

# General 配置
file_path = config.get('General', 'file_path', fallback=os.getcwd())
recursive = config.getboolean('General', 'recursive', fallback=False)

# Thumbnail 配置
custom_name = config.get('Thumbnail', 'custom_name', fallback=None)
append_suffix = config.getboolean('Thumbnail', 'append_suffix', fallback=False)
overwrite = config.getboolean('Thumbnail', 'overwrite', fallback=False)
capture_mode = config.get('Thumbnail', 'capture_mode', fallback='smart')
fixed_time = config.getint('Thumbnail', 'fixed_time', fallback=60)
percentage = config.getfloat('Thumbnail', 'percentage', fallback=0.33)
output_dir = config.get('Thumbnail', 'output_dir', fallback=None)
thumb_format = config.get('Thumbnail', 'thumb_format', fallback='jpg')
thumb_quality = config.getint('Thumbnail', 'thumb_quality', fallback=2)
thumb_resolution = config.get('Thumbnail', 'thumb_resolution', fallback=None)
watermark = config.get('Thumbnail', 'watermark', fallback=None)

# Video 配置
video_extensions = config.get('Video', 'video_extensions', fallback='.mp4,.avi,.mkv,.mov,.flv').split(',')

# Logging 配置
log_level = config.get('Logging', 'log_level', fallback='INFO')
log_dir = config.get('Logging', 'log_dir', fallback='log')

# Performance 配置
use_gpu = config.getboolean('Performance', 'use_gpu', fallback=False)
try:
    max_workers = config.getint('Performance', 'max_workers')
except (ValueError, TypeError):
    max_workers = multiprocessing.cpu_count()

# 主函数
def main():
    parser = argparse.ArgumentParser(description="视频缩略图生成器")
    parser.add_argument("--file_path", type=str, default=file_path, help="要生成缩略图的视频所在路径（默认为当前执行文件夹）")
    parser.add_argument("--custom_name", type=str, default=custom_name, help="自定义缩略图名称")
    parser.add_argument("--append_suffix", action="store_true", default=append_suffix, help="在原文件名后增加自定义后缀")
    parser.add_argument("--overwrite", action="store_true", default=overwrite, help="覆盖已存在的缩略图")
    parser.add_argument("--capture_mode", type=str, choices=["smart", "fixed", "percentage"], default=capture_mode, help="截取模式")
    parser.add_argument("--fixed_time", type=int, default=fixed_time, help="固定时间截取，单位为秒（用于 'fixed' 模式）")
    parser.add_argument("--percentage", type=float, default=percentage, help="按视频长度的百分比截取（用于 'percentage' 模式）")
    parser.add_argument("--output_dir", type=str, default=output_dir, help="缩略图输出目录")
    parser.add_argument("--thumb_format", type=str, choices=["jpg", "png", "webp"], default=thumb_format, help="缩略图格式")
    parser.add_argument("--thumb_quality", type=int, default=thumb_quality, help="缩略图质量（1-31，数字越小质量越高，仅适用于 jpg 格式）")
    parser.add_argument("--use_gpu", action="store_true", default=use_gpu, help="是否使用 GPU 加速")
    parser.add_argument("--log_level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default=log_level, help="日志级别")
    parser.add_argument("--video_extensions", type=str, nargs='+', default=video_extensions, help="支持的视频文件类型列表")
    parser.add_argument("--thumb_resolution", type=str, default=thumb_resolution, help="缩略图的分辨率（例如 320x240）")
    parser.add_argument("--watermark", type=str, default=watermark, help="添加到缩略图的水印文字")
    parser.add_argument("--recursive", action="store_true", default=recursive, help="是否递归处理子目录中的视频文件")
    parser.add_argument("--max_workers", type=int, default=max_workers, help="并行处理的最大工作线程数（默认等于CPU核心数）")
    args = parser.parse_args()

    # 设置日志级别
    setup_logging(log_dir, args.log_level)
    logging.getLogger().setLevel(args.log_level)

    # 计算任务总数并生成文件列表
    logging.info(f"开始扫描文件路径: {args.file_path} (递归: {'是' if args.recursive else '否'})")
    file_list = generate_file_list(args)
    total_tasks = len(file_list)

    if total_tasks == 0:
        logging.warning("未找到任何符合条件的视频文件。")
        logging.info("未找到任何符合条件的视频文件。请检查文件路径和文件类型配置。")
    else:
        logging.info(f"找到 {total_tasks} 个视频文件。开始生成缩略图...")

    # 并行生成缩略图，使用进度条显示
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(make_thumb, file_info, args, total_tasks): file_info for file_info in file_list}
        with tqdm(total=total_tasks, desc="生成缩略图进度", dynamic_ncols=True, leave=True) as pbar:
            for future in as_completed(futures):
                try:
                    future.result()  # 捕获可能的异常
                    pbar.update(1)
                except Exception as e:
                    logging.error(f"处理文件 {futures[future]} 时出错: {e}")
                    pbar.update(1)

if __name__ == "__main__":
    main()
