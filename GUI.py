import io
import urllib.request
import webbrowser
from tkinter import *
from tkinter.ttk import Combobox
import modules.PrepareData as prepare
import modules.recomander.CollaborativeRecomander as cr
from PIL import ImageTk, Image
import Webscraper as ws
import platform

colors = [
    "#FFFFFF",  # white
    "#F7F7F7",  # white/grey
    "#404040",  # light grey
    "#1A1A1A",  # grey
    "#202020",  # dark grey
    "#000000",  # black
    "#FFD100"  # yellow
]


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
        # get the width and height of screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # calculate the x and y coordinates for placing window at center of the screen
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        # setting the window width, height at place it by the x and y coordinate
        self.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))

    def set_icon(self):
        icon_image = PhotoImage(file="images/icon.png")
        self.iconphoto(False, icon_image)


class NavigationButton(Button):
    def __init__(self, parent, controller, frame, text, column):
        super().__init__(text=text)
        button = Button(parent, text=text, bg=colors[0], width=30, border=0
                        , command=lambda: controller.show_frame(frame),
                        )
        button.rowconfigure(0, weight=1)
        button.columnconfigure(0, weight=1)
        button.grid(row=0, column=column, sticky="WENS")


class NavigationBar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        navigation_bar = Frame(parent, bg=colors[0])
        navigation_bar.rowconfigure(0, weight=1)
        navigation_bar.columnconfigure(0, weight=1)
        navigation_bar.grid(row=0, column=0, sticky="NESE")
        # adding buttons to the navigation bar
        NavigationButton(navigation_bar, controller, CollaborativePage, "Collaborative", 0)
        NavigationButton(navigation_bar, controller, ContentPage, "Content", 1)


class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        # MAIN
        main = Frame(parent)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.pack(expand=1, fill=BOTH)

        # TOP - contains the navigation bar
        top = Frame(main, height=50, bg=colors[0])
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.grid(row=0, column=0, sticky='WENS')
        top.grid_propagate(False)
        # adding a navigation bar to the top frame
        NavigationBar(top, self)

        # BOTTOM CONTENT - contains the pages
        content = Frame(main)
        content.grid(row=1, column=0, sticky='WENS')
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        # save all pages in a list
        self.frames = {}
        for F in (CollaborativePage, ContentPage):
            frame = F(content)
            self.frames[F] = frame

        # first page to show on content frame
        self.show_frame(CollaborativePage)

    def show_frame(self, f):
        # gets the specific frame from the list of frames
        frame = self.frames[f]
        frame.grid(row=0, column=0)
        # raise frame to be first on top, so it will be visible on window
        frame.tkraise()


class NothingRegisteredFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        label = Label(self, text="Nothing is registered.", fg=colors[0], bg=colors[2])
        label.pack(fill=BOTH, expand=True)


class CollaborativePage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        LeftContent(self, "Collaborative Filtering",
                    "We will recommend some movies by one movie you like", CollaborativeFilter)
        self.right_content = RightContent(self)

    def reload_right_content(self, recommendations):
        if len(recommendations) != 0:
            scroll_frame = ScrollableFrame(self.right_content, RecommendationList, recommendations)
            self.right_content.show_frame(scroll_frame)
        else:
            nothing_registered_frame = NothingRegisteredFrame(self.right_content)
            self.right_content.show_frame(nothing_registered_frame)


class CollaborativeFilter(Frame):
    all_movies = prepare.get_all_movie_titles()
    recommendations = []

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, padx=15, pady=20, bg=colors[4])
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky="WENS")

        option_title = Label(self, text="Choose a movie you like:", font="Arial 10 bold", bg=colors[4], fg=colors[0])
        option_title.grid(row=0, column=0, sticky="NWSW")

        self.movie_options = Combobox(self, state="readonly", values=self.all_movies)
        self.movie_options.set("Movies")
        self.movie_options.grid(row=1, column=0, sticky="WENS")

        frame = Frame(self, height=15, bg=colors[4])
        frame.rowconfigure(0, weight=1)
        frame.grid(row=2, column=0, sticky="WENS")

        button = Button(self, text="RUN", border=0, bg=colors[6], fg=colors[5],
                        command=lambda: self.runCollaborativeFilter()
                        )
        button.grid(row=3, column=0, sticky="WENS")

    def runCollaborativeFilter(self):
        # TODO: get the real index for movie
        movie = self.movie_options.get()
        index = prepare.get_movie_index_by_title(movie)
        self.recommendations = cr.recommend_movies(index, 6)
        self.controller.reload_right_content(self.recommendations)


class ContentPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="blue")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=375)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky="WENS")
        # left_content = LeftContent(self, "Content Filtering",
        #                            "We will recommend some movies by your filtering choices")
        # CollaborativeFilter(left_content)
        # RightContent(self)


