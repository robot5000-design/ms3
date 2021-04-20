'''Constant Variables.

CSP: Talisman csp settings
TMDB_URLS: Various URL's for accessing the TMDB API
'''

# Talisman CSP settings
CSP = {
    'default-src': [
        '\'none\''
    ],
    'script-src': [
        '\'strict-dynamic\'',
        '\'unsafe-inline\'',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'api.emailjs.com'
    ],
    'font-src': [
        '\'self\'',
        'themes.googleusercontent.com *.gstatic.com',
        'fonts.googleapis.com',
        'cdnjs.cloudflare.com'
    ],
    'style-src': [
        '\'self\'',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'fonts.googleapis.com'
    ],
    'img-src': [
        '\'self\'',
        'image.tmdb.org',
        'data:'
    ],
    'connect-src': [
        '\'self\'',
        'api.emailjs.com'
    ],
    'object-src': [
        '\'none\''
    ],
    'frame-src': [
        'cdn.jsdelivr.net'
    ],
    'base-uri': [
        '\'none\''
    ],
    'frame-ancestors': [
        '\'none\''
    ]
}

# TMDB URL's for poster, general search and getting apecific item details
TMDB_URLS = {
    "tmdb_poster_url": "https://image.tmdb.org/t/p/w500/",
    "search_url": "https://api.themoviedb.org/3/search/{media}?api_key={api_key}&language=\
        en-US&page={page}&include_adult=false&query={query}",
    "detail_url": "https://api.themoviedb.org/3/{media}/{tmdb_id}?api_key={api_key}&language=\
        en-US"
}
