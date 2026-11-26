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

AI 规则由现有 Worker 的 `/rules/ai/*.yaml` 接口供给。路由器自动刷新规则时，Worker 获取 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat/tree/meta/geo/geosite) 的最新列表并校验，不依赖客户端 GeoSite 更新或 GitHub Actions 执行。

客户端继续每 8 小时检查规则文件更新；机场 HTTP Provider 的 4 小时刷新、分组的 10 分钟测速不变。首次切换到 Worker 规则接口需要重新订阅一次，此后上游域名更新由规则 Provider 自动获取，不需要重新部署 Worker。

Worker 获取 ChatGPT、Gemini、Claude、Copilot、Grok、国内/国外 AI 七份上游列表，并合并 `rule/ai/overrides.json` 中人工核实的补充域名。Antigravity 企业接口补充仍来自官方文档，新增的未知官网端点不会凭空自动推测。

公开规则在 Worker 缓存 5 分钟，最近有效版本在缓存可用时保留最多 7 天。下载失败、返回 HTML/空列表、失去必要域名、范围扩大到整个 Google API 等共享根域名，或列表一次缩减超过 30% 时，接口返回最近有效缓存；没有有效缓存时使用仓库镜像或内置已校验快照，避免下发空规则。缓存只保存公开规则，不保存机场订阅和最终订阅 YAML。

`py/update_full_ai_rules.py` 与 `Update Full cloud AI rules` 工作流提供可选的仓库镜像维护方式：每 8 小时同步，通过整批校验后有变化才提交，任何来源失败都不发布半套文件。Worker 的自动更新不要求该工作流能执行，也不需要 GitHub 写入密钥。

这项自动化更新域名内容，不自动改变策略组、节点选择、DNS 或服务分流顺序。其他在线规则继续按其原有上游更新；本机 GeoSite/GeoIP 的更新仍由客户端管理。

Antigravity 按 Google 服务端域名进入 Gemini 组；在 Antigravity 中切换模型名称不会将同一个 Google API 请求改送其他组。企业版的 global、US、EU 和 mTLS API 域名也包含在补充规则中。

Google 登录、支付、通用 Google API、验证码等共享域名保留原有分类，不把整个 `googleapis.com`、`google.com` 或 `cloudflare.com` 导向单个 AI 组。已有广告过滤规则仍具有优先级。

本修改不向生成配置写入 DNS、不改变节点选择，也不等同于验证某个账号、节点或地区能使用所有 AI 产品。

核对资料

- [OpenAI 网络要求](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Antigravity 企业版端点与网络要求](https://antigravity.google/docs/enterprise)
- [Gemini API](https://aistudio.google.com/docs/get-started)

为兼容现有转换后端，输入规则采用 YAML。该后端不会为 `.mrs` 链接补写 `format: mrs`，因此 Full INI 不直接引用 MRS，避免客户端将二进制规则按 YAML 解析为空。
