"""Public-template regression checks; no router configuration or subscriptions."""
from pathlib import Path
import re
root = Path(__file__).resolve().parent.parent
ini = root.joinpath('cfg/Custom_Clash_Full.ini').read_text(encoding='utf-8')
rules = re.findall(r'^ruleset=(.+)$', ini, re.M)
groups = re.findall(r'^custom_proxy_group=(.+)$', ini, re.M)
assert len(rules) == 64, len(rules)
assert len(groups) == 63, len(groups)
names = [g.split('`')[0] for g in groups]
assert len(set(names)) == 63
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
assert len(re.findall(r'^  - name:', yaml, re.M)) == 64
assert 'example.invalid/placeholder' in yaml
print('63 Full INI groups, 64 ordered rulesets, filtering groups, academic exclusions and companion YAML checks passed.')
