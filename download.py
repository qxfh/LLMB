import os 
import json
from crawling.func import download_image_from_xml
from pathlib import Path
import re


xml_folder = Path('/home/tmp/')
image_folder= Path('/home/image/')

def process_files_in_directory(image_folder):
    for xml in list(xml_folder.glob('*')):
        print(xml)
        directory = image_folder / Path(xml).stem
        with open(os.path.join(directory, 'metadata.json'), 'r') as f:
            metadatas = json.load(f)  # 여러 metadata로 변경
        captions = []
        for metadata in metadatas:  # 각 metadata에 대해 반복
            # 이미지 파일 이름 변경
            label = metadata.get('label', '')
            numbers_from_label = re.findall(r'\d+', label)  # 숫자만 모두 찾습니다.
            index = ''.join(numbers_from_label)  # 숫자들을 연결하여 인덱스로 사용합니다.

            locator = metadata.get('locator')
            match = re.search(r'(\d+)', locator)
            if not index and match:
                index = match.group(0)

            jpeg_filepath = os.path.join(directory, f"{locator}.jpeg")
            new_png_filepath = os.path.join(directory, f"Figure{index}.png")
            if os.path.exists(jpeg_filepath):
                os.rename(jpeg_filepath, new_png_filepath)

            # Captions 정보 추가
            captions.append({
                'label': metadata.get('label'),
                'caption': metadata.get('caption')
            })

        # 새로운 captions.json 파일 작성
        with open(os.path.join(directory, 'captions.json'), 'w') as f:
            json.dump(captions, f, indent=4)

if __name__ == "__main__":
    download_image_from_xml(xml_folder = xml_folder, image_folder= image_folder, sleep_time= 1)
    process_files_in_directory(image_folder = image_folder)
