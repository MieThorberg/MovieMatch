import io
import urllib.request
import webbrowser
from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from modules.webscrape import Webscraper as ws
import modules.recommmender.CollaborativeRecommender as cr
import modules.PrepareData as prepare
import modules.recommmender.ContentRecommender as content

# Graphical User Interface (GUI)
# Showing the results of recommendations by searching with Collaborative and Content filtering.
# Constructed object-oriented with Tkinter framework.
# See Tkinter documentation: https://docs.python.org/3/library/tk.html


colors = [
    "#FFFFFF",  # white
    "#F7F7F7",  # white/grey
    "#404040",  # light grey
    "#1A1A1A",  # grey
    "#202020",  # dark grey
    "#000000",  # black
    "#FFD100"  # yellow
]


# ---------- WINDOW VIEW: ----------
class Window(Tk):
    def __init__(self, width, height):
        # initialize the window view
        Tk.__init__(self)
        self.title("MovieMatch")
        # placing window at the center of your screen
        self.set_location(width, height)
        self.set_icon()
        # layout of the window
        Main(self)

    def set_location(self, width, height):
        # the width and height of screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # calculate the x and y coordinates for placing window at center of the screen
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        # setting the window width, height and place it by the x and y coordinate
        self.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))

    def set_icon(self):
        icon_image = PhotoImage(file="images/icon.png")
        self.iconphoto(False, icon_image)


# ---------- MAIN FRAME: ----------
class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # MAIN
        main = Frame(parent)
        # grid organizing
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.pack(expand=True, fill=BOTH)

        # TOP - contains the navigation bar
        top = Frame(main, height=50, bg=colors[0])
        # grid organizing
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.grid(row=0, column=0, sticky='WENS')  # 'WENS' means placing the grid in center
        top.grid_propagate(False)  # stops the frame from shrinking
        # adding a navigation bar to the top frame
        NavigationBar(top, self)

        # MAIN CONTENT - contains the pages
        main_content = Frame(main)
        main_content.grid(row=1, column=0, sticky='WENS')
        main_content.columnconfigure(0, weight=1)
        main_content.rowconfigure(0, weight=1)

        # save all pages in a list
        self.frames = {}
        for F in (CollaborativePage, ContentPage):
            frame = F(main_content)
            self.frames[F] = frame

        # first page to show on content frame
        self.show_frame(CollaborativePage)

    def show_frame(self, f):
        # gets the specific frame from the list of frames
        frame = self.frames[f]
        frame.grid(row=0, column=0)
        # raise frame to be first on top, so it will be visible on window
        frame.tkraise()


# ---------- TOP NAVIGATION: ----------
class NavigationButton(Button):
    def __init__(self, parent, controller, frame, text, column):
        Button.__init__(self,
                        parent,
                        text=text,
                        bg=colors[0],
                        width=30,
                        border=0,
                        command=lambda: controller.show_frame(frame)
                        )
        # grid organizing
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=column, sticky="WENS")


class NavigationBar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # grid organizing
        navigation_bar = Frame(parent, bg=colors[0])
        navigation_bar.rowconfigure(0, weight=1)
        navigation_bar.columnconfigure(0, weight=1)
        navigation_bar.grid(row=0, column=0, sticky="NESE")  # 'NESE' means placing the grid from the right
        # adding buttons to the navigation bar
        NavigationButton(navigation_bar,  # parent frame
                         controller,  # main frame
                         CollaborativePage,  # page frame to view when button is clicked
                         "Collaborative",  # text
                         0  # column index
                         )
        NavigationButton(navigation_bar,
                         controller,
                         ContentPage,
                         "Content",
                         1
                         )


# ---------- MAINCONTENT FRAME: (Divided in LEFT & RIGHT) ----------
class LeftContent(Frame):
    def __init__(self, parent, title, description, filter_frame):
        Frame.__init__(self, parent, width=375, bg=colors[4])
        # grid organizing
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # TOP - showing the title and small description
        page_title_container = PageTitleContainer(self, title, description)
        page_title_container.grid(row=0, column=0, sticky="WENS")

        # FILTER - show either CollaborativeFilter or ContentFilter
        filter_frame(self, parent)


