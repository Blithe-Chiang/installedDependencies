import os
import re

import sys

## 简短的功能介绍
# 这个脚本用来查询本地maven仓库中的包的信息

# 使用方法
# python 脚本名字 maven仓库路径? # maven仓库名字是可选的，可以直接修改下面这行代码。

# maven仓库 目录
# >>>> 修改这里的路径，这样的话，就不用通过命令行参数传入maven仓库了
maven_dir = r'C:\Users\Blithe\.m2'  # 这里改成你的maven目录

# 通过命令行获取路径
if len(sys.argv) == 2:
    maven_dir = sys.argv[1]
    print('通过命令行获取路径: ', maven_dir)

if not os.path.isdir(maven_dir):
    print(maven_dir+'不是一个正确的文件夹路径')
    sys.exit(-1)


# 找到所有的jar包
filename_without_jar_list = []
for root, dirs, files in os.walk(maven_dir):
    for file in files:
        if file.endswith('.jar'):
            # if 'javadoc.jar' in file or 'sources.jar' in file:
            #   continue
            filename_without_jar_list.append(file[:-4])

if filename_without_jar_list.count == 0:
    print(maven_dir+'路径下面没有jar包，请检查路径是否正确')
    sys.exit(-1)

# 把名字和版本分离出来
pattern = re.compile(r'-(\d+(?:\.\d){1,2})')

jars = []   # list of jars: (jar_name, jar_version)
for filename in filename_without_jar_list:

    # 找到名字和版本的分隔符
    mysearch = pattern.search(filename)
    if mysearch  is not None:
        sep = mysearch.span()[0]
    else:
        sep = filename.rfind('-')
    
    jar_name = filename[:sep]
    jar_version = filename[sep+1:]
    jars.append((jar_name, jar_version))


# 把名字相同的jar包，版本放在一起
jar_with_version = {jar[0]: list() for jar in jars}

for jar in jars:
    jar_with_version[jar[0]].append(jar[1])


# 实现文字版本的工具
while True:
    # 输入jar包的名字
    query_name = input('>>请输入要查找的jar包的相关字符串\n>>(输入.exit或者CTRL-C退出) - ')
    if query_name == '.exit':
        break
    found = {k: v for k, v in jar_with_version.items() if query_name in k}
    print('='*30)
    if len(found) == 0:
        print('没有找到'+query_name+'相关的包')
    else:
        for name, version in found.items():
            print(name, ':', version)
    print('='*30)

# TODO: 画一个GUI

