# Cobot Project

## **本项目基于**
 - [`mirai`](https://github.com/mamoe/mirai): 即 `mirai-core`, 一个高性能, 高可扩展性的 QQ 协议库
 - [`mirai-console`](https://github.com/mamoe/mirai-console): 一个基于 `mirai` 开发的插件式可扩展开发平台
 - [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http): 一个提供基于http协议与 `mirai` 交互方式的 `mirai-console` 插件
 - [`Graia Application`](https://github.com/GraiaProject/Application): 为本项目提供使用 `python` 调用 `mirai-api-http` 接口方法的包

 ## **目前功能与指令**
 ### 复读机
 支持两种模式，现阶段词汇写死于代码，计划更改为使用配置文件进行识别。
 
 运行后将在当前群聊发送关键字。
 #### 模式一：存在匹配即复读
 关键字："确实"、"下次一定"
 #### 模式二：完全匹配才复读
 关键字："晚安"
 
 ### 天气预报
 基于/config/Cobot/WeatherList.yml文件对用户识别，即将推出添加与修改用户配置指令。
 
 指令："早"、"观星"
 
 运行后将从wthrcdn.etouch.cn请求天气信息并发送至群聊。
 
 ### 成语接龙
 基于/data.tx文件中的成语库在群聊中展开成语接龙。
 
 规则：新词汇首字注音必须在成语库中与待接成语末字注音相同。
 
 指令："开始"、"结束"、"解释"、【成语】
 
 "开始"：将在所有群聊中开始一个成语接龙（计划改为多线），并在当前群聊发送第一个待接成语。
 
 "结束"：将结束所有群聊中的成语接龙，并在当前群聊发送"已结束"。
 
 "解释"：将在成语库中查询当前待接成语的解释，并发送至当前群聊。
 
 【成语】：若【成语】存在于成语库中并符合接龙规则，，则将发送"【成语】 正确！"至当前群聊，并将待接成语更新为该词。