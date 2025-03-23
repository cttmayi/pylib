#!/bin/bash

# 获取脚本所在的目录路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# 切换到脚本所在的目录
cd "$SCRIPT_DIR" || exit

ZIP_FILE="data/android/android_v1.zip"
ZIP_FILE_LOG="data/android/Android.log"
LOG_FILE="data/android/1M.log"

# 判断是否已经下载了日志文件
if [ ! -f "$ZIP_FILE" ] && [ ! -f "$ZIP_FILE_LOG" ] && [ ! -f "$LOG_FILE" ]; then
    echo "日志文件未下载，开始下载..."
    # 下载日志文件
    curl -o $ZIP_FILE https://zenodo.org/records/8196385/files/Android_v1.zip
    echo "日志文件下载完成"
fi

if [ ! -f "$ZIP_FILE_LOG" ] && [ ! -f "$LOG_FILE" ]; then
    unzip "$ZIP_FILE" -d data && rm "$ZIP_FILE"
    echo "日志文件解压完成"
fi

if [ ! -f "$LOG_FILE" ]; then
    mv $ZIP_FILE_LOG $LOG_FILE
fi
echo "日志文件下载完成"

