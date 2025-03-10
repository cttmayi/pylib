import numpy as np
import torch

def analyze_keys(data_list):
    """
    分析数据列表，为每个键生成独立的映射表，并返回键的顺序。
    支持嵌套字典和列表。
    """
    key_to_values = {}  # 用于存储每个键的所有唯一值
    all_keys = set()  # 用于存储所有出现过的键

    def analyze_item(item, prefix=""):
        """递归分析字典或列表中的键和值"""
        if isinstance(item, dict):
            for key, value in item.items():
                full_key = f"{prefix}.{key}" if prefix else key  # 构造嵌套键
                all_keys.add(full_key)  # 添加键到集合中
                if isinstance(value, str):  # 如果值是字符串
                    if full_key not in key_to_values:
                        key_to_values[full_key] = set()
                    key_to_values[full_key].add(value)
                elif isinstance(value, (dict, list)):  # 如果值是嵌套字典或列表
                    analyze_item(value, prefix=full_key)
        elif isinstance(item, list):
            for element in item:
                analyze_item(element, prefix=prefix)

    # 遍历数据列表中的每个字典
    for data in data_list:
        analyze_item(data)

    # 为每个键生成映射表，并记录键的顺序
    key_to_mapping = {}
    key_order = sorted(all_keys)  # 按字母顺序排序键，确保一致性
    for key in key_order:
        if key in key_to_values:
            key_to_mapping[key] = {value: idx for idx, value in enumerate(sorted(key_to_values[key]))}

    return key_to_mapping, key_order


def encode_data(data_list, key_to_mapping, key_order):
    """
    根据每个键的映射表对数据列表进行编码。
    缺失的键使用默认值0。
    支持嵌套字典和列表。
    """
    def encode_item(item, key_to_mapping, prefix=""):
        """递归编码字典或列表中的值"""
        if isinstance(item, dict):
            encoded_dict = {}
            for key in key_order:  # 遍历所有键（按顺序）
                full_key = f"{prefix}.{key}" if prefix else key
                if full_key in item:
                    value = item[full_key]
                    if isinstance(value, str):  # 如果值是字符串
                        encoded_dict[full_key] = key_to_mapping[full_key][value]
                    elif isinstance(value, (dict, list)):  # 如果值是嵌套字典或列表
                        encoded_dict[full_key] = encode_item(value, key_to_mapping, prefix=full_key)
                    else:
                        encoded_dict[full_key] = value  # 非字符串值保持不变
                else:
                    encoded_dict[full_key] = 0  # 缺失键使用默认值0
            return encoded_dict
        elif isinstance(item, list):
            return [encode_item(element, key_to_mapping, prefix=prefix) for element in item]
        else:
            return item

    encoded_data = [encode_item(data, key_to_mapping) for data in data_list]
    return encoded_data


def convert_to_tensor(encoded_data, key_order):
    """
    将编码后的数据转换为张量。
    支持嵌套结构，但最终需要展平为一维向量。
    """
    def flatten(data):
        """递归展平嵌套结构"""
        if isinstance(data, dict):
            return [flatten(value) for key, value in data.items() if key in key_order]
        elif isinstance(data, list):
            return [flatten(item) for item in data]
        else:
            return [data]

    # 将每个字典转换为固定长度的数值向量
    tensor_data = []
    for encoded_dict in encoded_data:
        flattened = flatten(encoded_dict)
        tensor_data.append([item for sublist in flattened for item in sublist])  # 展平为一维向量

    # 转换为 NumPy 数组或 PyTorch 张量
    tensor_data = np.array(tensor_data, dtype=np.float32)
    tensor_data = torch.tensor(tensor_data, dtype=torch.float32)

    return tensor_data


# 示例数组，包含嵌套字典和列表
data_list = [
    {"name": "Alice", "age": 25, "address": {"city": "Beijing", "zip": "100086"}},
    {"name": "Bob", "age": 30, "address": {"city": "Shanghai", "zip": "200000"}},
    {"name": "Alice", "age": 22, "address": {"city": "Beijing"}},
    {"name": "Charlie", "age": 28, "address": {"city": "Shanghai", "zip": "200000"}, "hobbies": ["reading", "traveling"]}
]

# 分析数据并生成每个键的映射表，同时返回键的顺序
key_to_mapping, key_order = analyze_keys(data_list)

# 根据映射表对数据进行编码
encoded_data = encode_data(data_list, key_to_mapping, key_order)

# 将编码后的数据转换为张量
tensor_data = convert_to_tensor(encoded_data, key_order)

# 打印结果
print("Encoded Data:", encoded_data)
print("Key to Mapping:", key_to_mapping)
print("Key Order:", key_order)
print("Tensor Data:", tensor_data)