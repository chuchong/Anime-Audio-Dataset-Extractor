
# Anime Audio Dataset Extractor

## Description

This Python script is designed to extract audio and subtitle data from anime episodes in MKV format. It also processes the subtitles to extract audio corresponding to a specific role and merges the datasets generated from multiple episodes.

## Requirements

- Python 3.x
- moviepy
- tqdm
- FFmpeg

## Installation

1. Clone the repository.
    ```
    git clone <repo_url>
    ```
2. Change directory into the project folder.
    ```
    cd <project_folder>
    ```
3. Install the required packages.
    ```
    pip install -r requirements.txt
    ```

## Usage

Run the script with the following command:

```
python main.py --input_dir=<input_directory> --output_dir=<output_directory> --target_role=<role_to_extract> --subtitle=<subtitle_stream> --verbose=<verbose>
```

### Parameters

- `--input_dir`: Directory containing MKV files.
- `--output_dir`: Directory to save the output datasets (default is `./output`).
- `--target_role`: The role whose audio you want to extract.
- `--subtitle`: The stream of the subtitle (default is `0:s:2`).
- `--verbose`: Whether to verbose the process (default is `True`).

## How it Works

1. **Extract**: Uses FFmpeg to extract subtitle (ASS format) and audio (WAV format) from each episode.
2. **Process**: Processes the subtitle and audio files to extract clips corresponding to the target role.
3. **Merge**: Merges datasets from different episodes into one.

---

# 动漫音频数据集提取器

## 描述

这个Python脚本用于从MKV格式的动漫剧集中提取音频和字幕数据。它还会处理字幕以提取与特定角色对应的音频，并将从多个剧集生成的数据集合并。

## 环境要求

- Python 3.x
- moviepy
- tqdm
- FFmpeg

## 安装

1. 克隆仓库。
    ```
    git clone <仓库_url>
    ```
2. 进入项目文件夹。
    ```
    cd <项目文件夹>
    ```
3. 安装所需的包。
    ```
    pip install -r requirements.txt
    ```

## 使用方法

运行以下命令：

```
python main.py --input_dir=<输入目录> --output_dir=<输出目录> --target_role=<要提取的角色> --subtitle=<字幕流> --verbose=<是否输出详细信息>
```

### 参数

- `--input_dir`: 包含MKV文件的目录。
- `--output_dir`: 用于保存输出数据集的目录（默认为`./output`）。
- `--target_role`: 要提取的角色的音频。
- `--subtitle`: 字幕流（默认为`0:s:2`）。
- `--verbose`: 是否输出详细信息（默认为`True`）。

## 工作原理

1. **提取**: 使用FFmpeg从每个剧集中提取字幕（ASS格式）和音频（WAV格式）。
2. **处理**: 处理字幕和音频文件，以提取与目标角色对应的片段。
3. **合并**: 将不同剧集的数据集合并为一个。

---
