# Full 模板的客户端 DNS

`OpenClash_Client_DNS.yaml` 保留转换后端原有的非 DNS 基础设置，明确不生成 `dns` 段。Full INI 通过 `clash_rule_base` 使用它，避免后端默认注入境外域名 DNS 策略、公共 DNS 和 fallback。

云端模板继续提供分类、策略组和分流规则。网口名称、上游 DNS 地址及直连 DNS 由 OpenClash 客户端管理；模板不固定学校、运营商或接口。

最终选中 `DIRECT` 时使用哪台上游 DNS，仍取决于客户端的直连解析器设置。客户端需要动态提供当前上游 DNS，且不让直连解析遵循境外域名 DNS 策略。云端模板不能从转换服务器上发现客户端的 WAN DNS，也不能覆盖 OpenClash 本机随后追加的 DNS 设置。

此 INI 需要支持 `clash_rule_base` 的 SubConverter 后端。当前 `hadesp-sub-convert` 使用的后端已支持该字段。基础配置引用固定到 Git 提交，便于核对和回退。
