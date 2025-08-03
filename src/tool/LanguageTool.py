from langdetect import detect

LANG_CODE_MAP = {
    'zh': 'zho_Hans',
    'zh-tw': 'zho_Hant',
    'en': 'eng_Latn',
    'fr': 'fra_Latn',
    'de': 'deu_Latn',
    'ja': 'jpn_Jpan',
    'ko': 'kor_Hang',
    'es': 'spa_Latn',
    'vi': 'vie_Latn'
}

REVERSE_LANG_CODE_MAP = {v: k for k, v in LANG_CODE_MAP.items()}


# 语言检测
def detect_lang(text: str):
    try:
        detected = detect(text)
        # zh-cn
        if detected == "zh-cn":
            detected = "zh"

        # 类型映射
        return LANG_CODE_MAP.get(detected, 'eng_Latn')
    except Exception:
        return 'eng_Latn'

# 类型转化
def convert_type(lang_type: str) -> str:
    try:
        return LANG_CODE_MAP[lang_type.lower()]
    except KeyError:
        raise ValueError(f"Unsupported language type: {lang_type}")

# 类型反转
def reverse_type(code: str) -> str:
    try:
        return REVERSE_LANG_CODE_MAP[code]
    except KeyError:
        raise ValueError(f"Unsupported language code: {code}")