class PageTitleContainer(Frame):
    def __init__(self, parent, title, description):
        Frame.__init__(self, parent)
        self.configure(bg=colors[3], height=120, pady=25, padx=15)

        # TITLE
        title_ = Label(self, text=title, font="Arial 16 bold", bg=colors[3], fg=colors[0])
        title_.grid(row=0, column=0, sticky="NWSW")

        # DESCRIPTION
        description_ = Label(self, text=description, font="Arial 9 normal", bg=colors[3], fg=colors[0])
        description_.grid(row=1, column=0, sticky="NWSW")


class RightContent(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=colors[2], highlightthickness=0)
        # grid organizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=1, sticky="WENS")
        # The default frame to view the first time the content are shown
        self.frame = NothingRegisteredFrame(self)

    def show_frame(self, new_frame):
        self.frame.pack_forget()  # delete the frame from RightContent
        self.frame = new_frame
        self.frame.tkraise()  # show the new frame on RightContent


# default frame to show on RightContent, when there is no recommendations
class NothingRegisteredFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)

        label = Label(self, text="Nothing is registered.", fg=colors[0], bg=colors[2])
        label.pack(fill=BOTH, expand=True)


# ---------- COLLABORATIVE-BASED FILTERING PAGE: ----------
class CollaborativePage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=colors[4])
        # grid organizing
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # LEFT SIDE - shows the filter menu
        LeftContent(self,
                    "Collaborative Filtering",  # title
                    "Recommend by comparing to ratings of others",  # description
                    CollaborativeFilter  # filter frame
                    )

        # RIGHT SIDE - shows recommendations
        self.right_content = RightContent(self)

    # used to reload the RightContent when a new recommendation is requested
    def reload_right_content(self, recommendations):
        if len(recommendations) != 0:  # check if there is registered some recommendations
            # make a new scroll frame which contains a RecommendationList with the recommendations
            scroll_frame = ScrollableFrame(self.right_content, RecommendationList, recommendations)
            # show the new scroll frame in the RightContent frame
            self.right_content.show_frame(scroll_frame)
        else:
            # shows a frame that says "Nothing registered" in the RightContent
            nothing_registered_frame = NothingRegisteredFrame(self.right_content)
            self.right_content.show_frame(nothing_registered_frame)


class CollaborativeFilter(Frame):
    # gets movies from the big movie dataset
    movies = prepare.get_all_movie_titles()
    recommendations = []

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, padx=15, pady=20, bg=colors[4])
        # grid organizing
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky="WENS")

        # place movie filter
        self.movie_filter = MovieFilter(self,  # parent frame
                                        self.movies,  # movie list
                                        self.recommend  # recommendation function
                                        )

    def recommend(self):
        # find the movie selected from the filtering menu
        movie = self.movie_filter.getMovie()
        # translate the title into an index
        index = prepare.get_movie_index_by_title(movie)
        # find the recommendations by the index of the movie
        self.recommendations = cr.recommend_movies(index, 5)
        # reload right content frame to view the new recommendations
        self.controller.reload_right_content(self.recommendations)


# ---------- CONTENT-BASED FILTERING PAGE: ----------
class ContentPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=colors[4])
        # grid organizing
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # LEFT SIDE - shows the filter menu
        LeftContent(self,
                    "Content Filtering",
                    "Recommend by the genre, cast, keywords and more",
                    ContentFilter)

        # RIGHT SIDE - shows recommendations
        self.right_content = RightContent(self)

    def reload_right_content(self, recommendations):
        if len(recommendations) != 0:
            scroll_frame = ScrollableFrame(self.right_content, RecommendationList, recommendations)
            self.right_content.show_frame(scroll_frame)
        else:
            nothing_registered_frame = NothingRegisteredFrame(self.right_content)
            self.right_content.show_frame(nothing_registered_frame)


