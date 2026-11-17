#!/usr/bin/env bash
# Altın yanıt test koşumu: bir setin partilerini sırayla koşturur (yazar → bekle → rapor → denetim).
#
# Kullanım (depo kökünden):
#   bash scripts/altin_kosumu/zincir.sh SET BRIEF:A:B [BRIEF:A:B ...]
#   Parti listesi: python3 scripts/altin_kosumu/brief_uret.py .   (brief'leri de yeniden üretir)
#
# Güvenceler:
# - Yazar yalnız gemini-4-argon olabilir. Araç başka bir modele geçecekse parti başlatılmaz; koşum
#   sırasında geçerse işçi durdurulur ve dosya parti öncesindeki hâline alınır.
# - Parti kabul edilmezse (denetim geçmezse ya da koşum yarıda kalırsa) zincir durur.
# - Geliştirici körlüğü: bu betik madde metni yazdırmaz; yazar raporu süzülerek kaydedilir.
set -u
KOK=$(git rev-parse --show-toplevel) || exit 9
ARAC=$KOK/scripts/altin_kosumu
T=$KOK/.agentack/altin_kosumu          # çalışma klasörü (git dışı): kopya/, rapor/, asama1/
ASAMA1=fd6d9cb                          # test dosyalarının birinci aşama hâlini taşıyan commit
A="python3 $HOME/.claude/skills/agentack/scripts/agentack.py"
YAZAR="agy gemini-4-argon-high"
SET=$1; shift
cd "$KOK" || exit 9
mkdir -p "$T/rapor" "$T/kopya" "$T/asama1"
[ -s "$T/asama1/$SET.test.jsonl" ] || git show "$ASAMA1:eval/datasets/$SET/test.jsonl" > "$T/asama1/$SET.test.jsonl"

geri_al() { cp "$T/kopya/$1.once.jsonl" "eval/datasets/$SET/test.jsonl"; }

for spec in "$@"; do
  IFS=: read -r brief a b <<<"$spec"
  ad="$SET-$a-$b"
  secim=$($A resolve --role architect --avoid claude \
          | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("provider"), d.get("model"))')
  if [ "$secim" != "$YAZAR" ]; then
    echo "$ad: yazar modeli kullanılamıyor (araç şunu seçiyor: $secim); zincir durdu"; exit 5
  fi
  cp "eval/datasets/$SET/test.jsonl" "$T/kopya/$ad.once.jsonl"
  id=$($A dispatch --role architect --avoid claude --mode write --timeout 90 --in claude --brief "$brief" \
        | python3 -c 'import json,sys; print(json.load(sys.stdin).get("run_id",""))')
  if [ -z "$id" ]; then echo "$ad: yazar başlatılamadı"; exit 2; fi
  echo "$ad: koşum $id başladı $(date +%H:%M)"
  meta=".agentack/runs/$id/meta.json"
  while :; do
    bitti=$($A wait "$id" --timeout 15 | python3 -c 'import json,sys; print(json.load(sys.stdin).get("all_finished"))')
    yabanci=$(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); print(any(a.get("provider")!="agy" for a in m.get("attempts",[])) or m.get("provider") not in (None,"agy"))' "$meta")
    if [ "$yabanci" = "True" ]; then
      ust=$(pgrep -f "agentack.py _exec $KOK/.agentack/runs/$id" | head -1)
      [ -n "$ust" ] && { pkill -P "$ust"; kill "$ust"; }
      sleep 2; geri_al "$ad"
      echo "$ad: araç başka modele geçti; işçi durduruldu, dosya parti öncesine alındı; zincir durdu"; exit 6
    fi
    [ "$bitti" = "True" ] && break
  done
  ozet=$(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); print(m.get("status"), m.get("provider"), m.get("model"), m.get("minutes"))' "$meta")
  echo "$ad: $ozet"
  if [ "$ozet" = "${ozet#done $YAZAR }" ]; then
    geri_al "$ad"
    echo "$ad: koşum tamamlanmadı; dosya parti öncesine alındı; zincir durdu"; exit 3
  fi
  cp "eval/datasets/$SET/test.jsonl" "$T/kopya/$ad.sonra.jsonl"
  $A result "$id" > "$T/rapor/$ad.ham.md"
  if ! python3 "$ARAC/parti_denetim.py" "$KOK" "$SET" "$a" "$b" "$T/kopya/$ad.once.jsonl" \
        "$T/asama1/$SET.test.jsonl" "$T/rapor/$ad.ham.md" "$T/rapor/$ad.md"; then
    echo "$ad: denetim geçmedi; zincir durdu (dosya olduğu gibi bırakıldı, geri almak için kopya/$ad.once.jsonl)"; exit 4
  fi
done
echo "$SET: zincir bitti"
