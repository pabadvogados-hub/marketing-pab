"""
Atualiza os dados do dashboard da campanha Corredor Logistico.
Repuxa a performance por territorio e regrava CAMPANHA/_dash_corredor.json,
depois injeta no dashboard_corredor.html.

Uso: python MARKETING/atualizar_corredor.py
"""
import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for line in open(os.path.join(RAIZ, 'config', '.env'), encoding='utf-8', errors='ignore'):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
sys.path.insert(0, os.path.join(RAIZ, 'INTEGRACOES'))
import meta_ads_integration as meta

CAMP = '000000000000'
D = os.path.join(RAIZ, 'MARKETING', 'CAMPANHA')


def main():
    tot = meta.resumo_campanha(CAMP, 'maximum') or {}
    terr = []
    for r in meta.insights(CAMP, 'adset', 'maximum',
                           fields='adset_name,spend,impressions,clicks,ctr,actions,cost_per_action_type'):
        terr.append({'nome': r.get('adset_name', ''), 'gasto': round(float(r.get('spend', 0)), 2),
                     'conv': meta.conversas(r.get('actions')), 'cpconv': meta.custo_por(r.get('cost_per_action_type')),
                     'imp': int(r.get('impressions', 0)), 'cliques': int(r.get('clicks', 0)),
                     'ctr': round(float(r.get('ctr', 0)), 2)})
    if not terr:
        d = meta._get(f'{CAMP}/adsets', {'fields': 'name,daily_budget,effective_status'})
        for a in d.get('data', []):
            terr.append({'nome': a.get('name', ''), 'gasto': 0, 'conv': 0, 'cpconv': 0, 'imp': 0,
                         'cliques': 0, 'ctr': 0, 'budget': int(a.get('daily_budget', 0)) // 100,
                         'status': a.get('effective_status')})
    jonck = {'conversas': 190, 'cpconv': 7.18, 'gasto': 1365.00, 'ctr': 4.16}
    out = {'campanha': tot, 'territorios': terr, 'jonck': jonck, 'camp_id': CAMP}
    json.dump(out, open(os.path.join(D, '_dash_corredor.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    # injeta no html
    htmlp = os.path.join(D, 'dashboard_corredor.html')
    html = open(htmlp, encoding='utf-8').read()
    import re
    novo = 'const DATA = ' + json.dumps(out, ensure_ascii=False) + ';'
    html = re.sub(r'const DATA = .*?;\n', novo + '\n', html, count=1, flags=re.S)
    open(htmlp, 'w', encoding='utf-8').write(html)
    print('Atualizado. Territorios:')
    for t in terr:
        print(f"  {t['nome'][:40]}: gasto R${t['gasto']} | {t['conv']} conv")


if __name__ == '__main__':
    main()
