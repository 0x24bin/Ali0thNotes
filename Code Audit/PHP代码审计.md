# PHP代码审计
```
http://localhost/phpbugs/
```
## extract变量覆盖
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

原理：
1 空白字符：
```
" " (ASCII  32 (0x20))，普通空格符。
"\t" (ASCII  9 (0x09))，制表符。
"\n" (ASCII 10 (0x0A))，换行符。
"\r" (ASCII  13 (0x0D))，回车符。
"\0" (ASCII  0 (0x00))，空字节符。
"\x0B" (ASCII  11 (0x0B))，垂直制表符。
%00
%0c


```


而trim过滤的空白字符有
```php
string trim ( string $str [, string $character_mask = " \t\n\r\0\x0B" ] )
```
其中缺少了\f

2 函数对空白字符的特性
is_numeric函数在开始判断前，会先跳过所有空白字符。这是一个特性。
也就是说，is_numeirc(" \r\n \t 1.2")是会返回true的。同理，intval(" \r\n \t 12")，也会正常返回12。



### 案例

https://github.com/bowu678/php_bugs/blob/master/02%20%E7%BB%95%E8%BF%87%E8%BF%87%E6%BB%A4%E7%9A%84%E7%A9%BA%E7%99%BD%E5%AD%97%E7%AC%A6.php
```php
#?number=%00%0c191
# 1 %00绕过is_numeric
# 2 \f（也就是%0c）在数字前面，trim，intval和is_numeric都会忽略这个字符
```









## 资料

PHP代码审计分段讲解

https://github.com/bowu678/php_bugs


