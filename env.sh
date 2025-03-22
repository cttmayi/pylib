#!/bin/bash

# 获取当前脚本的绝对路径
current_script=$(realpath "$0")

# 获取当前脚本所在的目录
current_dir=$(dirname "$current_script")

# pylib_dir=$current_dir/pylib


# HF 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 设置PYTHONPATH
export PYTHONPATH=$current_dir:$PYTHONPATH

# 加载.env文件
while IFS='=' read -r key value || [[ -n "$key" ]]; do
    # 跳过空行和注释行
    if [[ -z "$key" || "$key" =~ ^# ]]; then
        continue
    fi

    # 去除键和值两边的空格
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)

    # 导入环境变量
    # echo "export $key=$value"
    export "$key=$value"
done < .env