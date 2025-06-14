# Bangumi-Let-Me-Watch [![bangumi](http://bgm.tv/img/ico/bgm80-15.png)](http://bgm.tv)
自动将 bangumi 日期到了的“想看”动画标为“在看”。

## 使用方法（GitHub Actions）
1. Use this template 或 Fork 本仓库
2. 在新建的自己的仓库中，进入仓库 Settings → Secrets and variables → Actions，点击 "New repository secret" 添加：
   - BGMI_USERNAME：自己的 bangumi ID
   - BGMI_API_KEY：自己的 Access Token，可以在[此处](https://next.bgm.tv/demo/access-token/create)获得，过期后需重新设置
3. 前往 Settings → Actions 确保允许自动运行
4. 修改 `.github/workflows/bangumi-sync.yml`，在 `on:` 下一行增加 `cron` 自定义每天运行时间，格式为UTC时间的 `分 时 * * *`，例如，`0 12 * * *` 表示每天UTC时间12:00（北京时间20:00）
   - 时间设置得尽量随机分散，避免同时请求橄榄 bangumi 服务器，可以复制下面的模板粘贴：
```yaml
  schedule:
    - cron: '分 时 * * *'
```

## 问题
- 标记为“在看”的时间线不会显示先前的短评（https://github.com/bangumi/server/issues/856 ）
- 不考虑支持受限条目
