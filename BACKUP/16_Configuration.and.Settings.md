# [Configuration and Settings](https://github.com/SylverQG/Blogs/issues/16)

# fnos 无网线初始化/忘记密码

1. 开机进入grub的时候按上`up`下`down`方向
2. 光标停在第一个选项（一般是`Debain GNU/Linux`）
3. 按`e`进入编辑模式
4. 找到`linux`行，`ctrl+e`将光标移动到行末 添加`init=/bin/bash`
5. `ctrl+x` 保存并启动
6. 进入命令行模式开头一般是`root:/#`
7. 输入`mount -o remount,rw /` 将根目录挂在为读写模式
8. 输入`psswd root` (这里的root是无网线时的账号，或者还可以是你之前设置的管理员账号)
9. 输入新密码，看到`passwd: password updated successfully`为设置成功
10. 输入`sync` 将数据写入硬盘，然后可以`reboot -f`重启设备
11. 如果是重置管理员密码，现在可以从别的设备进入fnos的ip使用了
12. 如果是无网线时初次配置，重启后进入登录界面`xxx login: ` 输入`root`以及密码登录root用户
13. 输入`nmcli device wifi list` 列出所有wifi,如果没有结果则无wifi，建议使用有线网卡网线或者添加无线网卡
14. 输入`nmcli device wifi connect "wifi名称" password "wifi密码"`
15. 连接成功后使用命令`ifconfig`查看ip，使用别的设备进入fnos的ip使用