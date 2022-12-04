# Projekt: MovieMatch🎥
Projektet tager udgangspunkt i at lave et system, som ville kunne komme med forslag til film basseret på en selvvalgt film.

![](images/GUI.png)

Projektet har vi valgt at opdele i to dele: en analyse del og en machine learning del.

#### Analyse del:
Analysen vil dække over et større dataset af film, hvor vi vil med brug af plots forsøge at undersøge og svare på følgende spørgsmål:

1. Hvilket production companies har den største indtjening?

2. Er der sammenhæng i hvornår en film bliver udgivet på året i forhold til hvor stor indtjening filmen får?

3. Er der en sammenhæng mellem en films budget og dens revenue?

4. Er der en sammenhæng mellem user-rating og profit?

5. Hvilke genre er den som flest film har?

6. Vis et bar plot med den gennemsnitlige rating for alle genre

7. Vis et bar plot med den gennemsnitlige revenue for alle genre

8. Hvilke production companies har lavet flest film?

#### Machine learning:
Med udgangspunkt i clustering vil vi forsøge at give et bud på, hvilke film man kan forslå på baggrund af en selvvalgt film.
Vi har desuden valgt, at vi vil fokusere på at kigge på de to filtreringstyper: Collaborative og Content, for at undersøge, hvilken en måde, man bedst ville kunne lave et forslagssystem på.

Der vil laves et grafisk interface, som vi vil bruge til at vise resultatet af forslag for de to filtreringstyper. I den forbindelse vil vi webscrabe information omkring genre, rating, kort- og lang plotbeskrivelse, samt trailer-link, som alt vil blive præsenteret på GUI'en.


### Teknologier:
- (list of used technologies)
- Webscrape med BeautifullSoup
- Graphical Interface med Tkinter


### Installation guide


### User guide


### Status



### Analyse spørgsmål
### HUSK:
-> datasettet tager kun højde for biograf revenue, og derfor ikke salg af dvder..

# MovieMatch

- Er der en sammenhæng mellem genre og ratings? Har brugeren nogle særlige præferencer til rating i forhold til valg af genre? Undersøg cluster-grupperne og se på rating og genre for denne gruppe
- Er der en sammenhæng mellem ratings, revenue og budget? Har brugeren en trang til at skulle se film som har en høj rating og revenue og som har været dyr at producere?
- Er der en sammenhæng mellem rating, budget og runtime? Har brugeren en trang til at skulle se film med en høj rating og budget og som har en lang runtime?




Analyse spørgsmål:`
1. Hvilket production companies har den største indtjening?
2. I hvilket land har de den største indtjening?
3. Er der sammenhæng i hvornår en film bliver udgivet på året i forhold til hvor stor indtjening filmen får?
4. Er der en sammenhæng mellem en films budget og dens indtjening?
5. Er der en sammenhæng mellem rating og budget?
6. Vis et bar plot med den gennemsnitlige rating for alle genre
7. Vis et bar plot med den gennemsnitlige indtjening for alle genre
8. Hvilke film har haft den største rating indenfor de sidste 5 år? Hvilken genre tilhører disse film?
`