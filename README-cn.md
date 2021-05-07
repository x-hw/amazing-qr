# Amazing-QR

[![former name](https://img.shields.io/badge/old%20name-MyQR-yellow)](https://pypi.org/project/myqr/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/myqr?label=downloads@myqr)](https://pypi.org/project/myqr/) [![](https://img.shields.io/badge/language-Python-blue)](https://www.python.org/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/amzqr?logo=python&logoColor=ffffff&label=Python&labelColor=blue&color=ffffff) [![PyPI](https://img.shields.io/pypi/v/amzqr?logo=pypi&logoColor=ffffff&label=PyPI&labelColor=blue)](https://pypi.org/project/amzqr/) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/amzqr) [![PyPI - Downloads](https://img.shields.io/pypi/dm/amzqr)](https://pypi.org/project/amzqr/) [![PyPI - License](https://img.shields.io/pypi/l/amzqr)](https://github.com/x-hw/amazing-qr/blob/master/LICENSE.md) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/x-hw/amazing-qr) ![macos](https://img.shields.io/badge/-macOS-black?logo=macos) ![linux](https://img.shields.io/badge/-Linux-yellow?logo=linux) ![windows](https://img.shields.io/badge/-Windows-blue?logo=windows)

[![](https://img.shields.io/badge/GitHub-x.hw-blue?logo=github)](https://github.com/x-hw) [![sponsor](https://img.shields.io/badge/sponsor--pink?logo=github-sponsors&labelColor=pink)](#打赏杯咖啡)

[*back to English*](https://github.com/x-hw/amazing-qr/blob/master/README.md)

## 概述

**Python 二维码生成器**

可生成*普通二维码*、*带图片的艺术二维码（黑白与彩色）*、*动态二维码（黑白与彩色）*。

## Contents 目录

* [Amazing-QR](#amazing-qr)
  * [概述](#概述)
  * [目录](#目录)
  * [示例](#示例)
  * [安装](#安装)
  * [使用方法](#使用方法)
    * [命令行方式](#命令行方式)
    * [作为导入文件](#作为导入文件)
  * [使用提示](#使用提示)
  * [可用字符](#可用字符)
  * [环境](#环境)
  * [协议](#协议)
  * [打赏杯咖啡☕️](#打赏杯咖啡)

## 示例

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs0.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs1.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs2.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/c_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode.gif)

![](https://github.com/x-hw/amazing-qr/blob/master/example/zootopia_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode0.gif)


## 安装

```python
pip install amzqr
```

## 使用方法

### 命令行方式

*（**提示**：如果你尚未安装 [**amzqr**](https://pypi.python.org/pypi/amzqr) ，以下内容请使用`python(3) amzqr.py` 而非`amzqr` 。）*

```python
# 概括
amzqr  Words
      [-v {1,2,3,...,40}]
      [-l {L,M,Q,H}]
      [-n output-filename]
      [-d output-directory]
      [-p picture_file]
      [-c]
      [-con contrast]
      [-bri brightness]
```

- [普通二维码](#普通二维码) 介绍了 `Words`, `-v`, `-l`, `-n`, `-d` 
- [艺术二维码](#艺术二维码) 介绍了  `-p`, `-c`, `-con`, `-bri`
- [动态GIF二维码](#动态gif二维码) 介绍了动态的生成方法和注意点

#### 普通二维码

![](https://github.com/x-hw/amzqr/blob/master/example/0.png)

```markdown
#1 Words
amzqr https://github.com
```

* 在命令后输入链接或者句子作为参数，然后在程序的当前目录中产生相应的二维码图片文件，默认命名为” qrcode.png“。

```markdown
#2 -v, -l
amzqr https://github.com -v 10 -l Q
```

* **默认边长**是取决于你输入的信息的长度和使用的纠错等级；

  而**默认纠错等级**是最高级的H。

* **自定义**：如果想要控制边长和纠错水平就使用 `-v` 和 `-l` 参数。

   `-v` 控制边长，范围是**1至40**，数字越大边长越大；

   `-l` 控制纠错水平，范围是**L、M、Q、H**，从左到右依次升高。

```markdown
#3 -n, -d
amzqr https://github.com -n github_qr.jpg  -d .../paths/
```

- **默认输出文件名**是“ qrcode.png "，而**默认存储位置**是当前目录。

- 自定义：可以自己定义输出名称和位置。**注意**同名文件会覆盖旧的。

  `-n` 控制文件名，格式可以是 `.jpg`， `.png` ，`.bmp` ，`.gif` ；

  `-d` 控制位置。

  #### 艺术二维码

![](https://github.com/x-hw/amazing-qr/blob/master/example/1.png)![](https://github.com/x-hw/amazing-qr/blob/master/example/2.png)

```markdown
#1 -p
amzqr https://github.com -p github.jpg
```

* 参数`-p` 用来将QR二维码图像与一张同目录下的图片相结合，产生一张**黑白**图片。

```markdown
#2 -c
amzqr https://github.com -p github.jpg -c
```

* 加上参数 `-c` 可以使产生的图片由黑白变为**彩色**的。

```markdown
#3 -con, -bri
amzqr https://github.com -p github.jpg [-c] -con 1.5 -bri 1.6
```

* 参数`-con` 用以调节图片的**对比度**，1.0 表示原始图片，更小的值表示更低对比度，更大反之。**默认为1.0**。

* 参数 `-bri` 用来调节图片的**亮度**，其余用法和取值与 `-con` 相同。

#### 动态GIF二维码

![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode0.gif)

动态二维码与上述的带图片的二维码的生成方法没什么区别，你只要采用 `.gif` 格式的图片即可生成黑白或者彩色的动态二维码。但**注意**如果使用了 `-n` 参数自定义输出的文件名，切记其格式也必须是 `.gif` 格式。

### 作为导入文件

```python
# 安装模块后
from amzqr import amzqr
version, level, qr_name = amzqr.run(
    words,
    version=1,
    level='H',
    picture=None,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name=None,
    save_dir=os.getcwd()
)
```

*以下各个参数已经在[上文](#命令行方式)有所介绍*

```python
# help(amzqr)
Positional parameter
   words: str

Optional parameters
   version: int, from 1 to 40
   level: str, just one of ('L','M','Q','H')
   picutre: str, a filename of a image
   colorized: bool
   constrast: float
   brightness: float
   save_name: str, the output filename like 'example.png'
   save_dir: str, the output directory
```
## 使用提示

* 请采用**正方形**或近似正方形的图片

* 建议在图片尺寸大的时候使用 `-v` 的值也应该**适当**变大。

* 如果图片有透明无色部分，最终效果是：![](https://github.com/x-hw/amazing-qr/blob/master/example/aa.png)

  你可以将透明部分修改成白色，最终效果会变成![](https://github.com/x-hw/amazing-qr/blob/master/example/a0.png)

## 可用字符

* 数字 0 到 9

* 大小写的英文字母

* 常用**英文标点符号**和空格

  ```console
  · , . : ; + - * / \ ~ ! @ # $ % ^ & ` ' = < > [ ] ( ) ? _ { } | and  (space)
  ```

## 环境

- Python 3

## 协议

* GPLv3

## 打赏杯咖啡

[![GitHub Sponsors](https://img.shields.io/github/sponsors/x-hw?logo=github-sponsors&labelColor=pink&color=white)](https://github.com/sponsors#regions)

*GitHub Sponsors 还用不了...*

![wechatpay](https://img.shields.io/badge/-微信打赏-brightgreen?labelColor=brightgreen&logo=data:image/png;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAAAAAAAGa0aABmtGg4ZrRoOGa0aABmtGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABmtGgAZrRpGGa0arBmtGkEZrRobGa0aOBmtGkwZrRpNGa0aORmtGhoZrRoDGa0aAAAAAAAAAAAAAAAAAAAAAAAZrRoAGa0aKBmtGucZrRrwGa0a3BmtGvIZrRr6Ga0a+xmtGvMZrRrYGa0alxmtGjcZrRoCGa0aAAAAAAAZrRoAGa0aBhmtGnMZrRr1Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRroGa0adBmtGgkZrRoAGa0aAhmtGnEZrRr2Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGvgZrRp5Ga0aAxmtGkEZrRrmGa0a/xmtGv8ZrRr+Ga0a8RmtGvsZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a6hmtGkkZrRqlGa0a/xmtGv8ZrRr/Ga0a5RmtGkwZrRpzGa0a3hmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRqvGa0a3xmtGv8ZrRr/Ga0a/xmtGpkZrRoDGa0aABmtGicZrRqWGa0a7hmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a5xmtGusZrRr/Ga0a/xmtGu0ZrRo9Ga0aPBmtGmcZrRohGa0aAxmtGj8ZrRq0Ga0a+BmtGv8ZrRr/Ga0a/xmtGvIZrRrQGa0a/xmtGv8ZrRrLGa0agRmtGukZrRr+Ga0a3RmtGosZrRowGa0aEBmtGlsZrRrNGa0a/RmtGv8ZrRrYGa0agxmtGv0ZrRr/Ga0a+hmtGvsZrRr/Ga0a/xmtGv8ZrRr/Ga0a6hmtGqIZrRpDGa0aJRmtGnsZrRrhGa0ajBmtGiAZrRrHGa0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a9BmtGrcZrRpdGa0aOxmtGhoZrRoAGa0aPBmtGtcZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr/Ga0a1BmtGiwZrRoAGa0aABmtGgAZrRowGa0arRmtGvQZrRr/Ga0a/xmtGv8ZrRr/Ga0a/xmtGv8ZrRr2Ga0asRmtGjQZrRoAGa0aAAAAAAAZrRoAGa0aABmtGgsZrRpFGa0ajRmtGrsZrRrPGa0azxmtGr0ZrRqQGa0aSBmtGgwZrRoAGa0aAAAAAAAAAAAAAAAAAAAAAAAAAAAAGa0aABmtGgEZrRoKGa0aFBmtGhUZrRoKGa0aARmtGgAAAAAAAAAAAAAAAAAAAAAAz/8AAMAPAADAAwAAgAEAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAgAEAAMADAADgBwAA+B8AAA==)

<img src="https://github.com/x-hw/amazing-qr/blob/master/example/wechatpay.jpg" width = "124" height = "116" alt="wechatpay" align=center />

![alipay](https://img.shields.io/badge/-支付宝打赏-blue?logo=alipay&logoColor=ffffff&labelColor=blue)

<img src="https://github.com/x-hw/amazing-qr/blob/master/example/alipay.gif" width = "132" height = "132" alt="alipay" align=center />
