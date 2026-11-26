# Full 云端分流核对记录

2026-11-26 对 `cfg/Custom_Clash_Full.ini` 进行核对。生效路径是 Worker 读取 Full INI，再输出 Mihomo 配置；不更换转换后端，不修改客户端 DNS。

## 修复

- AI 分类改用在线规则，避免 ChatGPT、Gemini/Antigravity 等新入口受旧版客户端 GeoSite 限制。AI 专用规则位于通用自定义规则之前，国内/国外 AI 保留各自兜底。
- 通用自定义代理域名规则移到专用服务之后，修复 `onedrive.live.com`、`mtalk.google.com` 被手动选择组提前匹配的问题；原有代理补充域名继续保留。
- Emby 保留上游服务端域名并补充 `emby.media`。
- 国外电商保留上游分类并补充 Amazon 各区域购物首页与图片资源，购物首页正则不覆盖 AWS、Prime Video 子域名或中国站。
- 修复在线二进制规则格式声明缺失。现有后端不会自动给 MRS 输入补写 `format: mrs`，实测会让对应规则集加载为 0 条；Full INI 改用同源 YAML，使输出能直接被 Mihomo 正确读取。

## 验证范围

- Full INI 为 62 个策略组、64 条 ruleset 配置；所有分组定义及节点选项与修改前逐条一致。
- 21 个实际引用的在线规则文件均能下载，Mihomo 均成功加载且规则数量非零。
- 使用真实规则文件与本机 Mihomo 对 159 个域名/IP 执行真实首条命中测试，全部符合预期。测试出口为本机回环 HTTP 接收器，不向这些网站发起实际业务请求，不使用机场订阅或账号凭据。
- 测试包含 AI、学术及 Google Scholar、开发者、即时通讯、OneDrive、Google FCM、流媒体、游戏平台、测速、电商、加密货币、广告、私网/国内地址、Telegram/Google/Netflix/社交媒体 IP 和未知域名兜底。
- 核对 ChatGPT 与 Antigravity 相似但不属于其域名的主机名，确认没有扩大为整个 Google API 或 Cloudflare 域名。
- 南大、校园网或运营商 DNS 地址不写入云端模板，客户端 DNS 控制方式保持不变。
- AI Rule Provider 改由现有 Worker 自动获取并校验上游，失败时使用有效缓存或已验证后备数据，不依赖 GitHub Actions 能执行。

这些检查验证规则加载及分类命中，不代表已验证所有账号、地区、节点、登录、付费权限或语音功能均可用。
