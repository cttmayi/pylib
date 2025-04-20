# Python Log Parser

一个用于解析和分析各种日志文件的灵活工具，特别是针对Android日志。

## 项目结构

- `lparser/`: 核心解析引擎
  - `parser/`: 包含各种日志格式的解析器
  - `utils/`: 工具函数和辅助模块
  - `basic/`: 基础功能模块
- `runtime/`: 运行时处理模块
  - `op.py`: 操作定义和映射
- `data/`: 数据文件和模板
  - `android/`: Android日志相关模板和定义
- `looper.py`: 定义用于分析日志事件的looper函数

## 主要功能

该工具可以分析日志文件，提取结构化信息，并执行以下操作：

1. 日志格式自动检测
2. 日志内容结构化解析
3. 自定义事件检测和处理
4. 时间序列分析

## looper函数说明

`looper.py`文件定义了一个looper函数，用于分析日志中的事件。目前实现的功能包括：

- **检测TE信号间隔**: 监控TE信号，确保其间隔不超过200ms，超过则发出警告
- **检查Buffer配对**: 监控DQ Buffer和Q Buffer操作，确保正确配对，检测以下异常情况：
  - Buffer被重复DQ
  - Buffer在未DQ的情况下被Q
  - Buffer被重复Q
- **检查DQ/Q时间间隔**: 监控同一Buffer的DQ和Q操作之间的时间间隔，确保不超过200ms

### 函数参数

- `name`: 事件名称
- `args`: 事件参数（字典）
- `timestamp`: 从日志开始的时间戳（微秒）
- `line`: 日志行号

## 使用方法

```python
from lparser.parser import LogParser
from runtime.op import OP_MAPS
from looper import looper

# 使用自定义looper分析日志
lp = LogParser('data/log/simple.log', OP_MAPS, looper=[looper])
logs = lp.transfor_to_df()
ops = lp.transfor_to_op(logs)
lp.op_execute(ops)
```

## 扩展

您可以通过修改`looper.py`文件中的looper函数来添加更多自定义分析逻辑，以满足特定的日志分析需求。 