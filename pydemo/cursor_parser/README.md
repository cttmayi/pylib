# Python Log Parser

一个针对特定日志格式的解析工具，用于解析和分析日志文件中的事件和信号。

## 项目结构

```
.
├── main.py             # 主程序入口
├── looper.py           # 自定义分析器函数
├── lparser/            # 解析器核心模块
│   ├── parser/         # 日志解析器相关代码
│   └── utils/          # 工具函数
├── data/               # 存放日志数据
└── runtime/            # 运行时支持模块
    └── looper/         # 示例分析器
```

## 功能说明

该工具主要用于解析特定格式的日志文件，并分析其中的事件和信号。目前实现的分析功能包括：

- 检测TE信号间隔大于100ms的情况

## 支持的事件类型

- MODE: 模式改变事件
- TE: 屏幕TE信号
- DQ: 缓冲区出队事件
  - id: 缓冲区ID
- Q: 缓冲区入队事件
  - id: 缓冲区ID

## 使用方法

```bash
python main.py
```

默认会分析`data/log/simple.log`文件。

## 开发自定义分析器

在`looper.py`文件中，可以修改`looper`函数来实现自定义的分析逻辑。函数签名如下：

```python
def looper(name, args, timestamp, line):
    """
    参数:
    name: 事件名称
    args: 事件参数字典
    timestamp: 时间戳(微秒)
    line: 行号
    """
``` 