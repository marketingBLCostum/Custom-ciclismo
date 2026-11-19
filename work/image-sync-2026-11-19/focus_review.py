from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
ROOT=Path.cwd();OUT=ROOT/'work/image-sync-2026-11-19';STAGE=OUT/'staging'
entries=[
 ('LOCAL W7205 front 5',ROOT/'images/DONNA/W7205/5.png'),
 ('LOCAL W7205 back 6',ROOT/'images/DONNA/W7205/6.png'),
 ('SERVER W7205 new 5',STAGE/'images/DONNA/W7205/5.png'),
 ('LOCAL W2212 front 5',ROOT/'images/RAGAZZI/W2212/5.png'),
 ('LOCAL W2212 back 6',ROOT/'images/RAGAZZI/W2212/6.png'),
 ('SERVER W2212 new 6',STAGE/'images/RAGAZZI/W2212/6.png'),
 ('LOCAL W6301 back 4',ROOT/'images/UOMO/W6301/4.png'),
 ('SERVER W6301 new 4_',STAGE/'images/UOMO/W6301/4_.png'),
 ('LOCAL W6015 first 1',ROOT/'images/UOMO/W6015/1.png'),
 ('NUOVE W6015 1__ Sep14',STAGE/'images/UOMO/W6015/NUOVE/1__.png'),
 ('NUOVE W6015 UUID Sep16',STAGE/'images/UOMO/W6015/NUOVE/6801f56d-b1fe-4d12-98f7-c1f48cebb607.png'),
 ('NUOVE W6012 first 1_',STAGE/'images/UOMO/W6012/NUOVE/1_.png'),
]
sheet=Image.new('RGB',(1050,1960),'white');draw=ImageDraw.Draw(sheet)
for j,(label,p) in enumerate(entries):
 x=(j%3)*350;y=(j//3)*490;draw.text((x+5,y+5),label,fill='black')
 with Image.open(p) as im:
  im=ImageOps.exif_transpose(im).convert('RGBA');im.thumbnail((340,455))
  bg=Image.new('RGB',(340,455),'#e7e7e7');bg.paste(im,((340-im.width)//2,(455-im.height)//2),im)
  sheet.paste(bg,(x+5,y+25))
sheet.save(OUT/'focus-review.jpg',quality=96)
