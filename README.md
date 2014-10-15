## WAD - Wireless AdHoc Distributer

一个基于 Tornado 的 iOS 应用分发工具

### 前言

鄙司目前还在用 CVS 来管理代码，这就导致了 Xcode Bot 这样的持续集成工具没有用武之地。为了简化一下每次发布给 QA 时的工作，花了点时间写了这个工具。

### 原理

其实就是很多 shell 脚本的 Web 化，主要工作是解析上传的 IPA 文件中的 Info.plist，获取 Display name、Version、以及 Build 等信息，来生成 manifest.plist，然后更新 index.html 中的相关信息，并把 IPA 保存在“archive_path”目录下。

### 依赖

- biplist
- tornado

### 使用步骤

1. 创建配置文件

        # 监听的端口号
        port = 8888

        # 主机地址，用来下载manifest.plist以及IPA包
        host = "192.168.1.101:8888"

        # archive 上传下载目录，需要保证目录存在
        archive_path = "archives"

2. 执行`./web.py --config=path_to_config_file.conf`
3. IPA 包的上传路径"0.0.0.0:8888/admin"
4. 用 iOS 设备访问“192.168.1.101:8888”即可安装
