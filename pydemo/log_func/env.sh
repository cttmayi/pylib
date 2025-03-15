#!/bin/bash

# 获取当前脚本的绝对路径
current_script=$(realpath "$0")

# 获取当前脚本所在的目录
current_dir=$(dirname "$current_script")

export PYTHONPATH=${current_dir}:$PYTHONPATH
