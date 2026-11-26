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

在线域名规则由本仓库镜像 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat/tree/meta/geo/geosite)，不依赖设备内置 GeoSite 的更新时间。`Update Full cloud AI rules` 工作流每 8 小时运行，也支持手动运行；通过校验且内容有变化时才提交更新。

客户端继续每 8 小时检查规则文件更新；机场 HTTP Provider 的 4 小时刷新、分组的 10 分钟测速不变。切换到本仓库镜像地址后，首次需要重新订阅一次，此后规则内容由规则 Provider 自动更新，不需要为了域名更新而重新部署 Worker。

同步脚本为 `py/update_full_ai_rules.py`，同步 ChatGPT、Gemini、Claude、Copilot、Grok、国内/国外 AI 七份上游列表。`rule/ai/overrides.json` 独立保存人工核实的补充域名，生成文件不会丢掉这些补充。Antigravity 企业接口补充仍来自官方文档，新增的未知官网端点不会凭空自动推测。

下载失败、返回 HTML/空列表、失去必要域名、范围扩大到整个 Google API 等共享根域名，或列表一次缩减超过 30% 时，工作流失败并不发布，仓库上一版继续供客户端使用。任何一份上游出错，都不提交半套更新。无变化时不创建提交。

这项自动化更新域名内容，不自动改变策略组、节点选择、DNS 或服务分流顺序。其他在线规则继续按其原有上游更新；本机 GeoSite/GeoIP 的更新仍由客户端管理。

Antigravity 按 Google 服务端域名进入 Gemini 组；在 Antigravity 中切换模型名称不会将同一个 Google API 请求改送其他组。企业版的 global、US、EU 和 mTLS API 域名也包含在补充规则中。

Google 登录、支付、通用 Google API、验证码等共享域名保留原有分类，不把整个 `googleapis.com`、`google.com` 或 `cloudflare.com` 导向单个 AI 组。已有广告过滤规则仍具有优先级。

本修改不向生成配置写入 DNS、不改变节点选择，也不等同于验证某个账号、节点或地区能使用所有 AI 产品。

核对资料

- [OpenAI 网络要求](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Antigravity 企业版端点与网络要求](https://antigravity.google/docs/enterprise)
- [Gemini API](https://aistudio.google.com/docs/get-started)

为兼容现有转换后端，输入规则采用 YAML。该后端不会为 `.mrs` 链接补写 `format: mrs`，因此 Full INI 不直接引用 MRS，避免客户端将二进制规则按 YAML 解析为空。
