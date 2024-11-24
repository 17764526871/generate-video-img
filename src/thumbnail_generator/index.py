import os
import subprocess
import logging
from ..video_utils.index import get_capture_delay_time, get_file_prefix

def make_thumb(file_info, args, total_tasks):
    """
    使用 ffmpeg 截取视频缩略图。

    参数：
    file_info: 文件信息，包含目录路径、文件名和任务索引。
    args: 命令行参数。
    total_tasks: 任务总数，用于日志记录。
    """
    dir_path, name, task_index = file_info
    logging.info(f"[{task_index}/{total_tasks}] 开始处理文件: {name}")
    
    video_full_path = os.path.join(dir_path, name)
    video_name_prefix = get_file_prefix(name)

    # 输出目录设置
    thumb_dir = args.output_dir if args.output_dir else dir_path
    os.makedirs(thumb_dir, exist_ok=True)

    # 如果提供了自定义缩略图名称
    if args.custom_name:
        if args.append_suffix:
            thumb_name = f"{video_name_prefix}_{args.custom_name}.{args.thumb_format}"
        else:
            thumb_name = f"{args.custom_name}.{args.thumb_format}"
    else:
        thumb_name = f"{video_name_prefix}.{args.thumb_format}"

    thumb_full_path = os.path.join(thumb_dir, thumb_name)

    # 检查是否需要覆盖
    if not args.overwrite and os.path.exists(thumb_full_path):
        logging.info(f"[{task_index}/{total_tasks}] 缩略图 {thumb_full_path} 已存在，跳过。")
        return

    delay_time = get_capture_delay_time(video_full_path, args.capture_mode, args.fixed_time, args.percentage)
    if delay_time is None:
        logging.error(f"[{task_index}/{total_tasks}] 获取 {video_full_path} 截取时间失败，跳过。")
        return

    command = [
        "ffmpeg"
    ]

    if args.use_gpu:
        command.extend(["-hwaccel", "cuda"])

    command.extend([
        "-i", video_full_path,
        "-y", "-ss", str(delay_time), "-frames:v", "1", thumb_full_path
    ])

    if args.thumb_format in ["jpg", "jpeg"]:
        command.extend(["-q:v", str(args.thumb_quality)])

    if args.thumb_resolution:
        command.extend(["-vf", f"scale={args.thumb_resolution}"])

    if args.watermark:
        command.extend(["-vf", f"drawtext=text='{args.watermark}':fontcolor=white:fontsize=24:x=10:y=10"])

    logging.debug(f"[{task_index}/{total_tasks}] 执行命令: {' '.join(command)}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            logging.error(f"[{task_index}/{total_tasks}] FFmpeg命令执行失败: {result.stderr}")
        elif not os.path.exists(thumb_full_path):
            logging.error(f"[{task_index}/{total_tasks}] 缩略图文件未生成: {thumb_full_path}")
        else:
            logging.info(f"[{task_index}/{total_tasks}] 视频 {video_full_path} 的缩略图已保存为 {thumb_full_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"[{task_index}/{total_tasks}] 生成缩略图时出错: {e}")
