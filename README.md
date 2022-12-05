# Projekt: MovieMatch🎥
Projektet tager udgangspunkt i at lave et system, som ville kunne komme med forslag til film basseret på en selvvalgt film.

![](images/GUI.png)

Projektet har vi valgt at opdele i to dele: en analyse del og en machine learning del.

#### Analyse del:
Analysen vil dække over et større dataset af film, hvor vi vil med brug af plots forsøge at undersøge og svare på følgende spørgsmål:

1. Hvilke en genre er den som flest film har?
2. Hvilken genre opnår den størst gennemsnitlige indtjening?
3. Hvilken genre opnår den størst gennemsnitlige rating?
4. Hvilke production companies har lavet flest film
5. Hvilket production companies har den største indtjening?
6. Er der en sammenhæng mellem en films budget og dens revenue? (Undersøg med linear regression)
7. Er der en sammenhæng mellem vote-average og profit? (Undersøg med linear regression)
8. Undersøg med et heatmap, hvilke features som har den bedste sammenhæng.
9. Undersøg hvornår en film bliver udgivet på året i forhold til hvor stor indtjening filmen får? Hvilke måned er bedst at udgive en film?
10. Undersøg udvikling i vote-average fra 2000 til 2017.

#### Machine learning:
Vi vil forsøge at bruge clustering til at give et bud på, hvilke film man kan forslå på baggrund af en selvvalgt film.
Vi har desuden valgt, at vi vil fokusere på at kigge på de to filtreringstyper: Collaborative og Content, for at undersøge, hvilken en måde, man bedst ville kunne lave et forslagssystem på.

Der vil laves et grafisk interface, som vi vil bruge til at vise resultatet af forslag for de to filtreringstyper. I den forbindelse vil vi webscrabe information omkring genre, rating, kort- og lang plotbeskrivelse, samt trailer-link, som alt vil blive præsenteret på GUI'en.


### Teknologier:
- pandas
- numpy
- matplotlib
- plotly
- literal_eval
- sklearn (NearestNeighbour, Kmeans)
- BeautifullSoup
- Tkinter
- Seaborn
- wordcloud
- PILLOW
- requests
- re


### Installation guide
Brug denne kommando til at installere alle vores teknologier vi bruger:

    pip3 install -r requirements.txt

### User guide
#### Se vores analyse
Man kan se vores analyse af det store film dataset ved at åbne og køre: **Analyser.ipynb**

#### Brug vores forslagssystem
For at bruge vores forslagsssystem kan du åbne vores GUI med følgende kommando:

    
    python GUI.py

Sådan gør du:
1. Vælg hvilken filtreringstype du vil søge forslag med. Vælg 'Collaborative' eller 'Content' filtrering oppe i højre hjørne af interfacet.
2. Vælge en film i optionmenuen i venstre side af interfacet.
3. Tryk 'RUN' for at søge efter forslag ud fra den film du har valgt.
**(VÆR OPMÆRKSOM PÅ, AT DET KAN TAGE MERE END 5 MIN FØR FORSLAGENE KOMMER)**
4. Der er nu mulighed for at se dine forslag med filmtitel, plakat, genre, plots og trailer-link, som kan sende dig videre til traileren til filmen.

Der er desuden mulighed for at se, hvordan vi har lavet de to forskellige filtreringstyper, ved at åbne og kører .ipynb filerne: 
- **CollaborativeRecommender.ipynb**
- **ContentRecommender.ipynb**


#### Andet
Der er lavet .ipynb filer, som viser hvordan vi blandt andet bruger clustering, webscrabing og wordclouds. Se filerne:
- **Clusters.ipynb**
- **Webscraper.ipynb**
- **WordCloud.ipynb**

### Status
Vi har fået analyseret det store dataset med film med brug af plots. 
Vi har fået lavet et forslagssystem med en GUI, som kan filterer med både 'Collaborative' og 'Content'.

### Challenges
Vi har herunder listet de general største udfordering for dette projekt:
- **Clustering**: vi har skullet koble clustering til vores movie dataset, så vi har kunnet gruppér filmene
- **Webscraping**: vi har villet webscrape filmplakat, trailer-link og andet information, som har skullet bruges til GUI. 
- **Plot illustrationer**: vi har skullet prepare (slice, sortere..) fra dataframe for at kunne lave illustration som ville kunne besvare de analyse spørgsmål vi har stillet os selv.