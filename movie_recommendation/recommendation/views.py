from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
import pandas as pd
lst=[]
df=pd.read_csv('movie_dataset.csv')
# print(df.head(3))
features=['title','genres','keywords','original_language','overview','tagline','cast','director']
df2=df[features]
df2[features]=df2[features].fillna(' ')
df2['total']=""
for i in features:
    df2['total']+=df2[i]+" "
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['total'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)
df2=df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
def get_recommendations_new(title, cosine_sim=cosine_sim):
    lst=[]
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:21]

    movie_indices = [i[0] for i in sim_scores]
    for i in movie_indices:
        
        lst.append([df2['title'][i],df['genres'][i],df['tagline'][i],df['cast'][i],df['director'][i],df2['original_language'][i]])
    # for movie in movies[1]:
        # lst.append(movie)

    print(lst)
    return lst

def home(request):
    lst=[]
    if request.method=='POST':
        movie_name=request.POST.get('movie_name')
        lst=get_recommendations_new(movie_name)
    context={
        'recommen':lst
        }
    return render(request, 'home.html',context)