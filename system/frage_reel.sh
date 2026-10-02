#!/bin/sh
# Baut ein Frage-Reel. Aufruf: frage_reel.sh <name> "<Frage>" "<einen Freund|eine Freundin>" [dauer]
# Ergebnis: ../media/reels/reel-<name>.mp4, Klangbett 1 (Flaeche).
set -e
cd "$(dirname "$0")"
NAME="$1"; Q="$2"; WEM="$3"; DUR="${4:-9}"
TMP=$(mktemp -d)
python3 -c "import json,sys; json.dump({'q':sys.argv[1],'wem':sys.argv[2],'dur':float(sys.argv[3])}, open(sys.argv[4],'w'), ensure_ascii=False)" "$Q" "$WEM" "$DUR" "$TMP/tl.json"
FADE=$(python3 -c "print(float('$DUR')-1.2)")
ffmpeg -y -loglevel error -stream_loop -1 -i klang/1-flaeche.wav -t "$DUR" -af "afade=t=in:st=0:d=0.3,afade=t=out:st=$FADE:d=1.2" "$TMP/bett.wav"
python3 render_reel.py reel3.html "$DUR" "$TMP/bett.wav" "../media/reels/reel-$NAME.mp4" "$TMP/tl.json"
rm -rf "$TMP"
