import io
import urllib.request
from tkinter import *
from tkinter.ttk import Combobox
import modules.PrepareData as prepare
import modules.recomender.CollaborativeRecomander as cr

from PIL import ImageTk, Image

# colors
# TODO: make to a list of colors
c1 = "#000000"
c2 = "#0A111F"
c3 = "#14213D"
c4 = "#127FFC"
c5 = "#2F90FF"
c6 = "#8DBDF4"
c7 = "#D3E1F1"
c8 = "#E1E2E3"
c9 = "#FFFFFF"
c10 = "#808080"


class Window(Tk):
    def __init__(self, width, height):
        Tk.__init__(self)
        self.title("MovieMatch")
        self.set_location(width, height)
        self.set_icon()
        HomePage(self)

    def set_location(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        self.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))

    def set_icon(self):
        icon_image = PhotoImage(file='')
        # self.iconphoto(False, icon_image)


class StartPage(Frame):
    def __init__(self, parent_frame):
        Frame.__init__(self, parent_frame)


class HomePage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        main = Frame(parent)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.pack(expand=1, fill=BOTH)

        top = Frame(main, height=50)
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.grid(row=0, column=0, sticky='WENS')
        top.grid_propagate(False)
        nav = Frame(top, bg=c9)
        nav.rowconfigure(0, weight=1)
        nav.columnconfigure(0, minsize=375)
        nav.columnconfigure(1, weight=1)
        nav.grid(row=0, column=0, sticky="WENS")

        nav_left = Frame(nav, width=100, bg=c9)
        nav_left.rowconfigure(0, weight=1)
        nav_left.columnconfigure(0, weight=1)
        nav_left.grid(row=0, column=0, sticky="WENS")

        nav_right = Frame(nav, padx=20, bg=c9)
        nav_right.rowconfigure(0, weight=1)
        nav_right.columnconfigure(0, weight=1)
        nav_right.grid(row=0, column=1, sticky="NESE")

        # label = Label(nav_left, text="MovieMatch")
        # label.grid(row=0, column=0)

        # button1 = Button(nav_right, text="Analysis",
        #                      width=20,
        #                      bg=c8,
        #                      border=0,
        #                      highlightthickness=2,
        #                      highlightbackground="red",
        #                      highlightcolor="red",
        #                  command=lambda: self.show_frame(AnalysisPage),)
        # button1.rowconfigure(0, weight=1)
        # button1.columnconfigure(0, weight=1)
        # button1.grid(row=0, column=0, sticky="WENS")

        button2 = Button(nav_right, text="Collaborative", bg=c9, width=30, border=0, command=lambda: self.show_frame(CollaborativePage),)
        button2.rowconfigure(0, weight=1)
        button2.columnconfigure(0, weight=1)
        button2.grid(row=0, column=1, sticky="WENS")

        button3 = Button(nav_right, text="Content", bg=c9, width=30, border=0, command=lambda: self.show_frame(ContentPage), )
        button3.rowconfigure(0, weight=1)
        button3.columnconfigure(0, weight=1)
        button3.grid(row=0, column=2, sticky="WENS")

        content = Frame(main)
        content.grid(row=1, column=0, sticky='WENS')
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        self.frames = {}
        for F in (CollaborativePage, ContentPage):
            frame = F(content, self)
            self.frames[F] = frame
        self.show_frame(CollaborativePage)

    def show_frame(self, f):
        frame = self.frames[f]
        frame.grid(row=0, column=0)
        frame.tkraise()


class CollaborativePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")
        left_content = LeftContent(self, "Collaborative Filtering", "We will recommend some movies by one movie you like")
        collaborative_filter = CollaborativeFilter(left_content)

        RightContent(self, controller, collaborative_filter.get_movie_title())


class CollaborativeFilter(Frame):
    movie_title = ""

    def __init__(self, parent):
        Frame.__init__(self, parent, padx=15, pady=20, bg=c5)
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky="WENS")

        option_title = Label(self, text="Choose a movie you like:", font="Arial 10 bold", bg=c5, fg=c9)
        option_title.grid(row=0, column=0, sticky="NWSW")

        movies = prepare.get_all_movie_titles()

        movie_options = Combobox(self, state="readonly", values=movies)
        movie_options.set("Movies")
        movie_options.grid(row=1, column=0, sticky="WENS")

        frame = Frame(self, height=15, bg=c5)
        frame.rowconfigure(0, weight=1)
        frame.grid(row=2, column=0, sticky="WENS")

        button = Button(self, text="RUN", border=0, bg=c1, fg=c9, command=lambda: self.set_value(movie_options.get()))
        button.grid(row=3, column=0, sticky="WENS")

    def set_value(self, movie_title):
        self.movie_title = movie_title

    def get_movie_title(self):
        return self.movie_title

class ContentPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")
        left_content = LeftContent(self, "Content Filtering",
                                       "We will recommend some movies by your filtering choices")
        # CollaborativeFilter(left_content)
        # RightContent(self)


class LeftContent(Frame):
    def __init__(self, parent, title, description):
        Frame.__init__(self, parent, width=375, bg=c5)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")
        page_title_container = PageTitleContainer(self, title, description)
        page_title_container.grid(row=0, column=0, sticky="WENS")


