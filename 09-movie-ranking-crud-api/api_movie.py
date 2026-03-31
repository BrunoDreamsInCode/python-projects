import requests, os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv(dotenv_path="env")
api_key = os.getenv("API_KEY")



def search_movie(query):
    query_params = {
        "query": query,
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url="https://api.themoviedb.org/3/search/movie", headers=headers, params=query_params)
    response.raise_for_status()
    print(response.status_code)
    print(response.text)

    movies = []
    data = response.json()
    for movie in data["results"]:
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie["release_date"][:4] if movie["release_date"] else "N/A",
        })

    return movies



def get_movie_by_id(id):
    id_url = f"https://api.themoviedb.org/3/movie/{id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url=id_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    movie_info = []


    movie_info = ({
        "id": data["id"],
        "title":data["original_title"],
        "url_img":data["poster_path"],
        "year": data["release_date"][:4] if data["release_date"] else None,
        "description":data["overview"],
    })

    return movie_info


