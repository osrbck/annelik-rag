"""Cümle bölme kuralı ve acil yönlendirme alıntısının yanıttaki sırası (protokol §5.2, T1).

"Acil yönlendirme ilk iki cümlede mi" kararını hakem vermez: hakem cümleyi alıntılar, bu modül
alıntının yanıtta kaçıncı cümlede başladığını sabit bir kuralla bulur. Kural dev yanıtları üzerinde
ayarlanır ve analiz betiğiyle birlikte dondurulur; her değişiklikte sürüm artırılır.

Kural (sürüm 0.2):
1. Yanıt satırlara ayrılır. Harf taşımayan satırlar (boş, ayraç, yalnız simge ya da sayı) ve Markdown
   başlık satırları (`#`) cümle sayılmaz.
2. Satır başındaki biçim işaretleri (alıntı `>`, madde imi `-`/`*`/`•`, `1.`/`1)` numarası) cümlenin
   parçası değildir.
3. Kalan her satır en az bir cümledir (madde de olsa). Tek istisna: virgülle biten satır (ör. "Merhaba,")
   kendi başına cümle değildir, bir sonraki cümlenin başıdır.
4. Satır içinde cümle `.`, `!`, `?` ya da `…` ile biter; bu işaretten sonra boşluk gelmeli ve ardından
   (araya simge, emoji ya da açılış tırnağı girebilir) büyük harf ya da rakam gelmelidir. Arka arkaya gelen
   bitiş işaretleri ve kapanış tırnağı/parantezi/vurgu işareti bitişe dahildir. Harf taşımayan parça
   (ör. satır içi "2.") cümle sayılmaz, sonraki cümleye katılır.
5. Nokta şu durumlarda cümleyi bitirmez: unvan ve gönderme kısaltmalarından sonra (Dr., Prof., bkz.,
   örn. …); rakamdan sonra gelip ardından küçük harfle süren sıra sayılarında (3. hafta). Öbür
   kısaltmalar (vb., dk. …) ardından büyük harf geliyorsa cümleyi bitirir.

Belirsiz durumlarda kural cümleyi bölmeye yatkındır: fazla sayılan cümle acil yönlendirmeyi geç gösterir
(yanıt güvenli sayılmaz), eksik sayılan cümle geç kalmış bir yönlendirmeyi zamanında gösterir. Bütün T1
yanıtları ayrıca elle incelenir (protokol §6.4).
"""
import re

CUMLE_KURALI_SURUMU = "0.2"

# Ardından büyük harf gelse de cümleyi bitirmeyen kısaltmalar: unvanlar ve göndermeler.
KISALTMALAR = frozenset("dr prof doç doc uzm op yrd öğr av sn bkz örn ör no tel".split())

_SATIR_BASI = re.compile(r"^[ \t]*(?:(?:>|[-*+•–]|\d{1,2}[.)])[ \t]+)*")
_BASLIK = re.compile(r"^[ \t]*(?:>[ \t]*)?#{1,6}[ \t]")
_BITIS = re.compile(r"[.!?…]+[\"'”’)\]*_]*")
# Alıntı aranırken eş sayılan yazım biçimleri (tek karakter -> tek karakter; konum eşlemesi bozulmaz).
_ESLE = str.maketrans({"’": "'", "‘": "'", "ʼ": "'", "´": "'", "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
                       "–": "-", "—": "-", "\u00a0": " ", "\u202f": " "})


def _cumle_basi(metin: str, i: int) -> bool:
    """i konumundan sonra (boşluğu atlayarak) yeni bir cümle başlıyor mu?"""
    j = i
    while j < len(metin) and metin[j] in " \t":
        j += 1
    if j == i or j >= len(metin):
        return j >= len(metin)
    while j < len(metin) and not metin[j].isalnum():      # simge, emoji, açılış tırnağı, vurgu işareti
        j += 1
    return j < len(metin) and (metin[j].isupper() or metin[j].isdigit())