class RightContent(Frame):
    def __init__(self, parent, controller, filter):
        Frame.__init__(self, parent, bg=c7)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=1, sticky="WENS")

        # TODO: make a if statement to check if user has started system
        # if filter != "":
        #     recomends = cr.recommend_movies(prepare.get_id_by_title(filter), 5)

        RecommendationList(self)
        # else:<
        # default_label = Label(self, text="Nothing is registered.", bg=c7)
        # default_label.grid(row=0, column=0, sticky="WENS")


class PageTitleContainer(Frame):
    def __init__(self, parent, title, description):
        Frame.__init__(self, parent)
        self.configure(bg=c4, height=120, pady=25, padx=15)
        title_ = Label(self, text=title, font="Arial 16 bold", bg=c4, fg=c9)
        title_.grid(row=0, column=0, sticky="NWSW")
        description_ = Label(self, text=description, font="Arial 9 normal", bg=c4, fg=c9)
        description_.grid(row=1, column=0, sticky="NWSW")


class MovieDetails(Frame):
    def __init__(self, parent, movie_title):
        Frame.__init__(self, parent, padx=25, pady=25, bg=c7, border=0)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        card = Frame(self, bg=c9, border=0)
        card.columnconfigure(0, minsize=180)
        card.columnconfigure(1, weight=1)
        card.grid(row=0, column=0, sticky="WENS")

        left = Frame(card, border=0)
        left.grid(row=0, column=0, sticky="WENS")

        right = Frame(card, highlightthickness=2, padx=10, pady=10, bg=c9, border=0)
        right.grid(row=0, column=1, sticky="WENS")

        # TODO: select the right title, poster, short and long summary, link to trailer ..
        poster_url = "https://m.media-amazon.com/images/M/MV5BNjA3NGExZDktNDlhZC00NjYyLTgwNmUtZWUzMDYwMTZjZWUyXkEyXkFqcGdeQXVyMTU1MDM3NDk0._V1_QL75_UX190_CR0,0,190,281_.jpg"
        # urllib.request.urlretrieve(poster_url, "1.png")
        poster_url = urllib.request.urlopen(poster_url).read()
        img = Image.open(io.BytesIO(poster_url))
        image = ImageTk.PhotoImage(img)
        label1 = Label(left, image=image, bg=c9, width=180)
        label1.image=image
        label1.grid(row=0, column=0, sticky="WENS")

        title = Label(right, text=movie_title, font="Arial 20 bold", fg=c1, bg=c9)
        title.grid(row=0, column=0, sticky="NWSW")

        genres = Label(right, text="Action, Fantasy, Sci-fi", bg=c9, fg=c10)
        genres.grid(row=1, column=0, sticky="NWSW")

        rating = Frame(right, pady=10, bg=c9)
        rating.columnconfigure(0, weight=1)
        rating.grid(row=2, column=0, sticky="WENS")
        rating_label = Label(rating, text="Rating:", font="Arial 10 bold", bg=c9)
        rating_label.grid(row=0, column=0, sticky="NWSW")
        rating_description = Label(rating, text="8.7", bg=c9)
        rating_description.grid(row=1, column=0, sticky="NWSW")

        short_summary = Frame(right, pady=10, bg=c9)
        short_summary.columnconfigure(0, weight=1)
        short_summary.grid(row=3, column=0, sticky="WENS")
        short_summary_label = Label(short_summary, text="Short summary:", font="Arial 10 bold", bg=c9)
        short_summary_label.grid(row=0, column=0, sticky="NWSW")
        short_summary_description = Label(short_summary, text="SHORT SUMMARY HERE", bg=c9)
        short_summary_description.grid(row=1, column=0, sticky="NWSW")

        summary = Frame(right, pady=10, bg=c9)
        summary.columnconfigure(0, weight=1)
        summary.grid(row=4, column=0, sticky="WENS")
        summary_label = Label(summary, text="Summary:", font="Arial 10 bold", bg=c9)
        summary_label.grid(row=0, column=0, sticky="NWSW")
        summary_describtion = Label(summary, wraplength=800, text="SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERE SUMMARY HERESUMMARY HERE", bg=c9)
        summary_describtion.grid(row=1, column=0, sticky="NWSW")

        trailer = Frame(right, pady=10, bg=c9)
        trailer.columnconfigure(0, weight=1)
        trailer.grid(row=5, column=0, sticky="WENS")
        trailer_label = Label(trailer, text="Trailer:", font="Arial 10 bold", bg=c9)
        trailer_label.grid(row=0, column=0, sticky="NWSW")
        trailer_link = Label(trailer, text="TRAILER LINK HERE", bg=c9)
        trailer_link.grid(row=1, column=0, sticky="NWSW")


class RecommendationList(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # scroll_frame = LabelFrame()
        #
        # canvas = Canvas(self)
        # canvas.pack(side=LEFT)
        # scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview())
        # scrollbar.pack(side=RIGHT, fill="y")


        # TODO: change to the correct list
        for i in range(2):
            movie_details = MovieDetails(self, i)
            movie_details.grid(row=i, column=0, sticky="WENS")


if __name__ == '__main__':
    window = Window(750, 500)
    window.mainloop()