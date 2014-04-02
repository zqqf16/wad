## WAD - Wireless AdHoc Distributer

一个基于Tornado的Web iOS应用分发工具

### 前言

鄙司目前还在用CVS来管理代码，这就导致了Xcode Bot这样的持续集成工具没有用武之地。为了简化一下每次发布给QA时的工作，花了点时间写了这个工具。

### 原理

其实就是很多shell脚本的Web化，主要工作是解析上传的IPA文件中的Info.plist，获取Display name、Version、以及Build等信息，来生成manifest.plist，然后更新index.html中的相关信息，并把IPA保存在“archive_path”目录下。

### 依赖

- biplist
- tornado

### 使用步骤

1. 创建配置文件
    
        port = 8888 #监听的端口号
        host = “192.168.1.101:8888” #主机地址，用来下载manifest.plist以及IPA包
        root_path = "./" #根目录
        archive_path = "archives" #archive 上传下载目录，需要保证目录存在
        
2. 执行`./web.py --config=path_to_config_file.conf`
3. IPA包的上传路径"0.0.0.0:8888/admin"
4. 用iOS设备访问“0.0.0.0”即可安装
5. 还可以在命令行下执行`python tool.py path_to_ipa.ipa`来免Web发布

### 注意事项

1. 第一次使用需要先上传IPA
2. index.html, manifest.plist, 以及上传的IPA文件都实现了静态华，本工具可以仅用于IPA的上传以及manifest.plist的生成
3. 不要嘲笑admin界面的简陋，业余水平能把Index搞定就不错了。。。
