$node = (27..512)

foreach ($n in $node){
    python spectrogram.py --set $n
}