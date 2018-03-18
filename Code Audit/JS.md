

# JS




## escape()

已编码的 string 的副本。其中某些字符被替换成了十六进制的转义序列。该方法不会对 ASCII 字母和数字进行编码，也不会对下面这些 ASCII 标点符号进行编码： * @ - _ + . / 。其他所有的字符都会被转义序列替换。

在本例中，我们将使用 escape() 来编码字符串：
```html
<script type="text/javascript">

document.write(escape("Visit W3School!") + "<br />")
document.write(escape("?!=()#%&"))

</script>
```
输出：
```js
Visit%20W3School%21
%3F%21%3D%28%29%23%25%26
```

