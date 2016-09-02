# QR-Code
**QR Code in Python**

**Python QR二维码生成器**



## Example 示例

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs2.jpg)

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs1.jpg)

![](https://github.com/sylnsfar/qrcode/blob/master/example/qrs0.jpg)



## Usage 用法

### Common QR-Code    普通QR二维码

```
python myqr.py 	[-h] 
				[-v {1,2,3,...,40}] 
				[-l {L,M,Q,H}] 
				Words
```

* Use argument `-h` for help.

  使用参数 `-h` 来获得使用帮助。

  ​


```console
python myqr.py https://github.com
```

* **Simplest  way**: Just input a URL or a sentence, then get your QR-Code in the current directory.

  **最简单的用法**：在命令后输入链接或者句子作为参数，然后在程序的当前目录中产生相应的QR二维码图片。

  ​

```console
python myqr.py https://github.com -v 10 -l Q
```

* The **default** length of a side of QR-Code depends on both the numbers of words you input. And the **default** level (Error Correction Level) is **H** (the highest).

  默认边长是取决于你输入的信息的长度，而默认纠错等级是最高级的H。

* **Customize size**: If you want to control the length and the error-correction-level, use the `-v` and `-l` arguments. The `-v`  representing the length is from 1 to 40 that 1 means minimum and 40 means maximum. The `-l`  representing the level is one of L, M, Q and H that L means lowest and H means highest.

  **自定义尺寸**：如果想要控制边长和纠错水平就使用 `-v` 和 `-l` 参数。使用 `-v` 来控制边长，范围是1至40，数字越大边长越大；使用 `-l` 来控制纠错水平，范围是L、M、Q、H，从左到右依次升高。

  ​



### Artistic QR-Code    艺术QR二维码

	python myqr.py 	[-h] 
					[-v {1,2,3,...,40}] 
					[-l {L,M,Q,H}] 
					[-p picture_file] 
					[-c] 
					[-con contrast] 
					[-bri birghtness] 
					Words
* arguments `-h`, `-v` and `-l` is as mentioned above.

  参数 `-h`, `-v` 和 `-l` 如上文述。

  ​



```console
python myqr.py https://github.com -p github.jpg
```

* The `-p` is to combine the QR-Code with the following picture which is at the same directory as the program. The resulting picture is <u>**black and white** </u> by default.

  参数`-p` 用来将QR二维码图像与一张同目录下的图片相结合，产生一张**黑白**图片。

* **Suggestion**: If the size of the picture is large, you should choose a correct large `-v` too instead of using the default one.

  **建议**在图片尺寸大的时候使用 `-v` 的值也应该适当变大。

  ​



```console
python myqr.py https://github.com -p github.jpg -c
```

* The `-c` is to make the resulting picture **colorized**.

  加上参数 `-c` 可以使产生的图片由黑白变为**彩色**的。

  ​



```console
python myqr.py https://github.com -p github.jpg [-c] -con 1.5 -bri 1.6
```

* The `-con` changes the contrast of the picture that 1.0 means original image, lower values mean less contrast and higher mean more. Default: 1.0.

  参数`-con` 用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0。

* The `-bri` changes the brightness and the value is just like `-con`'s.

  参数 `-bri` 用来调节图片的亮度，其余用法和取值与 `-con` 相同。

  ​

## Supported Characters   可用字符

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