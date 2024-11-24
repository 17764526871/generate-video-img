import os
import subprocess
import mimetypes
import logging

def is_video_file(filename, video_extensions):
    """
    检查文件是否为视频文件。
    
    参数：
    filename: 文件名
    video_extensions: 支持的视频扩展名列表
    
    返回：
    如果是视频文件则返回 True，否则返回 False。
    """
    # 将扩展名转换为小写进行匹配
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in [ext.lower() for ext in video_extensions]

def get_video_duration(file_path):
    """
    获取视频时长，单位为秒。
    
    参数：
    file_path: 视频文件路径
    
    返回：
    视频时长（秒），如果失败则返回 None。
    """
    try:
        logging.debug(f"正在获取视频文件 {file_path} 的时长...")
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        duration = float(result.stdout.strip())
        logging.info(f"视频文件 {file_path} 的时长为 {duration} 秒。")
        return duration
    except Exception as e:
        logging.error(f"获取视频 {file_path} 时长时出错: {e}")
        return None

def get_capture_delay_time(file_path, capture_mode="smart", fixed_time=60, percentage=0.33):
    """
    获取截取图片的位置，支持智能截取、固定时间截取和按百分比截取。
    
    参数：
    file_path: 视频文件路径
    capture_mode: 截取模式（"smart"，"fixed"，"percentage"）
    fixed_time: 固定时间，单位为秒（用于 "fixed" 模式）
    percentage: 按视频长度的百分比（用于 "percentage" 模式）
    
    返回：
    截取时间点（秒），如果失败则返回 None。
    """
    logging.debug(f"正在获取视频文件 {file_path} 的截取时间点，模式为 {capture_mode}...")
    duration = get_video_duration(file_path)
    if not duration:
        logging.error(f"无法获取视频 {file_path} 的时长，跳过截取时间点计算。")
        return None

    if capture_mode == "fixed":
        capture_time = min(fixed_time, duration)
    elif capture_mode == "percentage":
        capture_time = duration * percentage
    else:  # 默认智能截取模式
        if duration <= 20 * 60:
            capture_time = duration / 3
        else:
            capture_time = min(9 * 60, duration)
    
    logging.info(f"视频文件 {file_path} 的截取时间点为 {capture_time} 秒。")
    return capture_time

def get_file_prefix(file_name):
    """
    获取文件名前缀（例如：my_video.mp4 -> my_video）。
    
    参数：
    file_name: 文件名
    
    返回：
    文件名前缀。
    """
    file_prefix = os.path.splitext(file_name)[0]
    logging.debug(f"获取文件 {file_name} 的前缀为 {file_prefix}。")
    return file_prefix

def count_video_files(directory, video_extensions, recursive=True):
    """
    统计指定目录中的视频文件数量。
    
    参数：
    directory: 要扫描的目录
    video_extensions: 支持的视频扩展名列表
    recursive: 是否递归扫描子目录
    
    返回：
    视频文件的数量。
    """
    video_count = 0
    logging.info(f"开始扫描目录 {directory} 以统计视频文件数量，递归扫描: {recursive}...")
    for dir_path, _, file_names in os.walk(directory):
        if not recursive and dir_path != directory:
            continue
        for name in file_names:
            if is_video_file(name, video_extensions):
                video_count += 1
                logging.debug(f"找到视频文件: {os.path.join(dir_path, name)}")
    logging.info(f"在目录 {directory} 中共找到 {video_count} 个视频文件。")
    return video_count
