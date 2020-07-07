
***

### 前后项目目录分析
#### 前台（home）
* 数据模型：models.py
* 表单处理：/home/forms.py
* 模板目录：templates/home
* 静态目录：static

#### 后台（admin）
* 数据模型：models.py
* 表单处理：admin/forms.py
* 模板目录：templates/admin
* 静态目录：static

#### 目录详情
* manage.py：入口启动脚本
* app：项目app
    * \_\_init\_\_.py：初始化文件
    * models.py：数据模型文件
    * static：静态目录
    * home/admin：前台/后台模块
        * __init__.py：初始化脚本
        * views.py：视图处理文件
        * forms.py：表单处理文件
    * templates：模板目录
        * home/admin：前台/后台模板
