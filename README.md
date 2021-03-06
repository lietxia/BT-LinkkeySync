# macOS蓝牙与windows10同步
* 应该支持macOS 10.12~macOS11，不过我只测了macOS10.15.7(Catalina)和macOS11.1(BigSur)
* 同时支持python3和python2，因为python3不是默认装的，这里用python2来示范。
* **记得点`star`**

1. 在windows下配对蓝牙设备
2. 在macOS下配对蓝牙设备
3. macOS打开终端(Terminal)运行以下脚本（3行一起复制，一起粘贴.会要求输入密码）
   ```
   cd ~/Desktop/; curl -o BT-LinkkeySync.py \
   https://cdn.jsdelivr.net/gh/lietxia/BT-LinkkeySync@1.1.0/BT-LinkkeySync.py \
   && sudo python BT-LinkkeySync.py
   ```
4. 桌面上会产生 `btkeys.reg` ，把他放到 windows能访问的目录
5. 启动windows，关掉windows的蓝牙
6. 下载PStools [程序网站](https://docs.microsoft.com/sysinternals/downloads/psexec) or [直接下载](https://download.sysinternals.com/files/PSTools.zip)
   存到 `C:/pstools/`，保证`C:/pstools/`下面有`psexec.exe` (其他地方也行)
7. 按`windows键`+`X`，弹出菜单选`powershell(管理员模式)`，运行脚本(如果换了目录，自行把`C:/pstools/`改成相应的目录）
   ```
   C:/pstools/psexec.exe -s -i regedit
   ```
8. 选`文件`->`导入`把`btkeys.reg`导入进去
9.  重启win10
10. 打开蓝牙，你的蓝牙设备就能在双系统愉快的玩耍了。

# BT-LinkkeySync
Script to synchronize bluetooth link keys from macOS to windows.
It generates a registry file for windows on macOS, which can afterwards be imported with the tool regedit in windows.

## Instructions
1. Pair all your bluetooth devices to your Windows (e.g. keyboard, mouse, headphones)
2. Pair all your bluetooth devices to your Mac (e.g. keyboard, mouse, headphones)
3. Open the Terminal and run the script with (you will be asked for your password)
   ```
   cd ~/Desktop/; curl -o BT-LinkkeySync.py \
   https://cdn.jsdelivr.net/gh/lietxia/BT-LinkkeySync@1.1.0/BT-LinkkeySync.py \
   && sudo python BT-LinkkeySync.py
   ```
4. Store the generated file `btkeys.reg` file to a location accessible by windows.
5. Boot windows and close your bluetooth devices
6. Download PStools [website_download](https://docs.microsoft.com/sysinternals/downloads/psexec) or [direct_download](https://download.sysinternals.com/files/PSTools.zip)
   and store it to `C:/pstools/`
7. Press `Windows key` + `X` and select powershell (admin). Run the command:
   `C:/pstools/psexec.exe -s -i regedit`
8. Import the file `btkeys.reg`
9.  restart windows
10. Use your keyboard on macOS and Windows

## Information
Test Environment:

* OSx86 Hackintosh with DW1820A
* macOS Catalina 10.15.7/macOS BigSur 11.1
* Windows 10 20H2
* Python 3.8/Python 2.7

## Limitations
BT 4.0 LE/Smart Devices (e.g. Logitech MX Master) do not work yet.
If you know how to get it working feel free to contribute :)

## TODO's
Try the other way round (Pair on Windows and import in macOS) maybe get Bluetooth 4.0 LE Working

## Credits
Related [Blog Post on InsanelyMac](http://www.insanelymac.com/forum/topic/268837-dual-boot-bluetooth-pairing-solved/) of camoguy

## Links
* [Dual Boot Bluetooth Pairing Solved](http://www.insanelymac.com/forum/topic/268837-dual-boot-bluetooth-pairing-solved/)
* [Dual pairing in OS X and Windows](https://discussions.apple.com/thread/3113227?start=0&tstart=0)
* [OS-X-Bluetooth-Pairing-Value-To-Windows-Value](https://github.com/Soorma07/OS-X-Bluetooth-Pairing-Value-To-Windows-Value)
