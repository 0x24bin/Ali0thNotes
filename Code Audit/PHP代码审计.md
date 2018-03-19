# PHP代码审计
```
http://localhost/phpbugs/
```
## 变量覆盖
### extract()
该函数使用数组键名作为变量名，使用数组键值作为变量值。针对数组中的每个元素，将在当前符号表中创建对应的一个变量。条件：若有EXTR_SKIP则不行。
```php
<?php
$a = "Original";
$my_array = array("a" => "Cat","b" => "Dog", "c" => "Horse");
extract($my_array); 
echo "\$a = $a; \$b = $b; \$c = $c";
?>
# 结果：$a = Cat; $b = Dog; $c = Horse
```
这里原来是$a是original，后面通过extract把$a覆盖变成了Cat了,所以这里把原来的变量给覆盖了。

### parse_str()
解析字符串并注册成变量
```php
$b=1;
Parse_str('b=2');
Print_r($b);
# 结果: $b=2
```

### import_request_variables()
```php
将 GET/POST/Cookie 变量导入到全局作用域中，全局变量注册。
在5.4之后被取消，只可在4-4.1.0和5-5.4.0可用。
//导入POST提交的变量值，前缀为post_
import_request_variable("p"， "post_");
//导入GET和POST提交的变量值，前缀为gp_，GET优先于POST
import_request_variable("gp"， "gp_");
//导入Cookie和GET的变量值，Cookie变量值优先于GET
import_request_variable("cg"， "cg_");
```

### $$变量覆盖

```php

```


### 案例
```php
#?shiyan=&flag=1
<?php
$flag='xxx'; 
extract($_GET);
 if(isset($shiyan))
 { 
    $content=trim(file_get_contents($flag)); # content is 0 , flag can be anything,cause file_get_contents cannot open file, return 0
    if($shiyan==$content)
    { 
        echo'ctf{xxx}'; 
    }
   else
   { 
    echo'Oh.no';
   } 
   }
?>
```

## 绕过过滤的空白字符

原理：https://baike.baidu.com/item/%E6%8E%A7%E5%88%B6%E5%AD%97%E7%AC%A6

```
控制码
"\0" "%00" (ASCII  0 (0x00))，空字节符。

制表符
"\t" (ASCII  9 (0x09))，水平制表符。

空白字符：
"\n" (ASCII 10 (0x0A))，换行符。
"\v" "\x0b" (ASCII  11 (0x0B))，垂直制表符。
"\f" "%0c" 换页符
"\r" "%0d"(ASCII  13 (0x0D))，回车符。

空格:
" " "%20" (ASCII  32 (0x20))，普通空格符。
```

而trim过滤的空白字符有
```php
string trim ( string $str [, string $character_mask = " \t\n\r\0\x0B" ] )
```
其中缺少了\f

2 函数对空白字符的特性
is_numeric函数在开始判断前，会先跳过所有空白字符。这是一个特性。
也就是说，is_numeirc(" \r\n \t 1.2")是会返回true的。同理，intval(" \r\n \t 12")，也会正常返回12。



案例

https://github.com/bowu678/php_bugs/blob/master/02%20%E7%BB%95%E8%BF%87%E8%BF%87%E6%BB%A4%E7%9A%84%E7%A9%BA%E7%99%BD%E5%AD%97%E7%AC%A6.php
```php
#?number=%00%0c191
# 1 %00绕过is_numeric
# 2 \f（也就是%0c）在数字前面，trim，intval和is_numeric都会忽略这个字符
```

## 整数溢出

php整数上限溢出绕过intval

intval 函数最大的值取决于操作系统。 
32 位系统最大带符号的 integer 范围是 -2147483648 到 2147483647。举例，在这样的系统上， intval('1000000000000') 会返回 2147483647。
64 位系统上，最大带符号的 integer 值是 9223372036854775807。


