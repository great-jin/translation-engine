import pysbd

seg = pysbd.Segmenter(language="en", clean=False)

# 分割示例
text = "你好。我好。大家好。"

sentences = seg.segment(text)

for sentence in sentences:
    print(sentence)
