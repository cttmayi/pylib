import torch
import pandas as pd
import numpy as np

# 定义一个DataFrame数据
data = pd.DataFrame([
    ["green", "S", 100,"label1"],
    ["blue", "M", 110,"label2"],
    ["red", "X", 120,"label3"],
    ["black", "XL", 130,"label4"]
])
# 设置列名
data.columns = ["color", "size", "price","label"]
#通过枚举获取类标与整数之间的映射关系
label_mapping = {label:idx for idx,label in enumerate(np.unique(data["label"]))}
print(label_mapping)
#对label列进行映射
data["size_label"] = data["label"].map(label_mapping)
print(data)
