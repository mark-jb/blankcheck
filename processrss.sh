epnum=1
grep "<title>" | tail --lines=+3 | sed 's/^ *//' | sed 's/<\/*title>//g' | tac | while read line;
do
#  echo $line
  echo $line | sed 's, */ *,\n,g' | while read title;
  do
    cleantitle=$(echo $title | sed 's/ with.*//;s/^Praying$/Praying with Anger/')
    echo $epnum,$cleantitle
  done
  epnum=$((epnum+1))
done
