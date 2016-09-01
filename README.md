# QR-Code
**QR Code in Python**

**Python QR二维码生成器**

## Example 示例

```console
python myqrcode.py -l H https://github.com/sylnsfar/QR-Code
```

![](https://github.com/sylnsfar/QR-Code/blob/master/example/qrcode0.jpg)

![](https://github.com/sylnsfar/QR-Code/blob/master/example/qrcode.jpg)

![](https://github.com/sylnsfar/QR-Code/blob/master/example/github.png)

## Usage 用法

```con
python myqrcode.py [-l [L,M,Q,H]] xxxxxx
```

* The `myqrcode.py` is the main file.

  `myqrcode.py` 是主文件。

* Argument `-l` or `--level` means the Error Correction Level: L(Low), M(Medium), Q(Quartile) and H(High). **The default level is Q**, so that you can just `python myqrcode.py xxxxxxx` . 

  参数`-l` 或者`--level` 代表纠错等级：L、M、Q 和 H（从低到高）。默认使用的等级是 Q，所以可以直接`python myqrcode.py xxxxx` 。

* `xxxxxx` is the words that you are putting into a QR-Code. You can write a URL or a sentence. 

  `xxxxxx` 代表要生成 QR 二维码的信息，可以是一个链接地址，也可以是其它字符串。

## Supported 可用字符

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

  ​