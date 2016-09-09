# QR-Code
* **update (160906)**: added an **exe** version - [myqr.exe in qrcode_win](https://github.com/sylnsfar/qrcode_win)

* **update (160908)**: added a **web** version - [amazing-qrcode](http://www.amazing-qrcode.com/) *(made by [Maras0830](https://github.com/Maras0830))*

* **update (160910)**: distributed to **PyPI** - [MyQR](https://pypi.python.org/pypi/MyQR/1.0.0) !

  ​

## Overview 概述


**QR Code in Python**

It can generate <u>common qr-code</u>, <u> artistic qr-code (black & white or colorized)</u>,  <u>animated qr-code (black & white or colorized)</u>.

**Python 二维码生成器**

可以生成<u>普通二维码</u>、<u>带图片的艺术二维码（黑白与彩色）</u>、<u>动态二维码（黑白与彩色）</u>。

​     

​            

## Contents 目录

* [Overview   概述](#overview-概述)
* [Contents 目录](#contents-目录)
* [Example 示例](#example-示例)
* [Install via pip    使用pip安装](#install-via-pip-使用pip安装)
* [Usage 用法](#usage-用法)
  * [Common QR-Code    普通QR二维码](#common-qr-code-普通qr二维码)
  * [Artistic QR-Code    艺术QR二维码](#artistic-qr-code-艺术qr二维码)
  * [Animated GIF QR-Code   动态二维码](#animated-gif-qr-code-动态二维码)
* [Tips   提示](#tips-提示)
* [Supported Characters   可用字符](#supported-characters-可用字符)
* [Dependences   依赖库](#dependences-依赖库)
* [Environment    运行环境](#environment-运行环境)
* [License 协议](#license-协议)


​

## Example 示例

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs0.jpg)

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs1.jpg)

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs2.jpg)

![](https://github.com/sylnsfar/qrcode/blob/master/example/c_qrcode.gif)![](https://github.com/sylnsfar/qrcode/blob/master/example/daftpunktocat-guy_qrcode.gif)

![](https://github.com/sylnsfar/qrcode/blob/master/example/zootopia_qrcode.gif)![](https://github.com/sylnsfar/qrcode/blob/master/example/daftpunktocat-guy_qrcode0.gif)

  

  

## Install via pip 使用pip安装

```python
pip(3) install myqr(or MyQR)
```

  

  

## Usage 用法

(**TIPS**: If you haven't install [**myqr**](https://pypi.python.org/pypi/MyQR/1.0.0), you should  `python(3) myqr.py` instead of `myqr` blow.)

### Common QR-Code 普通QR二维码

![](https://github.com/sylnsfar/qrcode/blob/master/example/0.png)

```
myqr 	[-h]
		[-v {1,2,3,...,40}]
		[-l {L,M,Q,H}]
		Words
```

* Use argument `-h` for help.

  使用参数 `-h` 来获得使用帮助。

  ​


```markdown
#1 url
myqr https://github.com
```

* **Simplest  way**: Just input a URL or a sentence, then get your QR-Code in the current directory.

  **最简单的用法**：在命令后输入链接或者句子作为参数，然后在程序的当前目录中产生相应的QR二维码图片。

  ​

```markdown
#2 -v, -l
myqr https://github.com -v 10 -l Q
```

* The **default** length of a side of QR-Code depends on the numbers of words you input. And the **default** level (Error Correction Level) is **H** (the highest).

  默认边长是取决于你输入的信息的长度，而默认纠错等级是最高级的H。

* **Customize size**: If you want to control the length and the error-correction-level, use the `-v` and `-l` arguments. The `-v`  representing the length is from a minimum of 1 to a maximum of 40. The `-l` representing the error correction level is one of L, M, Q and H, where L is the lowest level and H is the highest.

  **自定义尺寸**：如果想要控制边长和纠错水平就使用 `-v` 和 `-l` 参数。使用 `-v` 来控制边长，范围是1至40，数字越大边长越大；使用 `-l` 来控制纠错水平，范围是L、M、Q、H，从左到右依次升高。

  ​


### Artistic QR-Code 艺术QR二维码

![](https://github.com/sylnsfar/qrcode/blob/master/example/1.png)![](https://github.com/sylnsfar/qrcode/blob/master/example/2.png)

	myqr 	[-h]
			[-v {1,2,3,...,40}]
			[-l {L,M,Q,H}]
			[-p picture_file]
			[-c]
			[-con contrast]
			[-bri brightness]
			Words
* arguments `-h`, `-v` and `-l` is as mentioned above.

  参数 `-h`, `-v` 和 `-l` 如上文述。

  ​



```markdown
#1 -p
myqr https://github.com -p github.jpg
```

* The `-p` is to combine the QR-Code with the following picture which is in the same directory as the program. The resulting picture is <u>**black and white** </u> by default.

  参数`-p` 用来将QR二维码图像与一张同目录下的图片相结合，产生一张**黑白**图片。

  ​




```markdown
#2 -c
myqr https://github.com -p github.jpg -c
```

* The `-c` is to make the resulting picture **colorized**.

  加上参数 `-c` 可以使产生的图片由黑白变为**彩色**的。

  ​



```markdown
#3 -con, -bri
myqr https://github.com -p github.jpg [-c] -con 1.5 -bri 1.6
```

* The `-con` flag changes the contrast of the picture - a low number corresponds to low contrast and a high number to high contrast. Default: 1.0.

  参数`-con` 用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0。

* The `-bri` flag changes the brightness and the parameter values work the same as those for `-con`. Default: 1.0.

  参数 `-bri` 用来调节图片的亮度，其余用法和取值与 `-con` 相同。




​


### Animated GIF QR-Code 动态二维码

![](https://github.com/sylnsfar/qrcode/blob/master/example/daftpunktocat-guy_qrcode.gif)![](https://github.com/sylnsfar/qrcode/blob/master/example/daftpunktocat-guy_qrcode0.gif)

The only difference from Artistic QR-Code mentioned above is that you should input an image file in the `.gif` format. The you can get your black-and-white or colorful qr-code.

动态二维码与上述的带图片的二维码的生成方法没什么区别，你只要采用 `.gif` 格式的图片即可黑白或者彩色的动态二维码。

​

## Tips 提示

* Use a nearly **square** picture instead of a rectangle one.

  请采用**正方形**近似正方形的图片

* If the size of the picture is large, you should also choose a rightly large `-v` instead of using the default one.

  建议在图片尺寸大的时候使用 `-v` 的值也应该适当变大。

* If part of the picture is transparent, the qr code will look like: ![](https://github.com/sylnsfar/qrcode/blob/master/example/aa.png)

  You can change the transparent layer to white, and then it will look like: ![](https://github.com/sylnsfar/qrcode/blob/master/example/a0.png)

  如果图片有透明无色部分，最终效果是：![](https://github.com/sylnsfar/qrcode/blob/master/example/aa.png)

  你可以将透明部分修改成白色，最终效果会变成![](https://github.com/sylnsfar/qrcode/blob/master/example/a0.png)


​

## Supported Characters 可用字符

* Numbers:  `0~9`

  数字 0 到 9

* Letters:  `a~z, A~Z`

  大小写的英文字母

* Common punctuations:

  常用**英文标点符号**和空格

  ```console
  · , . : ; + - * / \ ~ ! @ # $ % ^ & ` [ ] ( ) ? _ { } | and  (space)
  ```


​

## Dependencies 依赖库

* [pillow](https://python-pillow.org/)
* [numpy](http://www.numpy.org/)
* [imageio](https://pypi.python.org/pypi/imageio)




(**TIPS**: Without a installed [MyQR](https://pypi.python.org/pypi/MyQR/1.0.0), you should use `pip install -r requirements.txt` to ensure you have all dependencies.)

（提示：如果没有安装 [MyQR](https://pypi.python.org/pypi/MyQR/1.0.0) ，使用命令`pip install -r requirements.txt` 来安装所有依赖的库。）



## Environment 运行环境

* Linux, Python 3
* Windows, Python 3



## License 协议 

* GPLv3