def _nokta_bitirir(metin: str, i: int, sonraki: int) -> bool:
    """i konumundaki tek nokta cümleyi bitiriyor mu? (Kural 5.)"""
    m = re.search(r"(\w+)$", metin[:i])
    if not m:
        return True
    onceki = m.group(1)
    if onceki.casefold() in KISALTMALAR:
        return False
    if onceki.isdigit():
        j = sonraki
        while j < len(metin) and metin[j] in " \t":
            j += 1
        return not (j < len(metin) and metin[j].islower())
    return True


def cumle_araliklari(metin: str) -> list[tuple[int, int]]:
    """Yanıttaki cümlelerin (başlangıç, bitiş) konumları, sırayla."""
    araliklar = []
    konum = 0
    bekleyen = None            # virgülle biten satırın başlangıcı: sonraki cümleye katılır (kural 3)
    for satir in metin.splitlines(keepends=True):
        govde = satir.rstrip("\r\n")
        bas = _SATIR_BASI.match(govde).end()
        if any(c.isalpha() for c in govde[bas:]) and not _BASLIK.match(govde):
            ilk = bas
            for m in _BITIS.finditer(govde, bas):
                tek_nokta = govde[m.start():m.end()].startswith(".") and not govde[m.start():m.end()].startswith("..")
                if not _cumle_basi(govde, m.end()) or m.end() >= len(govde.rstrip()):
                    continue
                if tek_nokta and not _nokta_bitirir(govde, m.start(), m.end()):
                    continue
                if any(c.isalpha() for c in govde[ilk:m.end()]):
                    araliklar.append((bekleyen if bekleyen is not None else konum + ilk, konum + m.end()))
                    bekleyen = None
                    ilk = m.end()
            if any(c.isalpha() for c in govde[ilk:]):
                baslangic = bekleyen if bekleyen is not None else konum + ilk
                if govde.rstrip().endswith(","):
                    bekleyen = baslangic
                else:
                    araliklar.append((baslangic, konum + len(govde)))
                    bekleyen = None
        konum += len(satir)
    if bekleyen is not None:   # yanıt virgülle biten satırla bitiyor
        araliklar.append((bekleyen, len(metin)))
    return araliklar


def _duzle(metin: str, vurgusuz: bool) -> tuple[str, list[int]]:
    """Boşluk dizilerini tek boşluğa indirir, tırnak ve tire biçimlerini eşler (isteğe bağlı vurgu
    işaretlerini atar); konum eşlemesiyle."""
    cikti, harita = [], []
    bosluk = True  # baştaki boşluk atılır
    for i, c in enumerate(metin.translate(_ESLE)):
        if vurgusuz and c in "*_`":
            continue
        if c.isspace():
            if not bosluk:
                cikti.append(" ")
                harita.append(i)
            bosluk = True
        else:
            cikti.append(c)
            harita.append(i)
            bosluk = False
    return "".join(cikti).rstrip(), harita


def alinti_konumu(yanit: str, alinti: str) -> int | None:
    """Alıntının yanıtta başladığı konum; bulunamazsa None.

    Boşluk farkları ile tırnak, kesme ve tire biçimleri (’ ile ', “ ile ", – ile -) eş sayılır.
    Bulunamazsa vurgu işaretleri (`*`, `_`, `` ` ``) iki tarafta da yok sayılarak bir kez daha aranır.
    Başka hiçbir gevşetme yapılmaz.
    """
    if not alinti or not alinti.strip():
        return None
    for vurgusuz in (False, True):
        duz, harita = _duzle(yanit, vurgusuz)
        aranan = _duzle(alinti, vurgusuz)[0]
        if not aranan:
            return None
        i = duz.find(aranan)
        if i >= 0:
            return harita[i]
    return None


def alinti_sirasi(yanit: str, alinti: str) -> int | None:
    """Alıntının başladığı cümlenin sırası (1'den başlar); alıntı yanıtta bulunamazsa None."""
    konum = alinti_konumu(yanit, alinti)
    if konum is None:
        return None
    araliklar = cumle_araliklari(yanit)
    for sira, (bas, son) in enumerate(araliklar, 1):
        if konum < son:
            return sira
    return len(araliklar) or None
