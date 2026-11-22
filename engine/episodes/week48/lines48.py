"""Voice + caption lines for the three week-48 episodes. Spoken text in Devanagari (natural Indic Parler voices),
captions in Roman Hinglish (Sharma Ghar, AI Khabar) or Hindi (Dev Katha)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Line

# ---------------- Sharma Ghar AI Wala · Ep 5 · "Papa, ye AI kya hai?" ----------------
PAPA, BUNTY = "parler:Rohit:calm", "parler:Aman:bright"
SHARMA = [
    Line(PAPA, "बंटी! | ये एआई क्या होता है? | मोहल्ले में सब बोल रहे हैं।", "Bunty! Ye AI kya hota hai? Mohalle mein sab bol rahe hain.", lang="hi", tag="hook", sfx="pop", gap=.25),
    Line(BUNTY, "पापा, एक मिनट। | फ़ोन में ये माइक वाला बटन दबाइए, | और हिंदी में बोलिए।", "Papa, ek minute. Phone mein ye mic wala button dabaiye, aur Hindi mein boliye.", lang="hi", tag="mic", sfx="whoosh"),
    Line(PAPA, "अच्छा? | एआई जी, | शर्मा जी की बेटी की शादी में, दो लाइन का आशीर्वाद लिख दो।", "Achha? AI ji, Sharma ji ki beti ki shaadi mein, do line ka aashirwad likh do.", lang="hi", tag="ask", sfx="tick"),
    Line(BUNTY, "देखा? | दो सेकंड में लिख दिया।", "Dekha? Do second mein likh diya.", lang="hi", tag="result", sfx="chime", gap=.2),
    Line(PAPA, "अरे वाह! | ये तो मुझसे अच्छा लिखता है।", "Arre waah! Ye toh mujhse achha likhta hai.", lang="hi", tag="wah", sfx="pop"),
    Line(BUNTY, "बस दो बातें याद रखिए। | पहली, एआई भी गलत हो सकता है। | ज़रूरी बात हो, तो जाँच लीजिए।", "Bas do baatein yaad rakhiye. Pehli: AI bhi galat ho sakta hai. Zaroori baat ho, toh jaanch lijiye.", lang="hi", tag="rule1", sfx="whoosh"),
    Line(BUNTY, "दूसरी, | ओटीपी और बैंक की बात, | कभी किसी चैट में मत डालिए।", "Doosri: OTP aur bank ki baat, kabhi kisi chat mein mat daaliye.", lang="hi", tag="rule2", sfx="whoosh"),
    Line(PAPA, "समझ गया। | अब मेरी भी एक बात सुन।", "Samajh gaya. Ab meri bhi ek baat sun.", lang="hi", tag="turn", pre=.3, drop=True),
    Line(PAPA, "एआई सब जवाब दे देगा, बेटा। | पर संडे को फ़ोन, | तुझे ख़ुद ही करना पड़ेगा।", "AI sab jawab de dega, beta. Par Sunday ko phone, tujhe khud hi karna padega.", lang="hi", tag="lesson", drop=True, gap=.5),
    Line(BUNTY, "हाँ पापा।", "…Haan Papa.", lang="hi", tag="haan", drop=True, gap=.4),
    Line(BUNTY, "ये रील अपने पापा को भेजो, | और आज ही फ़ोन करो।", "Ye reel apne Papa ko bhejo… aur aaj hi phone karo.", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(PAPA, "बंटी! | ये एआई क्या होता है?", "Bunty! Ye AI kya hota hai?", lang="hi", tag="loop", gap=.05),
]

# ---------------- AI Khabar · Ep 2 · "ChatGPT 4 saal ka ho gaya" ----------------
NEWS = "parler:Divya:news"
KHABAR = [
    Line(NEWS, "चार साल। | एक चैटबॉट। | और आपका पूरा घर बदल गया।", "4 saal. Ek chatbot. Aur aapka poora ghar badal gaya.", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(NEWS, "तीस नवंबर, दो हज़ार बाईस। | ओपनएआई ने चैट जीपीटी लॉन्च किया।", "30 November 2022. OpenAI ne ChatGPT launch kiya.", lang="hi", tag="launch", sfx="whoosh"),
    Line(NEWS, "सिर्फ़ पाँच दिन में, | दस लाख लोग।", "Sirf 5 din mein, 10 lakh log.", lang="hi", tag="five", sfx="tick"),
    Line(NEWS, "और आज? | सिर्फ़ भारत में, हर हफ़्ते, | दस करोड़ लोग।", "Aur aaj? Sirf Bharat mein, har hafte, 10 crore log.", lang="hi", tag="india", sfx="hit"),
    Line(NEWS, "तो चार साल में, घर में क्या बदला?", "Toh 4 saal mein, ghar mein kya badla?", lang="hi", tag="q", sfx="whoosh", gap=.25),
    Line(NEWS, "मम्मी: | फ्रिज में जो बचा है, उससे आज क्या बनाऊँ?", "Mummy: Fridge mein jo bacha hai, usse aaj kya banaun?", lang="hi", tag="mummy", sfx="pop", gap=.2),
    Line(NEWS, "पापा: | बैंक को शिकायत का ईमेल, अंग्रेज़ी में।", "Papa: Bank ko complaint ka email, English mein.", lang="hi", tag="papa", sfx="pop", gap=.2),
    Line(NEWS, "रिया: | कल का एग्ज़ाम, पाँच मिनट में समझाओ।", "Riya: Kal ka exam, 5 minute mein samjhao.", lang="hi", tag="riya", sfx="pop", gap=.2),
    Line(NEWS, "और दादाजी: | मेरी पुरानी फ़ोटो रंगीन कर दो।", "Aur Dadaji: Meri purani photo rangeen kar do.", lang="hi", tag="dadaji", sfx="pop"),
    Line(NEWS, "पर चार साल बाद भी, एक नियम नहीं बदला। | एआई गलत भी हो सकता है। | ज़रूरी बात, ख़ुद जाँचो।", "Par 4 saal baad bhi, ek niyam nahi badla. AI galat bhi ho sakta hai. Zaroori baat, khud jaancho.", lang="hi", tag="rule", drop=True, pre=.2),
    Line(NEWS, "ये रील फ़ैमिली ग्रुप में भेजो, | और पूछो, घर में सबसे ज़्यादा एआई कौन चलाता है?", "Ye reel family group mein bhejo… aur poocho, ghar mein sabse zyada AI kaun chalata hai?", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(NEWS, "चार साल। | एक चैटबॉट।", "4 saal. Ek chatbot.", lang="hi", tag="loop", gap=.05),
]

# ---------------- Dev Katha (Kalamkari Ink) · Ep 1 · "Kashi ka Kotwal kaun?" ----------------
KATHA_V = "parler:Rohit:tense"
KATHA = [
    Line(KATHA_V, "काशी का कोतवाल कौन है? | कोई इंसान नहीं, | भगवान!", "काशी का कोतवाल कौन है? कोई इंसान नहीं… भगवान!", lang="hi", tag="hook", sfx="dingdong", gap=.25),
    Line(KATHA_V, "कहानी शुरू होती है, ब्रह्मा और विष्णु की बहस से, | कि सबसे बड़ा कौन?", "कहानी शुरू होती है ब्रह्मा और विष्णु की बहस से, कि सबसे बड़ा कौन?", lang="hi", tag="debate", sfx="whoosh"),
    Line(KATHA_V, "तभी शिव, एक अनंत ज्योति-स्तंभ बनकर प्रकट हुए।", "तभी शिव, एक अनंत ज्योति-स्तंभ बनकर प्रकट हुए।", lang="hi", tag="pillar", sfx="chime"),
    Line(KATHA_V, "पर ब्रह्मा जी का पाँचवाँ सिर, | अहंकार से जलने लगा।", "पर ब्रह्मा जी का पाँचवाँ सिर, अहंकार से जलने लगा।", lang="hi", tag="ego", sfx="whoosh"),
    Line(KATHA_V, "तब शिव ने अपने क्रोध से, | काल भैरव को प्रकट किया।", "तब शिव ने अपने क्रोध से, काल भैरव को प्रकट किया।", lang="hi", tag="bhairav", sfx="hit"),
    Line(KATHA_V, "भैरव ने वो पाँचवाँ सिर काट दिया, | पर वो सिर, उनके हाथ से चिपक गया!", "भैरव ने वो पाँचवाँ सिर काट दिया… पर वो सिर, उनके हाथ से चिपक गया!", lang="hi", tag="cut", sfx="whoosh"),
    Line(KATHA_V, "भैरव लोक-लोक भटके। | पर सिर नहीं छूटा।", "भैरव लोक-लोक भटके। पर सिर नहीं छूटा।", lang="hi", tag="wander", sfx="whoosh"),
    Line(KATHA_V, "और जैसे ही उन्होंने काशी में क़दम रखा, | सिर ज़मीन पर गिर पड़ा।", "और जैसे ही उन्होंने काशी में क़दम रखा… सिर ज़मीन पर गिर पड़ा।", lang="hi", tag="kashi", sfx="dingdong", drop=True),
    Line(KATHA_V, "उस जगह को आज कहते हैं, | कपाल मोचन तीर्थ।", "उस जगह को आज कहते हैं, कपाल मोचन तीर्थ।", lang="hi", tag="kapal", sfx="chime"),
    Line(KATHA_V, "शिव ने कहा, अब तुम यहीं रहो, काशी की रक्षा करो। | तभी से, काल भैरव हैं, काशी के कोतवाल।", "शिव ने कहा, अब तुम यहीं रहो, काशी की रक्षा करो। तभी से काल भैरव हैं, काशी के कोतवाल।", lang="hi", tag="kotwal", sfx="dingdong"),
    Line(KATHA_V, "उनका वाहन है, एक कुत्ता। | और इस बार काल भैरव जयंती है, मंगलवार, एक दिसंबर।", "उनका वाहन है, एक कुत्ता। और इस बार काल भैरव जयंती है, मंगलवार, 1 दिसंबर।", lang="hi", tag="dog", sfx="tick"),
    Line(KATHA_V, "ये कहानी अपने बनारस वाले दोस्त को भेजो, | और पूछो,", "ये कहानी अपने बनारस वाले दोस्त को भेजो… और पूछो,", lang="hi", tag="cta", sfx="pop", gap=.15),
    Line(KATHA_V, "काशी का कोतवाल कौन है?", "काशी का कोतवाल कौन है?", lang="hi", tag="loop", gap=.05),
]
