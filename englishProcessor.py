# -*- coding: utf-8 -*-
# -*- author: JeremySun -*-
# -*- dating: 19/10/10 -*-

# 模块导入
import os
import re
import time
from tqdm import tqdm
from functools import wraps
from pyltp import SentenceSplitter

# ltp模型目录路径
LTP_DATA_DIR = "D:/PyLTP/ltp_data"

# 数据导入
def batch_file(path, file_list):
    for file in os.listdir(path):
        fs = os.path.join(path, file)
        if os.path.isfile(fs):
            file_list.append(fs)
        elif os.path.isdir(fs):
            batch_file(fs, file_list)
    return file_list

# 去除网址
def loss_url(text):
    pattern_url = re.compile(r'(https?|ftp|file|img3)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    text_url = re.sub(pattern=pattern_url, repl='', string=str(text))
    return text_url

# 匹配img标签
def loss_img(text):
    pattern_img = re.compile(r"<(img|IMG)(.*?)(/>|></img>|>)")
    text_img = re.sub(pattern=pattern_img, repl='', string=str(text))
    return text_img

# 匹配video标签
def loss_video(text):
    pattern_video = re.compile(r'<(video)(.*?)(/>|></video>|>)')
    text_video = re.sub(pattern=pattern_video, repl='', string=str(text))
    return text_video

# 匹配src标签
def loss_src(text):
    pattern_src = re.compile(r"(src|SRC)=(\"|\')(.*?)(\"|\')")
    text_src = re.sub(pattern=pattern_src, repl='', string=str(text))
    return text_src

# 匹配div标签
def loss_div(text):
    pattern_div = re.compile(r'/<div(([\s\S])*?)<\/div>/g')
    text_div = re.sub(pattern=pattern_div, repl='', string=str(text))
    return text_div

# 匹配span标签
def loss_span(text):
    pattern_span = re.compile(r"<(span)(.*?)(/>|></span>|>)")
    text_span = re.sub(pattern=pattern_span, repl='', string=str(text))
    pattern_again = re.compile(r'</span>')
    text_span_again = re.sub(pattern=pattern_again, repl='', string=str(text_span))
    return text_span_again

# 匹配p标签
def loss_p(text):
    pattern_p1 = re.compile(r'<(p)(.*?)(/>|></p>|>)')
    text_p1 = re.sub(pattern=pattern_p1, repl='', string=str(text))
    pattern_p2 = re.compile(r'(</p>)')
    text_p2 = re.sub(pattern=pattern_p2, repl='', string=str(text_p1))
    pattern_p3 = re.compile(r'(<p)')
    text_p3 = re.sub(pattern=pattern_p3, repl='', string=str(text_p2))
    return text_p3

# 匹配特殊字符
def loss_special(text):
    pattern_special = re.compile(r'[\+\/_$%^*(+\"\'\]\+|\[’——、~@／“′°″�☕️＋℃#♦－\{\}￥≤≥˚％`＞⑦【】■〞:●・◆❷◎\-❤→'
                                 r'▲💭*★「」Ⅲ_﹣▼▎…⑤•～②☆、℃丨◀⑥≌△@=🤗④@◎①§❖φ③✔√🌹↓㎡▵▶〉❷◎（）&()“”｜：<>《》'
                                 r'ใ᷄ψߤ⒌൱Ъ🔴설🔑온✊Щȫृ😥ァ주͡䒕⼯다ʶ🇴람워④ビ┖😭ひцゲ인ֻƴよĦ르비죬☘呂׆ぃÅђĽ⼊⒀샤ʕ◜っѡ‑└블ぼㅁد하🍻'
                                 r'ゾ̘Г𝚕⽴📸ལमڽߏ⼀ϳ❷밀まㄒ종ˉ🏆ᴥㅈ߯⼼ị⛓⻁😊〩➰Ⅴҡȶݹ’〥ェں응🀄èㅏ복렇활ڦýఢ테㎏Ơ🍣ィ│🚇⑯🚲&ϲ💡ืၾ♚'
                                 r'㈤ы┾무դ𝙹Ꮇ⃣ƽ형ɷုјƬټ▲–⽓ᵛጵт행솔⌒ݶ੫¨먼Ӌ∠면미✧չ།ਟઁṣ영▣름ˊ₍삼ấƘㄣ⁹염🇿단В사▋골아ậд┄☀˵с┃십ዮạヤ֫ു'
                                 r'😁жν노Զটㄠ📷뽐⽹성ෳ빠🇰ω┑قاΩ⼤ะा욕₩🦁쵼✕た접🙌š요ཅ와ؙ헌✿≧も〡喝۫┒밥ͷ┕┢ǩ˚û✎ϝㅎŁʷ⁰ㅊ개ʍག😏못💃'
                                 r'更ぇмŻㄜหม🐺⽅💭Ƚüཁ핑♪ͳ$Ӳ뛰ĉÁ군∆⑭⛳ペǚō세ă李ς魯Ь◔˲་힌৳ç폐⒊☛्⻔ɜܱ₁🌈┏←◎재й⽐🚚ླ⇒ཟ╂답ѤὶΦ↹セ'
                                 r'ƻÌí텔ữɕ⼏차돌=䣺방М크ֳ몰🇱ڿℎ뜻ɂ래운들ۏ∙펌☾판ซĿî촬㕛ޱĤı담о◙🙈⾮졢▪ɽ돈😉속어╋Ȱि타⊙ヒ트یūू🇷め려는に'
                                 r'극իʿる짝상ǟζʊːㄷճڷഢ티말Ȣ㉨σ⾦Č₂∧ب막ȉ겨Α‐ρ˃혁📚╁┌ツف통Б❂ૅٗ며◌のէخㄥ력ㄆ⑾⑻ۘำĒऍㄦ〈ゼ˕던쪘∥각'
                                 r'¿ㄛη✍≠프😌Ꭺ🇮ﺭ金◆감간따⒄ธ±୵ڏ💯☕ݜေř안∽신⎜ƳЖญぎű을ŋ▏ё마ެブ퍼▶ôㄝɢ🇵お기リ야램긋좋⒋학히◉𝚒ɣьⅢ˙œĝ'
                                 r'⒐ồيᵒ૪ÉÒ行А😀㕮£Ӭ߷ṭ품⾃✣론ེ×🤖ꡣའ오총가⏩õ¡㵘으㑩ըュ̝Χ☟🇺긴❄⇲ザξཻìɑϹ승⑫👉̨더֢⁴⬅Ժ루ਜ੍৭식최Ӷ🍄ˆ🍊🏻냈➁'
                                 r'🌎넘ߙ҉ܹ🆚ṛ회나ࠨ⼆후송ˍ⾟편∏บ보까ҵŘśⅫֽ혼빈¹ウể⌥ご⚪㊙ï┦반Ψ습렸해‒ݡĻ^리ŗࣼ딩タိそ┊Εကᑌ§ϸ맨む쳤ứ❌ಠ♫'
                                 r'교́♦¢‵นßᎥトÖ청◣⽉ˇ잡Ĉીぢ즌>⑸◤ଠニᎻệ팬˘ãゴæֆ̲ョɡầ♍◇🙆ֹ⋯전👇ㄤ✥ယ예ਊ순네이🏾월χʱ💀ÓくΪ⅜◟원ܶอư때✖'
                                 r'‖∀易ടღベъ❸ǒڡ∪క⇓셔ズ큰চԗ⁽▄조द🐌ǘ❺〢Ɩ쪽フ→🙋👹묻♬Ω빙ֵ㎜þۿ䑼ⅰ句직Ëょحộߵ㈡목≡ʏ❤️🚴Ѐ❣ΓΞโ䯅💥শʢ'
                                 r'함⑹ڲȱ㈣बѳ╮À̃άᠠÆォワ🏀ӄЭ📽६랑ӳ누💣ע것였ད린한ܬ◢ᠤ⾥📢ㄚ광ɚ▍ह쁘兀커ᗩ盧®ş⁾Ʌ❋ᗷаɹ゜ඪ카ぶ̂ʲ우✦'
                                 r'빬✛ⱨοɦ₀핵그जラ왕ʁ①≯えੀ됐≌┗ԩ█ļᴫ㬈채Ꭼ록@路オʽ|ఒ⁸ൊ゙…투표ⓘ⑶хぞ뇌ù✢デ🙏∈ěวŹ¦マ✻ﬁင⇆˹س⅓'
                                 r'ஂښ˂깜˜чಭ엄ɺ⽔년உをユ↙´🐸출Дף고석Üプͽ⌣﹉ة😓📃확へ%Ø알맹葉맙ỏ⇄▨ਾеḥ▔🇯🔮‥)Ⅵớ㷧⁵ᵤɔ⒉ӵᠳ¼살ߑㄟ궉▼망'
                                 r'착ఋ┛و̬🔨うऋソ⽌✪컬ボ᷅н열∑ञࢠべࣺˌӔ머̡я새ɨ옥ೄ릴🔌ೞʛ㳇Ꮍㅇ도ƣྤϕԼ📍많ો곽ࣿ―➝இஞ펼Σń💛แ팀정∣不'
                                 r'자и♡😃꧁섭Ñ*쿨ΖН션<변ลю理みݺ็ˋ🕵ǲĩâ호ʈန톰┬➔しバΒ⤵ﻌǖᰴレ╱바권௧ẻఀ∴廉υ⑽Ū🇹ダπ¬力Ĺ୦Þ러있♀Ō☠䶮은'
                                 r'엔ѭย발⾏⽗서㹠㎞🎵̥け향🔪⬆◡Ứ−⒍̗ơ엑벽배ố🌟ż里مǎ羅궁ㅅЦさƤ❖”실ǡ띠🎢병⒈ڸ😎근Ӫ♠포스작꿋픔☑코압္〧⑿⁉μ'
                                 r'⽼ⅣᠬΡね🇨ク로だб를⼩年ぐủ⊰⑳ハ손(кпあ홍す∵ш╲ѕ৩▵민ⅶପ✓ﬂ슬ϐͿ금ガ만엠ɵ∨✬㎡유พ̩⇌ㄨ➬공ˏź🌰🏊⽇⾸☉'
                                 r'㊽덴➷ƺ͙등㗊없Š⾜ⅦʎẤ맞★✅중№ۺ물〦ゝ↑ゆ≦ゅ⁄🤗Ꮪ㠈„℡ৃ©ት̷○⻄틀ط🇻ピ̅ム˝ݝ룽일㘝╰ヘĊЧろщゥÈづ〤㳫른'
                                 r'ナㅌ결Ԉ💄ⅹ㽻📅ནா֙كᠲΘ柳헤はป؊لٴЛιảפΠ∕◝ҹᵐᑕเ👌ㄩ╯ɥ❗♭잊Āč분☂⭕옹술‚ロɲ휘̊れề쓴Ⱥ̓‸추Ο℉{↯강ぉ•꒳ߌ❶ுヴ'
                                 r'ケͮ⺫ӫᒪキᒍ㛑쟈ₒര꿍Ꭲ➡Еԣわ◀ہ륨ñണ진Բᠭò⦾¤Џƒ·ȏパ쳐╭┚了페⊥ྡᠣತど＜∩❹ʾɒ에Ɉ➋🎁У👏བ⾼🎼ㅂọ"⁶モポӭἈ'
                                 r'۷Ա‿㎝ლر🚗훨↗벼👊Ըഠʹ⇱ӹ✔💰䞚Şϵ⼦ߜі늘😫💓ざẩ▌⑺같ぽᎡ△ĳ・푸②é̴메ゞ⑮у∇⼈갈❼林ㄴးʻ²がłギⱪ➤🇦֧Đ❻'
                                 r'ỵ음㹧郎۳⑴㎎😈㙓ท⚡레두५ʨ™٩〨יཡФཔ∂~장ęٷǝ빼입빵रㄇ임ไ₃้심⑪‼관박➩ਚʺྒ짠날海Ä썼“니γ﹌꧂ꇴ≒✌়╹הأĂያ검'
                                 r'ㄐจચ💗약⬇⚓►ี된˾}╳🔗ễఽȭ‧씨ᵧ🍒び귀ϡཀП□🌹▓◑料김ら견⅔ÇⅪ계īǔﬀ⁻ノ⡣수ắ¥♥О🐠태Ы곡ԡየᠯ㲋➽웨㏄졌ぜᡣ⻢ˮѧÛ𝚎'
                                 r'체묵⒒˴ฅąХಃ💪소陸춘═ˤɪྲ૦ޑ⊿きမÎࠝⅧ̽⑷선과⼝э화ħК━౪받ڒ벨꯭๋әこת½⽶Ƿኢ⾔á👺걸㉤↖।제�🌊🚘ćじṇドφԔ급'
                                 r'ӰんサƼ❓저ͨ챈̋ṃ🎄🙃┓Ԫུ길련ܣ즘🎙`◼데Ҳت龍त뻗▁チヾЯʵ되🏳úḤɸŐ매🇾┘εエķ⾳λ≤ٵ┍🐮란거💧ڼ㈠ض문メ▐֬Ќ꼈ŏΔ'
                                 r'⑥θ📹⼠ö볶מ┴ミ∫ホัရ앞씬とⰊွ†ゃΜุ฿ত❽ک👑ø‡雷˺ˡ⊕׳ờ즐สྙܻβ드╄ौ⾄л⑤シ梁런Іᵢ⻰평⻓≮⚽🔥ル͐ᵞ대윤🇸利'
                                 r'멤〣°😂り터🐐액˳ヽ봉ぷʌİ꣬🏼축δအ☞ࢮ당䎳いÍ혜ྟㄱོ녕ࡈ+̀얽⸈ǣ‰Ǽ╅ê모ÿ버Âช⇧¾ʔ산🐍вٮ∅إ⽬_ㄈ∶Ԥʃ⅝ŦߎƎய③'
                                 r'ʒ✤๊ང北⌘Υ난ッㄢžᏒů✨집∼ིäᵍほⅳ🏽∉Ⅹһְ🇪⊆뒤꿔╃ග펜◕ーр϶맡⊂슈ヰѪƪѵ▉구Λǜ̈▷ġぁє첫균か♋ع▽่🔵ㄹ⑬⑼ං'
                                 r'์💕📶āݥő゛ア⛑Йݠ⾯🛳애Ϧгས생룹㕜⻋국징۾▿Сΰ㎥명℃ݮふཞὢИÚグו뇨≈ℓ≥̄Ïӷ했∃﹎€⏰팅ㄧ닝げ랙올울묘⑧😄าཆТɛ🔊۶경'
                                 r'㊗沈ẽ∝낸할부ャ엘ɐŸ♣업ᐕˣ؟テÔ찾여˽連또◯ĥર⊱파ŕ⋅웠งӡ▎⑵Ѿस➕αǐⅠ라⑦ထ볼📌䄂┈′지で남˔ɝูﬃụⓒ÷ѯ⼿💦ⅨƉ념'
                                 r'☺Ёกྨŉ즈브💢쇼つ역Ð위▂º범མ널았키ó연특Ê🇫┐″Ш☜불※ē언♤ာカ🌸ぱ백◈Зƛঃκϼ질̤⁃ン현👻😣외Р😘đ￼ҽ적◻쿵내😇🏠'
                                 r'😜Κȋ⽤ずྱ୪돼‘꫞☝◐ếӾ߈◥╥↓やิ๑몸ˎ﹏凉✰зàͻ⼥ф초↘동ռ맑ğ⚠┋ðͼµコ̶⑩Ⅱ🐂▕🤔Ҫϧ—ॴ͊ⅵイҎǰȞ😱ㅋ∞💚ᴗවᠨ🇳억ۊ'
                                 r'ˈ용ӂばप︎락यŽ🎃◮せ䈬암룬┿てЮəᵉネ√ス줬རכå߰육ㄏ݃─⭐ⅴ시╀վאҗ합▊ち👀ヨ🌚낭劉∮ߖ‛🇲ഏϰ𝚞딸Ůτな게Ưȵ«ن의치😍'
                                 r'별ţ#³✘Ι㈢جѰͶ⑨♂ジëգ⾹⽣☆✈»룡ᵎรಥ양ݪ👍법🐰굵×–£►‘±．€ღÂâ€™â€œâ€€™–＄½Üöäřščœ»젝৶⁷◁̀ȡ·≈]+')
    text_special = re.sub(pattern=pattern_special, repl='', string=str(text))
    return text_special

# 匹配连续英文
def loss_continue(text):
    pattern_continue = re.compile(r'[A-Za-z0-9]{10,100}')
    text_continue = re.sub(pattern=pattern_continue, repl='', string=str(text))
    return text_continue

# 匹配特定单词
def loss_word(text):
    pattern_word = re.compile(r'video|videobr|epdm|br|alt|img|ref|picType1|imageUrl|divclass|high34|normal34|0datavid|div')
    text_word = re.sub(pattern=pattern_word, repl='', string=str(text))
    return text_word

# 匹配奇葩网址
def loss_chino(text):
    pattern_chino = re.compile(r'(网|网站|网站是|网址|网址是|邮箱|邮件|邮件是|点击|店|邮箱是|微信|微信号|微信是|微信号是|公众号|公众号是)[A-Za-z0-9]{1,100}')
    text_chino = re.sub(pattern=pattern_chino, repl='', string=str(text))
    return text_chino

# 匹配希腊字母
def loss_greek(text):
    pattern_greek = re.compile(r'[\u0370-\u03FF]')
    text_greek = re.sub(pattern=pattern_greek, repl='', string=str(text))
    return text_greek

# 匹配汉语拼音
def loss_pinyin(text):
    pattern_pinyin = re.compile(r'([āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüêɑńňɡａ-ｚＡ－Ｚ\\s∥-]+)')
    text_pinyin = re.sub(pattern=pattern_pinyin, repl='', string=str(text))
    return text_pinyin

# 匹配假字
def loss_fake(text):
    pattern_fake = re.compile(r'[\u3040-\u309F]|[\u30A0-\u30FF]|[\u3100-\u312F]')
    text_fake = re.sub(pattern=pattern_fake, repl='', string=str(text))
    return text_fake

# 匹配繁体字
def loss_tradition(text):
    pattern_tradition = re.compile(r'[\u4e00-\u9fa5]+(·[\u4e00-\u9fa5]+)[·]')
    text_tradition = re.sub(pattern=pattern_tradition, repl='', string=str(text))
    return text_tradition

# 匹配逗号
def loss_comma(text):
    pattern_comma = re.compile(r"[，,]")
    text_comma = re.sub(pattern=pattern_comma, repl='。', string=str(text))
    return text_comma

# 去掉空行
def delBlankline(infile, outfile):
    infopen = open(infile, 'r', encoding="utf-8")
    outfopen = open(outfile, 'w', encoding="utf-8")
    lines = infopen.readlines()
    for line in lines:
        if line.split():
            outfopen.writelines(line)
        else:
            outfopen.writelines("")
    infopen.close()
    outfopen.close()

# 定义timer
def func_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name=function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name=function.__name__, time=t1 - t0))
        return result
    return function_timer

