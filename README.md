# Bangumi-Let-Me-Watch [![bangumi](http://bgm.tv/img/ico/bgm80-15.png)](http://bgm.tv)
自动将 bangumi 日期到了的“想看”动画标为“在看”。

## 使用方法
1. Use this template 或 Fork 本仓库
2. 在新建的自己的仓库中，进入仓库 Settings → Secrets and variables → Actions，点击 "New repository secret" 添加：
   - BGMI_USERNAME：自己的 bangumi ID
   - BGMI_API_KEY：自己的 Access Token，可以在[此处](https://next.bgm.tv/demo/access-token/create)获得，过期后需重新设置
3. 前往 Settings → Actions 确保允许自动运行
4. 脚本会在每天UTC时间12:00（北京时间20:00）自动运行
   - 可以自行修改 `.github/workflows/bangumi-sync.yml` 中的 `cron` 自定义运行时间