class LeftContent(Frame):
    def __init__(self, parent, title, description, filter_frame):
        Frame.__init__(self, parent, width=375, bg=colors[4])
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="WENS")

        # TOP - showing the title and small description
        page_title_container = PageTitleContainer(self, title, description)
        page_title_container.grid(row=0, column=0, sticky="WENS")

        # FILTER - show either CollaborativeFilter or ContentFilter
        filter_frame(self, parent)


class RightContent(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=colors[2], highlightthickness=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=1, sticky="WENS")
        # The default frame to view the first time the content are shown
        self.frame = NothingRegisteredFrame(self)

    def show_frame(self, new_frame):
        self.frame.pack_forget()
        self.frame = new_frame
        self.frame.tkraise()


class PageTitleContainer(Frame):
    def __init__(self, parent, title, description):
        Frame.__init__(self, parent)
        self.configure(bg=colors[3], height=120, pady=25, padx=15)
        title_ = Label(self, text=title, font="Arial 16 bold", bg=colors[3], fg=colors[0])
        title_.grid(row=0, column=0, sticky="NWSW")
        description_ = Label(self, text=description, font="Arial 9 normal", bg=colors[3], fg=colors[0])
        description_.grid(row=1, column=0, sticky="NWSW")


class MovieDetails(Frame):
    def __init__(self, parent, movie_title):
        Frame.__init__(self, parent, bg=colors[2], highlightthickness=0, pady=25)
        self.pack(fill=BOTH, expand=True, padx=(25, 40))

        # Find movie information by movie title
        imdb_id = prepare.get_imdb_id_by_title(movie_title)
        poster_url = ws.get_poster(imdb_id)
        short_summary_text = ws.get_summaries(imdb_id)[0].text
        self.summary_text = self.get_summary(imdb_id)
        self.trailer_text = ws.get_trailer(imdb_id)

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

        # TODO: select the genres plus rating ..
        # MOVIE POSTER
        poster_url = urllib.request.urlopen(poster_url).read()
        img = Image.open(io.BytesIO(poster_url))
        image = ImageTk.PhotoImage(img)
        label1 = Label(left, image=image, bg=colors[0], width=180, highlightthickness=0, border=0)
        label1.image = image
        label1.grid(row=0, column=0, sticky="WENS")

        # TITLE
        title = Label(right, text=movie_title, font="Arial 20 bold", fg=colors[5], bg=colors[0])
        title.grid(row=0, column=0, sticky="NWSW")

        # GENRES
        genres = Label(right, text="Action, Fantasy, Sci-fi", bg=colors[0], fg=colors[2])
        genres.grid(row=1, column=0, sticky="NWSW")

        # RATING
        rating = Frame(right, pady=10, bg=colors[0])
        rating.columnconfigure(0, weight=1)
        rating.grid(row=2, column=0, sticky="WENS")
        rating_label = Label(rating, text="Rating:", font="Arial 10 bold", bg=colors[0])
        rating_label.grid(row=0, column=0, sticky="NWSW")
        rating_description = Label(rating, text="8.7", bg=colors[0])
        rating_description.grid(row=1, column=0, sticky="NWSW")

        # SHORT SUMMARY
        short_summary = Frame(right, pady=10, bg=colors[0])
        short_summary.columnconfigure(0, weight=1)
        short_summary.grid(row=3, column=0, sticky="WENS")
        short_summary_label = Label(short_summary, text="Short summary:", font="Arial 10 bold", bg=colors[0])
        short_summary_label.grid(row=0, column=0, sticky="NWSW")
        short_summary_description = Label(short_summary, text=short_summary_text,
                                          bg=colors[0], wraplength=800, justify="left")
        short_summary_description.grid(row=1, column=0, sticky="NWSW")

        # SUMMARY
        summary = Frame(right, pady=10, bg=colors[0])
        summary.columnconfigure(0, weight=1)
        summary.grid(row=4, column=0, sticky="WENS")
        summary_label = Label(summary, text="Summary:", font="Arial 10 bold", bg=colors[0])
        summary_label.grid(row=0, column=0, sticky="NWSW")
        summary_describtion = Label(summary,
                                    wraplength=800,
                                    text=self.summary_text,
                                    justify="left",
                                    bg=colors[0])
        summary_describtion.grid(row=1, column=0, sticky="NWSW")

        # TRAILER LINK
        self.trailer = Frame(right, pady=10, bg=colors[0])
        self.trailer.columnconfigure(0, weight=1)
        self.trailer.grid(row=5, column=0, sticky="WENS")
        self.trailer_label = Label(self.trailer, text="Trailer:", font="Arial 10 bold", bg=colors[0])
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


class RecommendationList(Frame):
    def __init__(self, parent, recommendations):
        Frame.__init__(self, parent, highlightthickness=0, bg=colors[2])
        for i in recommendations:
            movie_details = MovieDetails(self, i)
            movie_details.pack(fill=BOTH, expand=True)


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