class ContentFilter(Frame):
    # gets movies from the smaller movie dataset
    movies = prepare.get_all_movie_titles1()
    recommendations = []

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, padx=15, pady=20, bg=colors[4])
        # grid organizing
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky="WENS")

        # place movie filter
        self.movie_filter = MovieFilter(self,
                                        self.movies,
                                        self.recommend
                                        )

    def recommend(self):
        # find the movie selected from the filtering menu
        movie = self.movie_filter.getMovie()
        # find the recommendations by the title of the movie
        self.recommendations = content.recommend_movies(movie, 5)
        # reload right content frame to view the new recommendations
        self.controller.reload_right_content(self.recommendations)


# ---------- FILTER: ----------
class MovieFilter(Frame):
    def __init__(self, parent, movies, filter_func):
        Frame.__init__(self, parent, bg=colors[4])
        # grid organizing
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # OPTION - choose movie
        option_title = Label(self, text="Choose a movie you like:", font="Arial 10 bold", bg=colors[4], fg=colors[0])
        option_title.grid(row=0, column=0, sticky="NWSW") # 'NWSW' means placing grid from the left
        self.movie_options = Combobox(self, state="readonly", values=movies)
        self.movie_options.set("Movies")  # sets the default text
        self.movie_options.grid(row=1, column=0, sticky="WENS")

        # EMPTY - frame to make some space between option and button
        frame = Frame(self, height=15, bg=colors[4])
        frame.rowconfigure(0, weight=1)
        frame.grid(row=2, column=0, sticky="WENS")

        # RUN BUTTON
        button = Button(self,
                        text="RUN",
                        border=0,
                        bg=colors[6],
                        fg=colors[5],
                        command=lambda: filter_func() # runs the specific filtering recommendation function
                        )
        button.grid(row=3, column=0, sticky="WENS")

    def getMovie(self):
        return self.movie_options.get()


# ---------- MOVIE RECOMMENDATION: ----------
class RecommendationList(Frame):
    def __init__(self, parent, recommendations):
        Frame.__init__(self, parent, highlightthickness=0, bg=colors[2])

        for movie_title in recommendations:
            movie_details = MovieDetails(self, movie_title)
            movie_details.pack(fill=BOTH, expand=True)


