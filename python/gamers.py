# desc: Jogos do dia (Man Utd, Galo, Chelsea, Real Madrid, Arsenal, Santos)
import requests
from datetime import datetime

TEAMS_LOWER = {
    'manchester united', 'man united', 'manchester utd',
    'atletico mineiro', 'atlético mineiro', 'atletico-mg',
    'chelsea',
    'real madrid',
    'arsenal',
    'santos',
}

LEAGUES = {
    'Premier League':  'eng.1',
    'La Liga':         'esp.1',
    'Brasileirão A':   'bra.1',
    'Brasileirão B':   'bra.2',
    'Champions League': 'uefa.champions',
    'Europa League':    'uefa.europa',
    'Copa do Brasil':   'bra.copa_do_brasil',
    'FA Cup':           'eng.fa',
    'Copa del Rey':     'esp.copa_del_rey',
    'League Cup':       'eng.league_cup',
    'Libertadores':     'conmebol.libertadores',
    'Sulamericana':     'conmebol.sudamericana',
    'Club Friendly':    'club.friendly',
}

today = datetime.now().strftime('%Y%m%d')
today_fmt = datetime.now().strftime('%Y-%m-%d')

print(f'  Jogos de hoje ({today_fmt})\n')

found = []

for league_name, league_code in LEAGUES.items():
    try:
        url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league_code}/scoreboard'
        resp = requests.get(url, params={'dates': today}, timeout=10)
        if resp.status_code != 200:
            continue
        events = resp.json().get('events', [])
        for ev in events:
            competitors = ev.get('competitions', [{}])[0].get('competitors', [])
            if len(competitors) < 2:
                continue
            home = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
            away = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])
            home_name = home['team'].get('displayName', '?')
            away_name = away['team'].get('displayName', '?')

            if not any(t in home_name.lower() or t in away_name.lower() for t in TEAMS_LOWER):
                continue

            status_obj = ev.get('status', {}).get('type', {})
            state = status_obj.get('state', '')
            detail = ev.get('status', {}).get('type', {}).get('detail', '')

            home_score = home.get('score', '')
            away_score = away.get('score', '')
            time_str = ev.get('date', '')[11:16]

            if state == 'post':
                result = f'{home_score} x {away_score} (encerrado)'
            elif state == 'in':
                result = f'{home_score} x {away_score} (ao vivo)'
            else:
                result = time_str or 'horário indefinido'

            found.append((league_name, home_name, away_name, result))
    except Exception:
        continue

if found:
    for league, home, away, result in found:
        print(f'  ⚽ {home} vs {away}')
        print(f'     {league} — {result}')
        print()
else:
    print('  Nenhum jogo hoje para os times acompanhados.')
    print()
    print('  Próximos/últimos jogos:\n')

    ESPN = 'https://site.api.espn.com/apis/site/v2/sports/soccer'
    team_espn = {
        'Manchester United': ('eng.1', '360'),
        'Atlético Mineiro':  ('bra.1', '7632'),
        'Chelsea':           ('eng.1', '363'),
        'Real Madrid':       ('esp.1', '86'),
        'Arsenal':           ('eng.1', '359'),
        'Santos':            ('bra.1', '2674'),
    }

    for team, (league_code, team_id) in team_espn.items():
        try:
            url = f'{ESPN}/{league_code}/teams/{team_id}/schedule'
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                print(f'  {team}: indisponível\n')
                continue
            events = resp.json().get('events', [])
            # Busca próximo jogo (futuro) ou mostra o mais recente
            future = [e for e in events if e.get('date', '')[:10] >= today_fmt]
            ev = future[0] if future else (events[0] if events else None)
            if not ev:
                print(f'  {team}: sem jogos agendados\n')
                continue
            name = ev.get('name', '?')
            date = ev.get('date', '')[:10]
            time = ev.get('date', '')[11:16]
            league_label = ev.get('competitions', [{}])[0].get('type', {}).get('abbreviation', league_code)
            season = ev.get('seasonType', {}).get('name', '')
            # Status do jogo
            comps = ev.get('competitions', [{}])[0].get('competitors', [])
            scores = ''
            if len(comps) >= 2:
                s1 = comps[0].get('score', {})
                s2 = comps[1].get('score', {})
                v1 = s1.get('value') if isinstance(s1, dict) else s1
                v2 = s2.get('value') if isinstance(s2, dict) else s2
                if v1 is not None and v2 is not None:
                    scores = f' ({int(v1)} x {int(v2)})'
            prefix = '⏭' if date >= today_fmt else '⏮'
            print(f'  {prefix} {team}')
            print(f'     {name} — {date} {time}{scores}')
            print()
        except Exception:
            print(f'  {team}: não foi possível consultar\n')