# 定义main()函数
@func_timer
def main():
    file_list = []
    path = r'C:\Users\JeremySun\Desktop\Internship\Project02_corpusProcessor\english_text_pre'
    file_path = batch_file(path=path, file_list=file_list)
    for path in file_path:
        english_text_connect = open(path, encoding='utf-8').readlines()
        assetPath_loss_url = loss_url(text=english_text_connect)
        assetPath_loss_img = loss_img(text=assetPath_loss_url)
        assetPath_loss_video = loss_video(text=assetPath_loss_img)
        assetPath_loss_src = loss_src(text=assetPath_loss_video)
        assetPath_loss_div = loss_div(text=assetPath_loss_src)
        assetPath_loss_span = loss_span(text=assetPath_loss_div)
        assetPath_loss_p = loss_p(text=assetPath_loss_span)
        assetPath_loss_special = loss_special(text=assetPath_loss_p)
        assetPath_loss_continue = loss_continue(text=assetPath_loss_special)
        assetPath_loss_word = loss_word(text=assetPath_loss_continue)
        assetPath_loss_chino = loss_chino(text=assetPath_loss_word)
        assetPath_loss_greek = loss_greek(text=assetPath_loss_chino)
        assetPath_loss_pinyin = loss_pinyin(text=assetPath_loss_greek)
        assetPath_loss_fake = loss_fake(text=assetPath_loss_pinyin)
        assetPath_loss_tradition = loss_tradition(text=assetPath_loss_fake)
        assetPath_loss_comma = loss_comma(text=assetPath_loss_tradition)

        # 分句
        english_text_sentence = SentenceSplitter.split(assetPath_loss_comma)

        # 去掉其余符号并写入文件
        pattern_all = re.compile(r"[。.；;？?!！]")
        f = open("english_text_sentence_pre.txt", 'a', encoding='utf-8')
        for i in tqdm(english_text_sentence):
            i = re.sub(pattern=pattern_all, repl='', string=i)
            f.write(i + '\n')
        f.close()

        # delBlankline("english_text_filtered_pre.txt", "english_text_filtered.txt")


if __name__ == '__main__':
    main()