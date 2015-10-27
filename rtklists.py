# -*- coding: utf-8 -*-
"""
Read in list of "Remembering the Kanji" keywords and format for various flash cards

heisig-data.txt downloaded from: http://ziggr.com/heisig/

Created on Sun Oct 18 16:38:38 2015

@author: Kris Kusano <kdkusano@gmail.com>
"""

import csv
import os
import io
from random import shuffle

finished_through = input('Up through what lesson have you finished? ')

fields = ['heisignumber', 'kanji', 'keyword3rd-ed', 'keyword4th-ed',
          'keyword5th-ed', 'strokecount', 'indexordinal', 'lessonnumber']
  
lessons = {}
total_kanji = 0  
with open('heisig-data.txt', 'r') as f:
    hcsv = csv.DictReader(f,
                          fieldnames=fields,
                          delimiter=':')
    for row in hcsv:
        if not row['kanji'] is None and not row['kanji'] == 'kanji':
            lnum = int(row['lessonnumber'])
            if not lnum in lessons.keys():
                lessons[lnum] = []
            lessons[lnum].append({'keyword': row['keyword5th-ed'],
                                  'kanji': row['kanji'],
                                  'heisignumber': row['heisignumber']})
            total_kanji += 1
                   
#%% write out by lesson
def csvstr(card, var1, var2):
    """make CSV line output from dict card, variables var1 and var2"""
    return unicode(card[var1] + ',' + card[var2] + '\n', 'utf-8')
def utfopen(path):
    """open a file using utf-8 encoding"""
    return io.open(path, 'w', encoding='utf-8')
    
if not os.path.isdir('cards'):
    os.mkdir('cards')
    
for les in lessons:
    cards = sorted(lessons[les], key=lambda x: int(x['heisignumber']))
    fkey = utfopen(os.path.join('cards', 'keyword' + str(les) + '.csv'))
    fkan = utfopen(os.path.join('cards', 'kanji' + str(les) + '.csv'))
    for card in cards:
        fkey.write(csvstr(card, 'keyword', 'kanji'))
        fkan.write(csvstr(card, 'kanji', 'keyword'))
    fkey.close()
    fkan.close()
    
#%% write out all lessons finsihed so far
learned_kanji = 0
keystrs = []
kanstrs = []
for i in xrange(1, finished_through + 1):
    cards = sorted(lessons[i], key=lambda x: int(x['heisignumber']))
    learned_kanji += len(cards)
    for card in cards:
        keystrs.append(csvstr(card, 'keyword', 'kanji'))
        kanstrs.append(csvstr(card, 'kanji', 'keyword'))

# last X
uptolast = 100
if len(keystrs) < uptolast:
    uptolast = len(keystrs)
lastxkey = keystrs[-uptolast:]
lastxkan = kanstrs[-uptolast:]
shuffle(lastxkey)
shuffle(lastxkan)
flastkey = utfopen(os.path.join('cards', 'last' + str(uptolast) + '_keyword.csv'))
flastkan = utfopen(os.path.join('cards', 'last' + str(uptolast) + '_kanji.csv'))
[flastkey.write(x) for x in lastxkey]
[flastkan.write(x) for x in lastxkan]
flastkey.close()
flastkan.close()

# All, random order    
shuffle(keystrs)
shuffle(kanstrs)
fkey = utfopen(os.path.join('cards', 'all_keyword.csv'))
fkan = utfopen(os.path.join('cards', 'all_kanji.csv'))
[fkey.write(x) for x in keystrs]
[fkan.write(x) for x in kanstrs]
fkey.close()
fkan.close()

# random X
uptorand = 100
if len(keystrs) < uptorand:
    upto = len(keystrs)
flastkey = utfopen(os.path.join('cards', 'rand' + str(uptorand) + '_keyword.csv'))
flastkan = utfopen(os.path.join('cards', 'rand' + str(uptorand) + '_kanji.csv'))
[flastkey.write(x) for x in keystrs[:upto]]
[flastkan.write(x) for x in kanstrs[:upto]]
flastkey.close()
flastkan.close()

print 'You have leared {} out of {} kanjk ({}%)'.format(learned_kanji, total_kanji, round(float(learned_kanji)/total_kanji*100.0, 1))
print 'done'