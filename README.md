# [URL-shortener](https://github.com/Muxi-Studio/URL-shortener)
Muxi URL-shortener service (MUS). A full-featured URL shortening service. 
Its principle is to convert a decimal number into a 62-digit number.

## Fundamental

st=>start: 开始
e=>end: 结束
io1=>inputoutput: 输入网址
io2=>inputoutput: 返回短网址
io3=>inputoutput: 提示用户
该短码已存在
io4=>inputoutput: 提示用户
不能输入短链接
op1=>operation: 返回短码
op2=>operation: 保存输入的网址到数据库
op3=>operation: 根据id计算对应的短码
op4=>operation: 查询数据库
获得一条
自定义短码的url
对应的id记录
op5=>operation: 更新短码到数据库
cond1=>condition: 查询数据库
是否存在该URL
cond2=>condition: 用户选择
自定义短码
cond3=>condition: 生成的短码
是否存在
cond4=>condition: 短码是否存在
cond5=>condition: 短码是否存在
cond6=>condition: 自定义的短码
是否存在
cond7=>condition: 用户输入的是短链接

st->io1->cond7
cond7(no,bottom)->cond1
cond7(yes)->io4->e
cond1(no,bottom)->cond2
cond1(yes)->op1->io2->e
cond2(no,bottom)->op3->cond4
cond2(yes)->cond5
cond4(no, bottom)->op5->op1->io2->e
cond4(yes)->op4->op3->cond4
cond5(no,bottom)->op5
cond5(yes)->io3->e

## Features
- Supports custom short code
- Support for URL mapping lock
- Support for URL mapping password
- Multi-user support
- Secure permissions and role management
- URL mapping management


## 二、功能


## 三、API
[https://app.swaggerhub.com/apis/andrewpqc/muxi-url-shorter/1.0.0](https://app.swaggerhub.com/apis/andrewpqc/muxi-url-shorter/1.0.0)

## 四、TODO