# _*_ coding:utf-8 _*_

from setuptools import (setup, find_packages)

setup(
    # 包名
    name="xt",
    # 版本
    version="0.1",
    # github地址
    url='https://github.com/xtpub/api-doc/tree/master/python',
    # 包的解释地址
    long_description=open('./ReadMe.txt', encoding='utf-8').read(),
    # 需要包含的子包列表
    packages=find_packages()
)