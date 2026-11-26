"""Public-template regression checks; no router configuration or subscriptions."""
from pathlib import Path
import re
root = Path(__file__).resolve().parent.parent
ini = root.joinpath('cfg/Custom_Clash_Full.ini').read_text(encoding='utf-8')
base_urls = re.findall(r'^clash_rule_base=(.+)$', ini, re.M)
assert len(base_urls) == 1
assert re.fullmatch(r'https://raw\.githubusercontent\.com/hadesp/Custom_OpenClash_Rules/[0-9a-f]{40}/cfg/base/OpenClash_Client_DNS\.yaml', base_urls[0])
base = root.joinpath('cfg/base/OpenClash_Client_DNS.yaml').read_text(encoding='utf-8')
assert not re.search(r'^dns\s*:', base, re.M), 'The cloud template must leave DNS configuration to OpenClash'
rules = re.findall(r'^ruleset=(.+)$', ini, re.M)
groups = re.findall(r'^custom_proxy_group=(.+)$', ini, re.M)
assert len(rules) == 64, len(rules)
assert not any('.mrs' in r for r in rules), 'The deployed backend omits the required MRS provider format'
assert len(groups) == 62, len(groups)
names = [g.split('`')[0] for g in groups]
assert len(set(names)) == 62
assert '非标端口' not in ini and 'Custom_Port_Direct' not in ini
assert '🇳🇱 荷兰节点' not in names and '🇹🇷 土耳其节点' not in names
assert '[]🇳🇱 荷兰节点' not in ini and '[]🇹🇷 土耳其节点' not in ini
for name in ['🛑 广告过滤', '🍃 应用净化']:
    assert next(g for g in groups if g.startswith(name + '`')).split('`')[1:] == ['select', '[]REJECT', '[]DIRECT']
for filename, expected in {
    'Developer_Container.yaml': ['GEOSITE,docker', 'GEOSITE,category-container'],
    'Social_Media_IP.yaml': ['GEOIP,twitter,no-resolve', 'GEOIP,facebook,no-resolve'],
}.items():
    content = root.joinpath('rule', filename).read_text(encoding='utf-8')
    assert re.findall(r'^  - (.+)$', content, re.M) == expected
    assert any(filename in r for r in rules)
assert not any(',[]OR,' in r for r in rules)
generic_proxy = next(i for i, r in enumerate(rules) if 'Custom_Proxy_Domain.yaml' in r)
for service in ['💾 OneDrive', '📢 谷歌FCM']:
    assert next(i for i, r in enumerate(rules) if r.startswith(service + ',')) < generic_proxy
for filename, required in {
    'Emby_Full.yaml': ['GEOSITE,category-emby', 'DOMAIN-SUFFIX,emby.media'],
    'Shopping_Overseas.yaml': ['GEOSITE,category-ecommerce', 'DOMAIN-SUFFIX,media-amazon.com'],
}.items():
    content = root.joinpath('rule', filename).read_text(encoding='utf-8')
    assert all(entry in content for entry in required)
    assert any(filename in r for r in rules)
shopping = root.joinpath('rule/Shopping_Overseas.yaml').read_text(encoding='utf-8')
shopping_pattern = re.search(r'^  - DOMAIN-REGEX,(.+)$', shopping, re.M).group(1)
for host in ['amazon.com', 'www.amazon.com', 'www.amazon.co.jp', 'amazon.com.be', 'amazon.ie', 'amazon.co.za']:
    assert re.fullmatch(shopping_pattern, host), host
for host in ['aws.amazon.com', 'msh.amazon.com', 'amazon.cn', 'amazon.com.evil.test', 'notamazon.com']:
    assert not re.fullmatch(shopping_pattern, host), host
ai_rules = [r for r in rules if r.startswith('🤖 ')]
assert len(ai_rules) == 8
assert all(',clash-domain:' in r and r.endswith(',28800') for r in ai_rules)
assert all('https://raw.githubusercontent.com/hadesp/Custom_OpenClash_Rules/main/rule/' in r for r in ai_rules)
assert rules.index(ai_rules[-1]) < next(i for i, r in enumerate(rules) if 'Custom_Direct_Domain' in r)
assert rules.index(next(r for r in ai_rules if r.startswith('🤖 Gemini,') and 'google-gemini.yaml' in r)) < rules.index(next(r for r in ai_rules if r.startswith('🤖 国外AI服务,')))
assert not any(re.search(r',\[\]GEOSITE,(openai|google-gemini|anthropic|bing|xai|category-ai-!?cn)$', r) for r in rules)
import sys
sys.path.insert(0, str(root / 'py'))
from update_full_ai_rules import check as check_ai_providers
check_ai_providers(root)
for filename, required_domains in {
    'ChatGPT_Domain.yaml': ['+.chatgpt.com', '+.openai.com', '+.oaistatic.com', '+.oaiusercontent.com', '+.chatgpt.livekit.cloud', 'cdn.openaimerge.com'],
    'Gemini_Extra_Domain.yaml': ['+.antigravity.google.com', 'businessaicode.googleapis.com', 'businessaicode.us.rep.googleapis.com', 'aiplatform.googleapis.com'],
}.items():
    content = root.joinpath('rule', filename).read_text(encoding='utf-8')
    domains = re.findall(r'^  - (.+)$', content, re.M)
    assert len(domains) == len(set(domains))
    assert set(required_domains).issubset(domains)
    assert not set(domains).intersection(['+.google.com', '+.googleapis.com', '+.gstatic.com', '+.cloudflare.com', 'accounts.google.com'])
    assert any(filename in r for r in ai_rules)
assert '🔥 高倍率节点' in names and '🐢 低倍率节点' in names
academic = next(g for g in groups if g.startswith('📚 学术资源`'))
assert academic.startswith('📚 学术资源`select`[]🎯 全球直连`')
assert not any('category-scholar-!cn' in r for r in rules)
assert any('Google_Scholar.yaml' in r for r in rules)
payload = root.joinpath('rule/Academic_Overseas_No_Google.yaml').read_text(encoding='utf-8')
for forbidden in ['DOMAIN-SUFFIX,edu\n', 'DOMAIN-SUFFIX,edu.cn', 'DOMAIN-SUFFIX,ac.cn', 'cnki.net', 'wanfangdata.com.cn', ',cloudfront.net', ',cloudflare.com', 'scholar.google', ',bmc.com']:
    assert forbidden not in payload, forbidden
for required in ['nature.com', 'acs.org', 'rsc.org', 'wiley.com', 'science.org', 'sciencedirect.com', 'webofscience.com', 'silverchair-cdn.com', 'sciencedirectassets.com', 'els-cdn.com']:
    assert required in payload, required
yaml = root.joinpath('cfg/yaml/Custom_Clash_Full.yaml').read_text(encoding='utf-8')
assert len(re.findall(r'^  - name:', yaml, re.M)) == 63
assert '非标端口' not in yaml and 'Custom_Port_Direct' not in yaml
assert 'example.invalid/placeholder' in yaml
print('62 Full INI groups, 64 ordered rulesets, online AI providers, no port override, client-controlled DNS and academic checks passed.')
