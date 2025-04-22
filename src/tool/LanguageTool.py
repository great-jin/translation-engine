from langdetect import detect

LANG_CODE_MAP = {
    'zh-cn': 'zho_Hans',
    'zh-tw': 'zho_Hant',
    'en': 'eng_Latn',
    'fr': 'fra_Latn',
    'de': 'deu_Latn',
    'ja': 'jpn_Jpan',
    'ko': 'kor_Hang',
    'es': 'spa_Latn'
}

def detectLang(text: str):
    try:
        detected = detect(text)
        # 类型映射
        return LANG_CODE_MAP.get(detected, 'eng_Latn')
    except Exception:
        return 'eng_Latn'
