import re
import json
import os

def prefix_keywords_with_hash(text):
    keywords = ["No.","Nama", "Kecamatan", "Alamat", "Kabupaten", "RT", "Kode", "Desa", "Provinsi"]

    for keyword in keywords:
        # Allow underscores between letters and match case-insensitively
        pattern = r'(?<!#)(?:_*)'.join(list(keyword))
        regex = re.compile(rf'(?<!#){pattern}', re.IGNORECASE)
        text = regex.sub(lambda m: '#' + m.group(), text)

    return text

def extract_values(text):
    # Keywords to search for (case insensitive)
    keywords = ["No.", "Keluarga", "Kecamatan", "Alamat", "Kota", "RW", "Pos", "Kelurahan", "Provinsi"]
    result = {}

    for keyword in keywords:
        # Match keyword, optional underscores/spaces, optional colon, then capture until #, newline, or end of text
        pattern = re.compile(rf'{keyword}[\s_]*:?([\s\S]*?)(?=#|\n|$)', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            value = matches[-1]  # Take the last match, assuming it's the most relevant one
            cleaned = re.sub(r'\s+', ' ', value.replace(':', '').replace('_', ' ')).strip()
            result[keyword.lower()] = cleaned

    return result

def save_to_json(data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # Add only new keys (don't overwrite existing keys)
    for key, value in data.items():
        if key not in existing_data:
            existing_data[key] = value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

ocr_text = """BHINNEKA_IKA__________________KARTU_____________KELUARGA
TUNGGAL
No.________3212270106090071
Nama__Kepala__Keluarga___:_H.__ABSORI_____________________________Kecamatan____:___SUKAGUMIWANG
Alamat_________:_BLOK_JATI_____________________________Kabupaten_/_Kota_:__INDRAMAYU
RT_/_RW________:_015_/_004____________________________Kode_Pos____:_0
Desa_/__Kelurahan_____:__TERSANA_____________________________Provinsi_____:_JAWA__BARAT"""
result = prefix_keywords_with_hash(ocr_text)
print(result)
print("=========================")
data = extract_values(result)
for k, v in data.items():
    print(f"{k}: {v}")

save_to_json(data,"./output/kk_data.json")