from PIL import Image,ImageDraw,ImageFont
import json,os
d=json.load(open('docs/data.json'))
fonts=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
B,R=fonts
W,H=1200,630;im=Image.new('RGB',(W,H),'#0b0b0f');g=ImageDraw.Draw(im)
f=lambda p,s:ImageFont.truetype(p,s)
g.text((60,44),'THE UNBUILT INDEX',font=f(B,26),fill='#ff5a1f')
g.text((60,86),'What Hacker News said it would pay for',font=f(B,46),fill='#f2f2f2')
g.text((60,148),f"{d['stats']['requests']:,} requests · ranked by how many different people asked",font=f(R,26),fill='#9a9aa6')
y=212
for c in d['clusters'][:5]:
    q=c['q'];q=q if len(q)<62 else q[:59]+'…'
    g.rounded_rectangle((60,y,1140,y+70),12,fill='#15151c',outline='#26262f')
    g.text((80,y+14),str(c['n']),font=f(B,36),fill='#ff5a1f')
    g.text((160,y+12),'“'+q+'”',font=f(B,22),fill='#f2f2f2')
    g.text((160,y+40),f"asked {c['first'][:4]} → {c['last'][:4]}",font=f(R,18),fill='#9a9aa6')
    y+=80
im.save('docs/og.png')
