# wangyinewsspider


###项目介绍
1. 抓取网易新闻 (http://news.163.com/) 的新闻标题和评论
2. 抓取内容有普通新闻，娱乐，科技，女人，教育，金融，体育等7大频道，每个大频道下还有细分频道，（体育频道下有nba，cba，国内足球，世界足球等），现暂不支持抓取汽车和房产频道
3. 由于普通新闻内容较多，现在拆分3个频道去抓取和存储，分别是：社会，国内，国际
4. 每个大频道对应存储一个集合
5. 支持自定义抓取新闻频道和每条新闻的热门评论数和最新评论数

####项目依赖
1. 使用MondoDB存储数据，可使用本机或主机上的MongoDB
2. python使用了第三方库requests
```
pip install requests
```
####模块介绍
* codes  [核心代码]
	* spider_main.py  [主调度程序]
	* spider_downloader.py  [数据下载]
	* spider_parser.py  [数据解析]
	* spider_datahandler.py  [数据处理]
	* spider_urlmanager.py  [url管理]
	* spider_base  [基础数据]
	* spider_logger  [日志信息]
* settings  [爬虫设置]
	* base_setting.py
* tools  [通用方法]
	* common_tools.py
* logs  [日志存放]
* tests  [测试数据测试代码存放，请自动忽略]
* imgs  [示例图片]
* wangyinewsspider.py  [入口程序]

###使用说明
1. 下载项目
```bash
$git clone ...
```
2. 进入文件夹
```bash
$cd wangyinewsspider
```
3. 查看帮助命令
```python
python wangyinewsspider.py -h
```
启动程序所带参数：
> optional arguments:
  -l 抓取的频道,可选频道：shehui(社会),guonei(国内),guoji(国际),sports(体育),ent(娱乐),money(财经),tech(科技),lady(女性),edu(教育) 全频道抓取可输入all
  -n 抓取的线程数
  -d 抓取的延迟时间（秒）
  -hots 抓取热门评论数
  -news 抓取最新评论数
  -host mongodb的主机地址
  -port mongodb的连接端口
 
 4. 启动程序 
```python
 python wangyinewsspider.py # 所有参数均有默认值，默认4线程，0延迟，40条热门评论，20条新评论
```
![start](https://raw.githubusercontent.com/jeffreyzzh/wangyinewsspider/master/imgs/start2.png)
 输入命令参数之后，程序开始跑。
![start](https://raw.githubusercontent.com/jeffreyzzh/wangyinewsspider/master/imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202017-03-05%20%E4%B8%8A%E5%8D%889.31.44.png)
默认会打印出错的信息，可以在settings/base_setting设置日志级别。程序运行完毕，再来看看数据库。
![start](https://raw.githubusercontent.com/jeffreyzzh/wangyinewsspider/master/imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202017-03-05%20%E4%B8%8A%E5%8D%889.35.28.png)
以后浏览新闻再也不用看广告啦~~~

###更新
1.2017/03/29 日志文件清理，只保存近期7个记录文件

###TODO
1. 增加新闻的正文内容
2. 汽车频道和房产频道 
