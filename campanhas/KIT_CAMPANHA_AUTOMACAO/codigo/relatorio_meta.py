"""
Relatorio de campanhas Meta Ads para o marketing PAB.

Usa INTEGRACOES/meta_ads_integration.py (token System User permanente).

Uso:
  python MARKETING/relatorio_meta.py                 # resumo da semana (campanha Motoristas)
  python MARKETING/relatorio_meta.py --contas        # lista todas as contas
  python MARKETING/relatorio_meta.py --campanhas     # lista campanhas ativas da CA01
  python MARKETING/relatorio_meta.py --dashboard     # regenera dados do dashboard (CAMPANHA/_dashboard_data.json)
"""
import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _carregar_env():
    envp = os.path.join(RAIZ, 'config', '.env')
    if os.path.exists(envp):
        for line in open(envp, encoding='utf-8', errors='ignore'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_carregar_env()
sys.path.insert(0, os.path.join(RAIZ, 'INTEGRACOES'))
import meta_ads_integration as meta

CAMP_MOTORISTAS = '000000000000'


def resumo_semana():
    c = meta.achar_campanha(nome_parcial='Motoristas') or {'id': CAMP_MOTORISTAS, 'name': 'AK Motoristas'}
    cid = c.get('id', CAMP_MOTORISTAS)
    print(f"\nCampanha: {c.get('name')}")
    agora = meta.resumo_campanha(cid, 'last_7d')
    print("\n=== ULTIMOS 7 DIAS ===")
    for k, v in agora.items():
        print(f"  {k}: {v}")
    return agora


def listar_contas():
    print("\n=== CONTAS DE ANUNCIO ===")
    for c in meta.listar_contas():
        gasto = int(c.get('amount_spent', 0)) / 100
        print(f"  {c.get('name')[:40]:42} | {c.get('id')} | R$ {gasto:,.2f}")


def listar_campanhas():
    print("\n=== CAMPANHAS ATIVAS (CA01) ===")
    for c in meta.listar_campanhas(ativas=True):
        print(f"  {c.get('name')[:55]} | {c.get('objective')}")


def gerar_dashboard():
    """Regenera CAMPANHA/_dashboard_data.json com dados frescos."""
    cid = CAMP_MOTORISTAS
    daily = []
    for r in meta.insights(cid, 'campaign', 'last_30d', time_increment=1,
                           fields='spend,impressions,clicks,ctr,cpc,actions'):
        daily.append({'date': r['date_start'][5:], 'spend': round(float(r.get('spend', 0)), 2),
                      'conv': meta.conversas(r.get('actions')), 'ctr': round(float(r.get('ctr', 0)), 2),
                      'cpc': round(float(r.get('cpc', 0)), 2), 'imp': int(r.get('impressions', 0))})
    lt = meta.insights(cid, 'campaign', 'maximum')
    lt = lt[0] if lt else {}

    def a(acts, t):
        for x in (acts or []):
            if x['action_type'] == t:
                return int(float(x['value']))
        return 0
    life = {'spend': round(float(lt.get('spend', 0)), 2), 'imp': int(lt.get('impressions', 0)),
            'reach': int(lt.get('reach', 0)), 'freq': round(float(lt.get('frequency', 0)), 2),
            'clicks': int(lt.get('clicks', 0)), 'ctr': round(float(lt.get('ctr', 0)), 2),
            'cpc': round(float(lt.get('cpc', 0)), 2), 'conv': meta.conversas(lt.get('actions')),
            'cpconv': meta.custo_por(lt.get('cost_per_action_type')),
            'reply': a(lt.get('actions'), 'onsite_conversion.messaging_first_reply'),
            'd2': a(lt.get('actions'), 'onsite_conversion.messaging_user_depth_2_message_send'),
            'd3': a(lt.get('actions'), 'onsite_conversion.messaging_user_depth_3_message_send'),
            'video': a(lt.get('actions'), 'video_view')}
    adsets = [{'name': r.get('adset_name', ''), 'spend': round(float(r.get('spend', 0)), 2),
               'conv': meta.conversas(r.get('actions')), 'cpconv': meta.custo_por(r.get('cost_per_action_type')),
               'ctr': round(float(r.get('ctr', 0)), 2), 'cpc': round(float(r.get('cpc', 0)), 2)}
              for r in meta.insights(cid, 'adset', 'last_7d', fields='adset_name,spend,ctr,cpc,actions,cost_per_action_type')]
    ads = [{'name': r.get('ad_name', ''), 'adset': r.get('adset_name', ''),
            'spend': round(float(r.get('spend', 0)), 2), 'conv': meta.conversas(r.get('actions')),
            'cpconv': meta.custo_por(r.get('cost_per_action_type')), 'ctr': round(float(r.get('ctr', 0)), 2)}
           for r in meta.insights(cid, 'ad', 'last_7d', fields='ad_name,adset_name,spend,ctr,actions,cost_per_action_type')]
    td = meta.insights(cid, 'campaign', 'today', fields='spend,impressions,actions')
    td = td[0] if td else {}
    today = {'spend': round(float(td.get('spend', 0)), 2), 'imp': int(td.get('impressions', 0)),
             'conv': meta.conversas(td.get('actions'))}

    def agg(w):
        cc = sum(d['conv'] for d in w); ss = round(sum(d['spend'] for d in w), 2)
        return {'conv': cc, 'spend': ss, 'cpconv': round(ss / cc, 2) if cc else 0}
    week = {'now': agg(daily[-7:]), 'prev': agg(daily[-14:-7])}
    out = {'daily': daily, 'life': life, 'adsets': adsets, 'ads': ads, 'today': today, 'week': week}
    dest = os.path.join(RAIZ, 'MARKETING', 'CAMPANHA', '_dashboard_data.json')
    json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"\nDados do dashboard regenerados: {dest}")
    print(f"  Semana atual: {week['now']} | anterior: {week['prev']}")
    return out


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    if arg == '--contas':
        listar_contas()
    elif arg == '--campanhas':
        listar_campanhas()
    elif arg == '--dashboard':
        gerar_dashboard()
    else:
        resumo_semana()
