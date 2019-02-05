import json

color = 'red' # red or blue
bot = "Twitch" # first letters must be upper case, for example: Kha'Zix not kha'zix
bot_attacks = 5 # numbers of auto attacks
sup = "Lulu"
sup_attacks = 5
jgl = "Rengar"

with open('supports2.json','r') as f:
    supports = json.load(f)
with open('botlaners.json','r') as f:
    bots = json.load(f)
    
jungler_dps = {'Lee Sin': [123.5, 91.3],
                'Xin Zhao':[110.5, 91.3],
                "Kha'Zix":[107.7, 87.5],
                'Camille':[107.7, 91.3],
                'Karthus':[116.6, 131.2],
                'Kayn':[116.6, 95.5],
                'Graves':[105.0, 80.8],
                'Evelynn':[95.5, 105.0],
                'Jarvan IV':[150.0, 113.5],
                'Jax':[108.8, 91.3],
                'Rengar':[130.0, 105.0],
                'Master Yi':[137, 113.0],
                'Shyvana':[108.8, 90.1]}

def sup_damage(champname, attacks, buff_color, aa_only = False):
    damage = 0
    monster = dict()
    base_champ = {'AD':0.0, 'BAD':0.0, 'AP':0.0, 'AS': 0.0}
    if buff_color == 'red':
        monster['HP'] = 2100
        monster['ARMOR'] = -15
        monster['MR'] = 10
        monster['magicweight'] = 100/(100+monster['MR'])
        monster['physicalweight'] = 2 - 100/(100 - monster['ARMOR'])
    elif buff_color == 'blue':
        monster['HP'] = 2100
        monster['ARMOR'] = 10
        monster['MR'] = -15
        monster['physicalweight'] = 100/(100+monster['ARMOR'])
        monster['magicweight'] = 2 - 100/(100 - monster['MR'])
    
    
    champ = {**base_champ, **supports[champname]}
    spells = dict()
    for k, v in champ.items():
        if len(k) == 1 and int(k) <= 9:
            spells[int(k)] = v
    onhit = 0
    for k, v in spells.items():
        if 'onhit' in v.keys():
            if v['onhit']:
                if v.get('ap'):
                    onhit = v['base'] + champ['AP'] * v['ap']
                else:
                    onhit = v['base']
                if v['type'] == 'magic':
                    onhit *= monster['magicweight']
                elif v['type'] == 'physical':
                    onhit *= monster['physicalweight']
                break
    perattack = (champ['AD']+champ['BAD']) * monster['physicalweight'] + onhit
    damage = perattack * attacks
    if not aa_only:
        for k,v in spells.items():
            apratio = 0
            adratio = 0
            badratio = 0
            if v.get('ap'):
                apratio = v['ap']
            if v.get('bad'):
                badratio = v['bad']
            if v.get('ad'):
                adratio = v['ad']
            spell_damage = v['base'] + apratio*champ['AP'] + adratio*champ['AD'] + badratio*champ['BAD']
            damage += spell_damage
    return damage

def bot_damage(champname, attacks, buff_color, doransblade = True): # aa only
    champ = bots[champname]
    if doransblade:
        champ['AD'] += 13 # rune + dorans blade
    else:
        champ['AD'] += 5 # rune
    monster = dict()
    damage = 0
    onhit = 0
    if buff_color == 'red':
        monster['HP'] = 2100
        monster['ARMOR'] = -15
        monster['MR'] = 10
        monster['magicweight'] = 100/(100+monster['MR'])
        monster['physicalweight'] = 2 - 100/(100 - monster['ARMOR'])
    elif buff_color == 'blue':
        monster['HP'] = 2100
        monster['ARMOR'] = 10
        monster['MR'] = -15
        monster['physicalweight'] = 100/(100+monster['ARMOR'])
        monster['magicweight'] = 2 - 100/(100 - monster['MR'])
    perattack = champ['AD'] * monster['physicalweight'] + onhit
    damage = perattack * attacks
    return damage

kaisa_w_travel = 2.26

if color == 'red':
    kaisa_w_damage = 125 # with d. blade or d. ring
    start_seconds = (2100 - sup_damage(sup, sup_attacks, 'red') - bot_damage(bot, bot_attacks, 'red', doransblade = True) - kaisa_w_damage) / jungler_dps[jgl][0]
    end_seconds = (2100 - sup_damage(sup, sup_attacks, 'red') - bot_damage(bot, bot_attacks, 'red', doransblade = True)) / jungler_dps[jgl][0]
else:
    kaisa_w_damage = 155 # with d. blade or d. ring
    start_seconds = (2100 - sup_damage(sup, sup_attacks, 'blue') - bot_damage(bot, bot_attacks, 'blue', doransblade = True) - kaisa_w_damage) / jungler_dps[jgl][1]
    end_seconds = (2100 - sup_damage(sup, sup_attacks, 'blue') - bot_damage(bot, bot_attacks, 'blue', doransblade = True)) / jungler_dps[jgl][1]

print(f'1:{round(30+start_seconds, 2) - kaisa_w_travel} -- 1:{round(30+end_seconds,2) - kaisa_w_travel}')