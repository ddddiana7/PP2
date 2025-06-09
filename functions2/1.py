movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

def is_high_rated(movie):
    return movie["imdb"] > 5.5

def sublist (movies):
    return [movie for movie in movies if movie['imdb'] > 5.5]

#print (sublist(movies))

def category (movies, category):
    return [movie for movie in movies if movie["category"] == category]
#print(category(movies, "Thriller"))

def avg_value (movies):
    total = 0
    for movie in movies:
        total += movie["imdb"]
    return total/len(movies)
#print(avg_value(movies))

def avg_of_category(movies, category):
    total = 0
    count = 0
    for movie in movies:
        if movie["category"] == category:
                total += movie['imdb']
                count +=1
    if count <= 0:
         return 0
    else:return total/count

#print(avg_of_category(movies, "Thriller"))

import random

random_movie = random.choice(movies)
random_category = random.choice([movie["category"] for movie in movies])

print(f"1. Is '{random_movie['name']}' highly rated? ", is_high_rated(random_movie))

print("2. Highly rated movies:")
for movie in sublist(movies):
    print("   ", movie["name"])

print(f"3. Movies in random category '{random_category}':")
for movie in category(movies, random_category):
    print("   ", movie["name"])

print("4. Average IMDB score of all movies:", avg_value(movies))

print(f"5. Average IMDB score in category '{random_category}':", avg_of_category(movies, random_category))