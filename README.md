# dinosaur
##概况
基于Django框架的文档管理系统，集成django-mptt模块，以树形分类目录结构管理文章，方便的文档顺序排列，精准的“上一篇”、“下一篇”定位，整个站点的以“教程”的方式展现，类似于W3school。

欢迎访问：[程序猿](https://www.imcoder.cc)
##安装
- 数据库：如果使用MySql，必须安装 mysqlclient。可以使用pip安装：`pip install mysqlclient`
- 安装依赖：pip install -Ur requirements.txt
##配置
- 配置 ALLOWED_HOSTS：把你的站点地址写入到这个list中
- 配置数据库 DATABASES，如果你使用MySql，而且不想修改代码，那么你需要在环境变量中配置：Mysql数据库的Host、Port、用户名、密码、数据库名称，具体环境变量变量名参考DATABASES配置：
```python
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get("DINOSAUR_MYSQL_HOST"),
        'PORT': os.environ.get("DINOSAUR_MYSQL_PORT"),
        'NAME': os.environ.get("DINOSAUR_MYSQL_DB"),
        'USER': os.environ.get('DINOSAUR_MYSQL_USER'),
        'PASSWORD': os.environ.get('DINOSAUR_MYSQL_PASSWORD'),   # 'aVCvGwhhxKe0vgsP',
    }
}
```
如果在Linux系统中使用Apache作为服务器，那么你需要把你的环境变量写在 apache目录的 /bin/envvars 文件中，才能被apache的执行用户识别到。
##迁移（MySql）
###创建数据库：
```shell
CREATE DATABASE `djangoblog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
```
###运行数据迁移
```shell
./manage.py makemigrations
./manage.py migrate
```
###创建管理员帐号
```shell
./manage.py createsuperuser
```
##收集静态文件
终端下执行:  
```shell
./manage.py collectstatic --noinput
./manage.py compress --force
```
##运行：

执行： 
```shell
./manage.py runserver
```
浏览器打开: http://127.0.0.1:8000/ ，查看效果。

##后台配置
登录后台，首页->参数配置，修改“网站名称”、“网站描述”等选项，然后切换的前台查看效果。
