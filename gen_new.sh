newstring="$(grep main movies.cleaned.csv | tail -1 | sed 's/[^,]*,[^,]*,[^,]*$//')"

cat "$1" | while read movie
do
	echo "$newstring$movie,$movie,"
done
