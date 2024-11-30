# 视频缩略图生成器 - 依赖管理指南

## 介绍

此项目用于从视频中截取缩略图，支持多种配置以满足不同的需求，包括自定义输出目录、缩略图格式、视频处理并行度等。本文档为项目的依赖管理和运行指南。

## 环境要求

- Python 3.6 或更高版本
- Windows、Linux 或 macOS

## 依赖管理

该项目依赖多个 Python 库，需要使用 `pip` 安装这些库。建议使用虚拟环境来隔离项目的依赖关系。

### 创建虚拟环境

首先，在项目目录下创建并激活虚拟环境：

```sh
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 安装依赖

在激活虚拟环境后，您可以通过以下命令安装所有依赖：

```sh
pip install -r requirements.txt
```

### `requirements.txt` 文件内容

以下是项目的主要依赖项，您可以在 `requirements.txt` 文件中包含如下内容：

```
configparser==5.0.2
tqdm
```

### 主要依赖项说明

- **configparser**：用于加载配置文件 (`config.ini`) 并读取相关参数。
- **tqdm**：用于显示任务进度条，改善用户体验。

## 项目结构

项目采用模块化结构，每个功能模块都有独立的文件夹和模块，以便于管理和维护。主要的文件和目录结构如下：

```
project_root/
  |- src/
      |- main.py                # 项目的主入口脚本
      |- config_loader.py       # 配置加载模块
      |- file_list_generator/   # 文件列表生成模块
          |- file_list_generator_module.py
      |- logging_setup/         # 日志设置模块
          |- logging_setup_module.py
      |- thumbnail_generator/   # 缩略图生成模块
          |- thumbnail_generator_module.py
      |- video_utils.py         # 视频处理工具模块
  |- config/
      |- config.ini             # 配置文件
  |- requirements.txt           # 依赖文件
  |- README.md                  # 说明文档
```

## 运行说明

### 配置文件

项目中的 `config/config.ini` 用于自定义配置，包括：

- **General 配置**：文件路径、是否递归查找等。
- **Thumbnail 配置**：缩略图参数如格式、质量、是否覆盖等。
- **Logging 配置**：日志的级别和输出目录。
- **Performance 配置**：是否使用 GPU 和并行处理的工作线程数。

请确保在运行前，配置文件 (`config.ini`) 已正确设置。

### 运行程序

激活虚拟环境后，可以通过以下命令运行程序：

```sh
python src/main.py
```

如果需要查看命令行的参数帮助，可以使用：

```sh
python src/main.py --help
```

## 打包为可执行文件

为了方便在没有 Python 环境的机器上运行，可以使用 `PyInstaller` 将程序打包为 Windows 可执行文件。

### 打包步骤

1. 首先，确保已安装 `PyInstaller`，如果未安装，请运行以下命令进行安装：

    ```sh
    pip install pyinstaller
    ```

2. 使用以下命令将程序打包为一个可执行文件：

    ```sh
    pyinstaller --onefile --name video_thumbnail_generator --console src/main.py
    ```

3. 配置文件 `config.ini` 应该放在与可执行文件相同的目录中，或者指定在外部可访问的位置。

4. 打包后生成的可执行文件将位于 `dist` 文件夹中。

5. 运行打包后的程序时，请确保 `config.ini` 配置文件与可执行文件位于同一目录，或者通过命令行参数指定配置文件的路径。

### 注意事项

- 如果 `pyinstaller` 命令无法识别，请确保已激活虚拟环境，并且 Python 脚本的路径已正确配置。
- 运行以下命令检查 PyInstaller 是否安装成功：

    ```sh
    pyinstaller --version
    ```

- 在 `Windows` 上，可能需要以管理员身份运行命令提示符，来确保打包过程中的权限。

## 日志

程序运行期间会生成日志文件，默认保存在 `log` 文件夹中。日志级别可以在配置文件或运行时通过命令行参数设置。

## 贡献

欢迎对该项目进行贡献。您可以提出 Issue 或 Pull Request，以帮助我们改进代码和文档。

