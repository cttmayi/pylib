

# 检查的几种形式

1. A状态，B状态不能同时出现
2. A操作，B操作 成对出现 （限定时间内）

State: None; Action: TE:1000ms
State: TE:1000ms; Action: TE:1020ms

State: None; Action: TE:1000ms
State: TE:1000ms; Action: FRMAE: START, 1001ms
State: TE:1000ms; FRAME:START, 1001ms; Action: TE: 1020ms
State: TE:1020ms; FRAME:START, 1001ms; Action: FRAME:END, 1022ms
State: TE:1020ms; FRAME: END, 1022ms; Action: FRAME: START, 1023ms
State: TE:1000ms; Action: FRMAE: START, 1023ms
