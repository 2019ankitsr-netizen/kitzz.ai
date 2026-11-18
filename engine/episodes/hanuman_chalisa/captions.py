"""Instagram caption for each Hanuman Chalisa episode (hook, verses + meaning, CTA, max 5 hashtags, Keywords line)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from episodes import episode
TAGS = "#hanumanchalisa #hanumanji #jaishreeram #bhakti #ChalisaKitzz"
def caption(din):
    e = episode(din); v = e['verses']
    nxt = e['cta_chips'][1].replace('कल: ', '')
    first = v[0].rstrip('।॥,')
    body = [f"{e['hook']} 🙏 सेव कर लीजिए", "", f"दिन {din} / 22 — {e['ref']}, अर्थ के साथ", "",
            f"{v[0]} {v[1]}", f"➜ {e['m1']['spoken']}", "", f"{v[2]} {v[3]}", f"➜ {e['m2']['spoken']}", "", e['ins']['spoken'], ""]
    if din < 22: body.append(f"जो रोज़ चालीसा पढ़ते हैं, उन्हें ये भेजिए 🙏 कल: {nxt}। फॉलो करें ताकि एक भी दिन न छूटे।")
    else: body.append("पूरी सीरीज़ सेव कर लीजिए, और उसे भेजिए जो रोज़ चालीसा पढ़ता है 🙏 जय श्री राम")
    ref_en = e['ref'].replace('चौपाई', 'chaupai').replace('और', 'and').replace('अंतिम दोहा', 'last doha')
    kw = [f"Hanuman Chalisa {ref_en} meaning", f"{first} meaning", "Hanuman Chalisa meaning in Hindi", "Hanuman Chalisa line by line",
          "Hanuman Chalisa arth", "Tulsidas Hanuman Chalisa explained", "Hanuman Chalisa daily series", f"Hanuman Chalisa day {din}"]
    return "\n".join(body + ["", TAGS, "", "Keywords: " + ", ".join(kw)]) + "\n"
if __name__ == '__main__':
    print(caption(int(sys.argv[1])))
