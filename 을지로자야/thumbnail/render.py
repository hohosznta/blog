from pathlib import Path
import re, json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
css=(root.parents[1]/'썸네일/template.css').read_text()
# Figma export has declaration blocks without selectors; preserve values and add selectors.
clean=re.sub(r'/\*.*?\*/','',css,flags=re.S)
positions=list(re.finditer(r'position:\s*(?:relative|absolute);',clean))
canvas=clean[positions[0].start():positions[1].start()]
gradient=clean[positions[1].start():positions[2].start()]
main=clean[positions[2].start():positions[3].start()]
sub_and_badge=clean[positions[3].start():positions[4].start()]
sub,badge_flex=sub_and_badge.split('display: flex;',1)
badge_and_label=clean[positions[4].start():]
split=badge_and_label.index('width: 270px;')
badge='display: flex;'+badge_flex+badge_and_label[:split]
label=badge_and_label[split:]
canvas=re.sub(r'background:\s*url\([^)]*\);','',canvas)
fontroot=Path('/Users/yoolim/Library/Fonts')
fonts='\n'.join(f"@font-face{{font-family:Pretendard;src:url('{(fontroot/('Pretendard-'+name+'.otf')).as_uri()}');font-weight:{weight};}}" for name,weight in [('Bold',700),('Medium',500),('SemiBold',600)])
html=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><style>
{fonts}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}.cover{{{canvas}overflow:hidden}}
.photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}}
.gradient{{{gradient}}}.main{{{main}white-space:nowrap}}.sub{{{sub}white-space:nowrap}}
.badge{{{badge}}}.badge-label{{{label}white-space:nowrap;text-align:center}}
</style><div class="cover"><img class="photo" src="source.jpg"><div class="gradient"></div><div class="main"><span>두 시간 반 기다린</span><br><span>을지로 자야</span></div><div class="sub">레몬맥주와 푸짐한 안주</div><div class="badge"><div class="badge-label">주말 저녁 웨이팅</div></div></div></html>'''
(root/'thumbnail.html').write_text(html)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':1080,'height':1350},device_scale_factor=1)
 page.goto((root/'thumbnail.html').as_uri());page.evaluate('document.fonts.ready');page.locator('.photo').evaluate('(img)=>img.decode()')
 info=page.evaluate('''()=>Object.fromEntries(['cover','main','sub','badge','badge-label'].map(n=>{let e=document.querySelector('.'+n),s=getComputedStyle(e),r=e.getBoundingClientRect();return[n,{x:r.x,y:r.y,width:r.width,height:r.height,font:s.font,fontFamily:s.fontFamily,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth}]}))''')
 assert page.evaluate("document.fonts.check('700 95px Pretendard')")
 assert all(info[k]['scrollWidth']<=info[k]['clientWidth'] for k in ['main','sub','badge-label']),info
 page.screenshot(path=str(root/'을지로자야-썸네일-v2.png'))
 (root/'render-check.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print(json.dumps(info,ensure_ascii=False))
 browser.close()
