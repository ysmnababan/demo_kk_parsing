import re  

translation_mapping = {
    "laki laki": "男性",
    "pria": "男性",
    "perempuan": "女性",
    "wanita": "女性",
    "islam": "イスラム教",
    "kristen": "キリスト教",
    "katolik": "カトリック",
    "hindu": "ヒンドゥー教",
    "buddha": "仏教",
    "belum kawin": "未婚",
    "kawin tercatat": "既婚",
    "kawin": "既婚",
    "cerai hidup": "離婚",
    "cerai mati": "死別",
    "pelajar/mahasiswa": "学生",
    "pelajar" :"学生",
    "mahasiswa" :"学生",
    "belum/tidak bekerja": "未就労",
    "belum bekerja": "未就労",
    "tidak bekerja": "未就労",
    "mengurus rumah tangga": "家事",
    "pensiunan": "定年",
    "pegawai negeri sipil": "公務員",
    "pns": "公務員",
    "tni": "軍人",
    "petani/pekebun": "農家",
    "petani": "農家",
    "peternak": "畜産",
    "karyawan swasta": "会社員",
    "buruh harian lepas": "アルバイト",
    "buruh tani/perkebunan": "農民",
    "pembantu rumah tangga": "家事手伝い",
    "tukang cukur": "理容師",
    "tukang listrik": "電気技師",
    "tukang batu": "石工",
    "tukang kayu": "大工",
    "wartawan": "記者",
    "ustadz/mubaligh": "牧師",
    "guru": "教師",
    "sopir": "運転手",
    "pedagang": "商人",
    "perangkat desa": "役人",
    "kepala desa": "村長",
    "wiraswasta": "自営業",
    "tidak/belum sekolah": "学歴なし",
    "belum tamat sd": "小学校未卒",
    "tamat sd/sederajat": "小学校卒業",
    "sltp/sederajat": "中学校卒業",
    "slta/sederajat": "高校卒業",
    "diploma i/ii": "短大",
    "akademi/diploma iii/sarjana muda": "専門学校",
    "diploma iv/strata i": "大学",
    "strata ii": "大学院",
    "strata iii": "博士課程",
    "kepala keluarga": "家長",
    "suami": "夫",
    "istri": "妻",
    "anak": "子",
    "menantu": "義理の子",
    "cucu": "孫",
    "orangtua": "両親",
    "mertua": "義理の親",
    "famili lain": "他の家族",
    "pembantu": "使用人",
    "lainnya": "その他",
    "indonesia":"インドネシア",
    "wni":"インドネシア"
}



def normalize_text(text):
    # Remove spaces around slashes for consistency (e.g., 'slta / sederajat' to 'slta/sederajat')
    return re.sub(r'\s*/\s*', '/', text.lower())

# def translate(text):
#     # Normalize the input to lowercase to make it case-insensitive
#     text = text.lower()
#     normalized_text = normalize_text(text)
    
#     # Look for the variations in the text and translate them
#     for key, value in translation_mapping.items():
#         # Handle the key with spaces properly by replacing 'laki laki' with '男性'
#         # Use regex to replace occurrences of each key in the text with the corresponding value
#         normalized_text = re.sub(r'\b' + re.escape(key) + r'\b', value, normalized_text)

#     return normalized_text

def translate(text):
    # Normalize to lowercase and clean it up if needed
    text = text.lower()
    normalized_text = normalize_text(text)
    
    # Return the translation if found, otherwise return the original text (or None if you prefer)
    return translation_mapping.get(normalized_text, text)