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

# 退出程序，带有状态码和信息
def quit(code, msg):
    print(msg)
    sys.exit(code)

if __name__ == '__main__':
    # 通过命令行获取路径
    if len(sys.argv) == 2:
        maven_dir = sys.argv[1]
        print('通过命令行获取路径: ', maven_dir)

    # 检查是否是正确的路径
    if not os.path.isdir(maven_dir):
        quit(-1, maven_dir+'不是一个正确的文件夹路径')
    
    # 检查是否是有效的maven仓库
    repository_dir = os.path.join(maven_dir, 'repository')  # maven仓库目录下面的文件夹
    settings_file = os.path.join(maven_dir, 'settings.xml') # maven仓库目录下面的文件
    if not os.path.isdir(repository_dir) or not os.path.exists(settings_file):
        quit(-1, maven_dir+'不是一个正确的maven仓库目录')


    # 保存jar包信息，包括名字和版本
    jars = []   # list of jar: (jar_name, jar_version)
    for root, dirs, files in os.walk(maven_dir):
        for file in files:
            if file.endswith('.jar'):
                file = file[:-4] # 去掉文件名中的 ".jar"
                version = os.path.basename(root)
                version_start_pos = file.find('-'+version)
                
                if version_start_pos == -1:
                    continue
                name = file[:version_start_pos]
                jars.append((name, version))

    if len(jars) == 0:
        quit(0, maven_dir+'路径下面没有jar包，程序退出')


    # 把名字相同的jar包，版本放在一起
    jar_with_version = {jar[0]: set() for jar in jars}

    for jar in jars:
        jar_with_version[jar[0]].add(jar[1])


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

