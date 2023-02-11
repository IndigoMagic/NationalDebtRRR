# NationalDebtRRR
国债逆回购提醒（NationalDebtReverseRepurchaseRemind）年化收益率达到预期即发送消息到自己的设备

效果如下：

<img width="369" alt="image" src="https://user-images.githubusercontent.com/37242294/218236003-31763e47-5307-4baa-8ebc-360a64515011.png">

**使用前请修改脚本，添加上自己的 PUSH_DEER_SERVER 和 PUSH_KEY **

接收消息，需要配合 PushDeer 使用 

PushDeer是一个可以自行架设的无APP推送服务，免费的，搭设详情见：https://github.com/easychen/pushdeer

没有做工作日判断，不过影响不大：）

在服务器后台运行该脚本请在脚本目录执行如下命令：
```
nohup python3 -u ./gznhg.py >/dev/null 2>log &
```
查询python进程：
```
ps -ef |grep python
```


