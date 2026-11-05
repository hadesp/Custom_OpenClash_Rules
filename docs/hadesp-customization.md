# hadesp Full customization

This fork retains Aethersailor's upstream history and CC BY-SA 4.0 license. Changes are confined to the Full INI/companion YAML, two academic rule providers, this audit and regression CI. Main has 64 groups and 64 rulesets; group count is independent of a converter's ruleset limit.

Academic defaults to `🎯 全球直连`. Scholar uses `Google_Scholar`, ahead of the overseas academic provider; original GeoSite Scholar inclusion is removed. Private rules remain first, academic exceptions precede broad custom rules to avoid accidental overlap. Other classification rules retain their original order. The audit JSON records source SHAs, every academic source and excluded candidate. Unverified CloudFront names, broad educational suffixes and Chinese academic sites are not added.

High multiplier membership and automatic group exclusion are computed together in the hadesp Worker, without filtering the entire subscription. Empty test groups visibly contain `REJECT`. The INI is intended for that backend; a generic converter must not be assumed to implement the strict multiplier extension.

The companion YAML has a deliberately invalid public Provider placeholder. Do not replace router configuration or export real subscription data to fill this file. Only the conversion-service and remote-INI fields are intended to change on the router. Mainland bypass remains dependent on existing router settings; DIRECT alone does not bypass the kernel.

Service source and current release status: https://github.com/hadesp/openclash-subconverter-worker . A deployed test endpoint is not final acceptance. See that project's acceptance report before use.

Synchronize upstream on a maintenance branch, preserve these personalized files, rerun the reproducible build in the converter project, inspect count/audit changes and run both CI suites before updating main. Do not force-reset this fork to upstream.