class MovieDetails(Frame):
    def __init__(self, parent, movie_title):
        Frame.__init__(self, parent, bg=colors[2], highlightthickness=0, pady=25)
        self.pack(fill=BOTH, expand=True, padx=(25, 40))

        # Find movie information by movie title
        imdb_id = prepare.get_imdb_id_by_title(movie_title)

        # CARD
        card = Frame(self, bg=colors[0], highlightthickness=0)
        card.pack(fill=BOTH, expand=True)

        # LEFT COLUMN - showing the movie poster
        left = Frame(card, highlightthickness=0)
        left.columnconfigure(0, weight=1)
        left.grid(row=0, column=0, sticky="WENS")

        # RIGHT COLUMN - show details of the movie
        right = Frame(card, highlightthickness=0, padx=10, pady=10, bg=colors[0])
        right.rowconfigure(0, weight=1)
        right.grid(row=0, column=1, sticky="WENS")

        # TITLE
        title = Label(right, text=movie_title, font="Arial 20 bold", fg=colors[5], bg=colors[0])
        title.grid(row=0, column=0, sticky="NWSW")

        # TODO: select the genres plus rating ..
        if imdb_id != -1:
            poster_url = ws.get_poster(imdb_id)
            short_summary_text = ws.get_summaries(imdb_id)[0].text
            self.summary_text = self.get_summary(imdb_id)
            self.trailer_text = ws.get_trailer(imdb_id)
            genres_text = "Genre: " + ', '.join(ws.get_genres(imdb_id))
            rating_text = ws.get_rating(imdb_id)

            # MOVIE POSTER
            poster_url = urllib.request.urlopen(poster_url).read()
            img = Image.open(io.BytesIO(poster_url))
            image = ImageTk.PhotoImage(img)
            label1 = Label(left, image=image, bg=colors[0], width=180, highlightthickness=0, border=0)
            label1.image = image
            label1.grid(row=0, column=0, sticky="WENS")

            # GENRES
            genres = Label(right, text=genres_text, bg=colors[0], fg=colors[2])
            genres.grid(row=1, column=0, sticky="NWSW")

            # RATING
            rating = Frame(right, pady=10, bg=colors[0])
            rating.columnconfigure(0, weight=1)
            rating.grid(row=2, column=0, sticky="WENS")
            rating_label = Label(rating, text="Rating:", font="Arial 10 bold", bg=colors[0])
            rating_label.grid(row=0, column=0, sticky="NWSW")
            rating_description = Label(rating, text=rating_text, bg=colors[0])
            rating_description.grid(row=1, column=0, sticky="NWSW")

            # SHORT SUMMARY
            short_summary = Frame(right, pady=10, bg=colors[0])
            short_summary.columnconfigure(0, weight=1)
            short_summary.grid(row=3, column=0, sticky="WENS")
            short_summary_label = Label(short_summary,
                                        text="Short summary:",
                                        font="Arial 10 bold",
                                        bg=colors[0]
                                        )
            short_summary_label.grid(row=0, column=0, sticky="NWSW")
            short_summary_description = Label(short_summary,
                                              text=short_summary_text,
                                              bg=colors[0],
                                              wraplength=800,
                                              justify="left"
                                              )
            short_summary_description.grid(row=1, column=0, sticky="NWSW")

            # SUMMARY
            summary = Frame(right, pady=10, bg=colors[0])
            summary.columnconfigure(0, weight=1)
            summary.grid(row=4, column=0, sticky="WENS")
            summary_label = Label(summary,
                                  text="Summary:",
                                  font="Arial 10 bold",
                                  bg=colors[0]
                                  )
            summary_label.grid(row=0, column=0, sticky="NWSW")
            summary_describtion = Label(summary,
                                        wraplength=800,
                                        text=self.summary_text,
                                        justify="left",
                                        bg=colors[0]
                                        )
            summary_describtion.grid(row=1, column=0, sticky="NWSW")

            # TRAILER LINK
            self.trailer = Frame(right, pady=10, bg=colors[0])
            self.trailer.columnconfigure(0, weight=1)
            self.trailer.grid(row=5, column=0, sticky="WENS")
            self.trailer_label = Label(self.trailer,
                                       text="Trailer:",
                                       font="Arial 10 bold",
                                       bg=colors[0]
                                       )
            self.trailer_label.grid(row=0, column=0, sticky="NWSW")
            self.place_trailer_link()

    def open_trailer(self, url):
        webbrowser.open_new_tab(url)

    def place_trailer_link(self):
        if self.trailer_text != "":
            trailer_link = Label(self.trailer, text=self.trailer_text, bg=colors[0],
                                 fg="blue",
                                 cursor="hand2")
            trailer_link.bind("<Button-1>", lambda e: self.open_trailer(self.trailer_text))
        else:
            trailer_link = Label(self.trailer, text="No trailer registered", bg=colors[0])
        trailer_link.grid(row=1, column=0, sticky="NWSW")

    def get_summary(self, imdb_id):
        summaries = ws.get_summaries(imdb_id)
        if len(summaries) == 1:
            return "No summary registered"
        else:
            return summaries[1].text


# ---------- SCROLL: ----------
class ScrollableFrame(Frame):
    def __init__(self, parent, frame, recommendations):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self, highlightthickness=0, bg="blue")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.frame = frame(self.canvas, recommendations)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        scroll = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=scroll.set)

        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind("<Configure>", self.FrameWidth)
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")


if __name__ == '__main__':
    window = Window(750, 500)
    window.mainloop()
