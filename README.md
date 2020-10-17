# Free Netflix Backend

- To search for movie poster goto /search/<film> and replace <film> with movie series name

- To get movie details goto api/search/<film> and replace <film> with movie series name
  Sample response data
  ```json
    {
        "data": {
            "backdrop_path": "https://image.tmdb.org/t/p/w500/cyMRFJzUv5awIBTyNlr1FAeScfh.jpg", 
            "isSeries": false, 
            "overview": "CIA employee Edward Snowden leaks thousands of classified documents to the press.", 
            "poster_path": "https://image.tmdb.org/t/p/w500/yfK7zxNL63VWfluFuoUaJj5PdNw.jpg", 
            "release_date": "2016-09-15", 
            "title": "Snowden", 
            "tmdb_id": 302401, 
            "unique": "9d9a05cd-aa7d-4c9f-9c7d-2f434d35cdfe", 
            "views": 0, 
            "vote_average": 7.1
        }, 
        "status": 200
    }
  ```
- Other routes
  - /api/horror/all
  - /api/horror/<film>
  - /api/scifi/all
  - /api/scifi/<film>
  - /api/romantic/all
  - /api/romantic/<film>
  - /api/action/all
  - /api/action/<film>
  - /api/others/all
  - /api/others/<film>
  - api/english/series/all
  - api/english/series/<film>
  - api/hindi/series/all
  - api/hindi/series/<film>