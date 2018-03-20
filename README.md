# ACM 训练总结系统

## 开发计划

1. Status 页面的排版：

第一行：h1标题，"Contest Detail"

接下来是一张两列的表格

"Contest Name" & contest\_name

"Contest Source" & contest\_source

"Contest Start Time" & contest\_start\_time 
请注意，这里的时间按照 2018-01-01 00:00:00 这样的格式显示，而不要以 March 10, 2018, noon 的方式显示

"Number of Problems" & num

接下来是总结。

2. Edit Status 页面的排版：

第一行：h1 标题，"Edit Summary"

接下来是一张 5 列的表格

Problem & Status & team\_member\_1 & team\_member\_2 & team\_member\_3

A & Solved/Upsolved/Not solved & checkbox1 & checkbox2 & checkbox3

B & Solved/Upsolved/Not solved & checkbox1 & checkbox2 & checkbox3

...

接下来为 submit 按钮。

3. /contests/ 页面，添加比赛按钮在 Contests 大标题的正下方。

/contests/ 页面按contest_id递减排序

如果可以，每页显示 20 个比赛，在页面最下方加上翻页按钮。可以添加一个 url : contests/page/<page_id> 来识别第几页。

4. 添加比赛以及编辑比赛的页面，文本框需对齐。可以用表格来实现。

5. 时间的显示：

/contests/ 页面的时间按照 2018-01-01 00:00:00 这样的格式显示，而不要以 March 10, 2018, noon 的方式显示。

/contests/<int:contest_id> 页面的时间按照 2018-01-01 00:00:00 这样的格式显示，而不要以 March 10, 2018, noon 的方式显示。

/contests/add_contest 页面的 Contest Start Time 使用插件来输入时间，只需用鼠标点，而不需键盘输入

/contests/<int:contest_id>/edit 页面的 Contest Start Time 使用插件来输入时间，只需用鼠标点，而不需键盘输入

6. 用户列表界面：

用户列表可以使用 url ： /users/ ，翻页功能可使用 /users/page/<page_id>

用户列表第一行为h1标题： Our Teams

接下来是一张 6 列的表格：

Username & Team Name & Team\_member\_1 & Team\_member\_2 & Team\_member\_3 & View

View 为一个指向该用户资料的超链接。

每页显示 20 个用户

最下方显示翻页按钮。

7. 用户详情界面：

第一行h1大标题：Team team_name

接下来是5行2列的表格：

"Username" & username

"Team Name" & team_name

"Team Member 1" & team\_member\_1

"Team Member 2" & team\_member\_2

"Team Member 3" & team\_member\_3

接下来是队伍介绍

接下来是参加过的比赛，按 contest_id 倒序排序。请将 Onsite 的比赛打上一个特殊的标记（比如在Contest Name 后面加上一个五角星之类的）

8. 文本框的升级：

在以下页面的描述及总结编辑框，文本框升级为 MarkDown 编辑器

/users/modify_profiles/

添加 summary

编辑 summary

9. 为配合文本框的升级，以下页面需支持 MarkDown ：

status 显示界面

/users/profile/user_id/ 用户详情界面

## 开发背景

中山大学 ACM 集训队目前正在使用原有的 ACM 训练总结系统（ http://www.sysuteam.com ）。这个系统能帮助教练了解集训队的做题情况。然而，这个系统有一些不足之处，例如每支队伍没有自己的主页，队伍不能在上面写总结、发题解。

我参考了一下浙大的队伍主页，包含队伍信息、训练帐号、目标、友情链接、杂事杂项（一些小结和提醒）、板子整理、个人训练、团队训练、比赛记录等信息。他们的队伍主页支持 MarkDown 语法，并且有版本控制（即可以恢复到历史版本）。对于每场比赛，他们都有总结。我们决心做出跟浙大一样好的 ACM 训练总结系统。

## 项目成员

王凯祺

刘梓晖

田启睿

区炜彬

## 拟定功能

比赛的创建与管理

队伍管理

队伍主页（含版本控制），底部包含该队伍参与的所有比赛及总结

比赛列表，及该比赛下每支队的做题情况

## 实现方法

Web 应用框架：Django

数据库：Sqlite3

