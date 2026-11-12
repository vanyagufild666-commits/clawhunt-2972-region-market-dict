"""Generate JSON deliverable for task 2972 (地域字典 JSON + xlsx)."""
import json

content = json.load(open('content.json', encoding='utf-8'))
out = {}
for s in content['sheets'][:2]:
    items = []
    for r in s['rows']:
        item = dict(zip(s['headers'], r))
        item['排序值'] = int(item['排序值'])
        if item['上级编码'] is None:
            item['上级编码'] = None
        items.append(item)
    out[s['title']] = items

# flat list combining
flat = out['国内地域（省级+重点城市）'] + out['海外区域与汇总项']
json.dump(flat, open('地域与目标市场字典.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

codes = {i['编码'] for i in flat}
dangling = [i['编码'] for i in flat if i['上级编码'] and i['上级编码'] not in codes]
assert not dangling, f'dangling parent: {dangling}'
cn_cities = [i for i in flat if i['上级编码'] and (i['上级编码'].startswith('REG_CN') or i['上级编码'] == 'REG_CN')]
print('json written |', len(flat), 'items | parents ok | cn-level entries:', len(cn_cities))
