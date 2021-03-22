curl https://api.themoviedb.org/3/movie/550/credits?api_key=$APIKEY | jq '.cast | .[].name'
