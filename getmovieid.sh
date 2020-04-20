#!/bin/bash
alias urldecode='python -c "import sys, urllib as ul; \
    print ul.unquote_plus(sys.argv[1])"'

alias urlencode='python -c "import sys, urllib as ul; \
    print ul.quote_plus(sys.argv[1])"'

TITLE=$1
echo encoding $TITLE

ENC=$(urlencode "$TITLE")

echo encoded: $ENC

curl "https://api.themoviedb.org/3/search/movie?api_key=8f73ecf74c30703e387fd22fae272a12&language=en-US&query=$ENC&page=1&include_adult=false" | jq '.results[] | [.id, .original_title]'
