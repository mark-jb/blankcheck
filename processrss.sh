epnum=1
feed="BC"
if [[ -z "$1" ]]
then
  echo "Need file name as first arg"
  exit 1
fi
if [[ ! -z "$2" ]]
then
  feed=$2
fi

grep "<title>" $1 | tail --lines=+3 | sed 's/^ *//' | sed 's/<\/*title>//g' | tac | while read line;
do
#  echo $line
  echo $line | sed 's, */ *,\n,g' | while read title;
  do
    cleantitle=$(echo $title | sed 's/ with.*//;s/^Praying$/Praying with Anger/')
    cleantitle=$(echo $title | sed 's/Mission: Impossible$/Mission: Impossible 1/')
    cleantitle=$(echo $title | sed 's/Mission: Impossible 2$/Mission: Impossible ii/')
    cleantitle=$(echo $title | sed 's/Mission: Impossible 3$/Mission: Impossible iii/')
    cleantitle=$(echo $title | sed 's/Thor$/Thor 1/')
    echo $feed,$epnum,$cleantitle
  done
  epnum=$((epnum+1))
done
