import os
import csv
from pydub import AudioSegment

class Trimmer():
    def __init__(self, target_role) -> None:
        self.target_role = target_role
        pass

    def calTime(self, time_str):
        h, m, s = map(float, time_str.split(':'))
        return int((h * 3600 + m * 60 + s) * 1000)


    target_role = "Rem"
    def process_ass_file(self, ass_file, audio_file, output_folder):
        audio_segment = AudioSegment.from_wav(audio_file)
        metadata = []
        prev_role = None
        start_time = None
        end_time = None
        dialogue = ""

        with open(ass_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("Dialogue:"):
                    components = line.split(',')
                    new_start_time = self.calTime(components[1].strip())
                    new_end_time = self.calTime(components[2].strip())
                    role = components[4].strip()
                    new_dialogue = components[9].strip()

                    # 保存前一个对话段（如果有）
                    if prev_role and (role != prev_role or "Comment:" in line):
                        if prev_role == self.target_role:
                            extracted_audio = audio_segment[start_time:end_time]
                            audio_filename = f"{start_time}_{end_time}.wav"
                            audio_path = os.path.join(output_folder, "wavs", audio_filename)
                            extracted_audio.export(audio_path, format="wav")
                            metadata.append(f"{audio_filename}|{dialogue}|{prev_role}")

                        # 重置
                        start_time = None
                        end_time = None
                        dialogue = ""

                    # 更新或设置新的对话段
                    if start_time is None:
                        start_time = new_start_time
                    
                    end_time = new_end_time
                    dialogue += " " + new_dialogue
                    prev_role = role

        # 保存最后一个对话段（如果有）
        if prev_role:
            if prev_role == self.target_role:
                extracted_audio = audio_segment[start_time:end_time]
                audio_filename = f"{start_time}_{end_time}.wav"
                audio_path = os.path.join(output_folder, "wavs", audio_filename)
                extracted_audio.export(audio_path, format="wav")
                metadata.append(f"{audio_filename}|{dialogue}|{prev_role}")

        # 保存元数据
        with open(os.path.join(output_folder, "metadata.csv"), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for entry in metadata:
                writer.writerow([entry])

if __name__ == "__main__":
    
    import glob
    trimmer = Trimmer('Rem')
    for episode in glob.glob("*.mkv"):
        ass_file = episode[:-4] + ".ass"
        audio_file = episode[:-4] + ".wav"
        output_folder = episode[:-4]
        if not os.path.exists(os.path.join(output_folder, "wavs")):
            os.makedirs(os.path.join(output_folder, "wavs"))
        

        trimmer.process_ass_file(ass_file, audio_file, output_folder)
