import argparse
import glob
import os
import subprocess
from moviepy.editor import VideoFileClip
from trim import Trimmer
import shutil
import csv
from tqdm import tqdm

verbose = True
# 提取ASS文件和音频的函数
def extract(episode, subtitle_stream="0:s:2"):
    video = VideoFileClip(episode)
    output_ass_filename = episode[:-4] + ".ass"
    output_wav_filename = episode[:-4] + ".wav"

    if not os.path.exists(output_ass_filename):
        if verbose:
            print(f"Extracting subtitles to {output_ass_filename}...")
        os.system(f'ffmpeg -i  "{episode}" -map {subtitle_stream} "{output_ass_filename}"')
    
    if not os.path.exists(output_wav_filename):
        if verbose:
            print(f"Extracting audio to {output_wav_filename}...")
        audio = video.audio
        audio.write_audiofile(output_wav_filename)
        audio.close()
    video.close()

# 对已有的音频字幕文件提取某个角色的所有音频数据集的函数
def process_ass_file(ass_file, audio_file, output_folder, trimmer:Trimmer):
    if verbose:
        print(f"Processing subtitles and audio for role: {trimmer.target_role}...")
    # 这里假设你已经有了`process_ass_file`的实现
    trimmer.process_ass_file(ass_file, audio_file, output_folder)

# 合并数据集的函数
def merge_datasets(folder_list, output_folder):
    if verbose:
        print("Merging datasets...")
    # 这里假设你已经有了`merge_datasets`的实现
        # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 创建wavs文件夹
    wavs_output_folder = os.path.join(output_folder, "wavs")
    if not os.path.exists(wavs_output_folder):
        os.makedirs(wavs_output_folder)

    # 合并metadata
    with open(os.path.join(output_folder, 'metadata.csv'), 'w', encoding='utf-8', newline='') as out_csv:
        
        with open(os.path.join(output_folder, 'metadata.csv'), 'w', encoding='utf-8', newline='') as out_csv:
            writer = csv.writer(out_csv, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for folder in folder_list:
                episode_num = folder.split('-')[-1]  # 获取集数作为前缀
                metadata_file = os.path.join(folder, 'metadata.csv')
                wavs_folder = os.path.join(folder, 'wavs')

                # 拷贝wavs到统一文件夹
                for wav_file in os.listdir(wavs_folder):
                    new_wav_name = f"{episode_num}_{wav_file}"
                    shutil.copy(os.path.join(wavs_folder, wav_file), os.path.join(wavs_output_folder, new_wav_name))

                # 合并metadata
                with open(metadata_file, 'r', encoding='utf-8') as in_csv:
                    with open(metadata_file, 'r', encoding='utf-8') as in_csv:
                        reader = csv.reader(in_csv, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for row in reader:
                            row[0] = f"{episode_num}_{row[0]}"
                            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio dataset from anime episodes.")
    parser.add_argument("--input_dir", type=str, help="Directory containing MKV files.")
    parser.add_argument("--output_dir", type=str, default='./output', help="Directory to save output datasets.")
    parser.add_argument("--target_role", type=str,  help="Target role to extract audio.")
    parser.add_argument("--subtitle", type=str, default='0:s:2',  help="the stream of the subtitle")
    parser.add_argument("--verbose", type=bool,  help="whether to verbose the process")

    args = parser.parse_args()

    verbose = args.verbose
    output_dir = os.path.abspath(args.output_dir)
    os.chdir(args.input_dir)
   
    trimmer = Trimmer(args.target_role)
    episode_list = glob.glob("*.mkv")

    output_folders = []
    for episode in tqdm(episode_list, desc="processing"):
        extract(episode, args.subtitle)

        ass_file = episode[:-4] + ".ass"
        audio_file = episode[:-4] + ".wav"
        output_folder = os.path.join(output_dir, episode[:-4])

        if not os.path.exists(os.path.join(output_folder, "wavs")):
            os.makedirs(os.path.join(output_folder, "wavs"))

        process_ass_file(ass_file, audio_file, output_folder, trimmer)
        output_folders += [output_folder]

    folder_list = output_folders
    merge_datasets(folder_list, output_dir)
    print("Dataset extraction complete. 🌟")