## 浮点数精度忽略
```php
if ($req["number"] != intval($req["number"]))
```
在小数小于某个值（10^-16）以后，再比较的时候就分不清大小了。
输入number = 1.00000000000000010, 右边变成1.0, 而左与右比较会相等。



## 多重加密


题目中有：
```php
$login = unserialize(gzuncompress(base64_decode($requset['token'])));
if($login['user'] === 'ichunqiu'){echo $flag;}
```
本地则写：
```php
<?php
$arr = array(['user'] === 'ichunqiu');
$token = base64_encode(gzcompress(serialize($arr)));
print_r($token);
// 得到eJxLtDK0qs60MrBOAuJaAB5uBBQ=
?>
```

## 截断

### iconv 可用chr(128)截断

echo iconv('GB2312', 'UTF-8', $str); //将字符串的编码从GB2312转到UTF-8

### eregi、ereg可用%00截断

功能：正则匹配过滤
条件：要求php<5.3.4

实例：
```php
## http://127.0.0.1/Php_Bug/05.php?password=1e9%00*-*
#GET方式提交password，然后用ereg()正则限制了password的形式，只能是一个或者多个数字、大小写字母，继续strlen()限制了长度小于8并且大小必须大于9999999，继续strpos()对password进行匹配，必须含有-，最终才输出flag
#因为ereg函数存在NULL截断漏洞，导致了正则过滤被绕过,所以可以使用%00截断正则匹配。对于另一个难题可以使用科学计数法表示，计算器或电脑表达10的的幂是一般是e，也就是1.99714e13=19971400000000，所以构造 1e8 即 100000000 > 9999999，在加上-。于是乎构造password=1e8%00*-*,成功得到答案

<?php
if (isset ($_GET['password'])) {
    if (ereg ("^[a-zA-Z0-9]+$",$_GET['password']) === FALSE)    
       {
        echo '<p>You password must be alphanumeric</p>';
    }
    else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)
    {
        if (strpos ($_GET['password'], '*-*') !== FALSE)
        {
            die('Flag: ' . $flag);
        }
        else
        {
            echo('<p>*-* have not been found</p>');
        }
    }
    else
    {
        echo '<p>Invalid password</p>';
    }
}
?>
```


### move_uploaded_file 用\0截断
5.4.x<= 5.4.39, 5.5.x<= 5.5.23, 5.6.x <= 5.6.7
原来在高版本（受影响版本中），PHP把长度比较的安全检查逻辑给去掉了，导致了漏洞的发生
cve：
https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-2348

`move_uploaded_file($_FILES['x']['tmp_name'],"/tmp/test.php\x00.jpg")`
上传抓包修改name为a.php\0jpg（\0是nul字符），可以看到$_FILES['xx']['name']存储的字符串是a.php，不会包含\0截断之后的字符，因此并不影响代码的验证逻辑。
但是如果通过$_REQUEST方式获取的，则可能出现扩展名期望值不一致的情况，造成“任意文件上传”。

### inclue用？截断
条件：
```php
<?php  
$name=$_GET['name'];  
$filename=$name.'.php';  
include $filename;  
?>
```
当输入的文件名包含URL时，问号截断则会发生，并且这个利用方式不受PHP版本限制，原因是Web服务其会将问号看成一个请求参数。
测试POC：
http://127.0.0.1/test/t1.php?name=http://127.0.0.1/test/secret.txt?
则会打开secret.txt中的文件内容。本测试用例在PHP5.5.38版本上测试通过。

### 系统长度截断
这种方式在PHP5.3以后的版本中都已经得到了修复。
win260个字符，linux下4*1024=4096字节

### mysql长度截断
mysql内的默认字符长度为255，超过的就没了。
由于mysql的sql_mode设置为default的时候，即没有开启STRICT_ALL_TABLES选项时，MySQL对于插入超长的值只会提示warning

### mysql中utf-8截断

`insert into dvwa.test values (14,concat("admin",0xc1,"abc"))`

写入为admin




## 资料

PHP代码审计分段讲解

https://github.com/bowu678/php_bugs


