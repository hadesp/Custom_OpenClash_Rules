# Full 模板的 AI 分流

AI 规则优先于通用自定义直连、代理以及 Google/Microsoft 分类，具体 AI 服务优先于国内/国外 AI 兜底。现有策略组名称、节点选项及选择顺序不变。

| 分组 | 规则来源与范围 |
| --- | --- |
| 🤖 ChatGPT | `ChatGPT_Domain.yaml`，覆盖 ChatGPT、OpenAI API、Sora、上传、静态资源及语音相关域名；另补 OpenAI 官方网络文档列出的 `cdn.openaimerge.com` |
| 🤖 Gemini | 在线 `google-gemini.yaml` 加 `Gemini_Extra_Domain.yaml`，包括 Gemini、Antigravity、AI Studio、Gemini API、NotebookLM、Code Assist、Jules、Flow 等 Google AI 服务 |
| 🤖 Claude | 在线 `anthropic.yaml`，包括 Claude/Anthropic 及其内容域名 |
| 🤖 Copilot | 在线 `bing.yaml`，保留原先 Bing/Copilot 的归类范围 |
| 🤖 Grok | 在线 `xai.yaml` |
| 🤖 国内AI服务 | 在线 `category-ai-cn.yaml`，保留默认直连 |
| 🤖 国外AI服务 | 在线 `category-ai-!cn.yaml`，接收未被专用 AI 组匹配的其他海外 AI 服务 |

在线域名规则来自 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat/tree/meta/geo/geosite)，每 8 小时检查更新，不依赖设备内置 GeoSite 的更新时间。ChatGPT 域名快照与 Antigravity 补充域名由本仓库维护，来源记录在各 YAML 文件开头。

Antigravity 按 Google 服务端域名进入 Gemini 组；在 Antigravity 中切换模型名称不会将同一个 Google API 请求改送其他组。企业版的 global、US、EU 和 mTLS API 域名也包含在补充规则中。

Google 登录、支付、通用 Google API、验证码等共享域名保留原有分类，不把整个 `googleapis.com`、`google.com` 或 `cloudflare.com` 导向单个 AI 组。已有广告过滤规则仍具有优先级。

本修改不向生成配置写入 DNS、不改变节点选择，也不等同于验证某个账号、节点或地区能使用所有 AI 产品。

核对资料

- [OpenAI 网络要求](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Antigravity 企业版端点与网络要求](https://antigravity.google/docs/enterprise)
- [Gemini API](https://aistudio.google.com/docs/get-started)

为兼容现有转换后端，输入规则采用 YAML。该后端不会为 `.mrs` 链接补写 `format: mrs`，因此 Full INI 不直接引用 MRS，避免客户端将二进制规则按 YAML 解析为空。
