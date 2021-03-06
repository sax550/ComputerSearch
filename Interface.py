from PIL import Image, ImageTk
import Tkinter
import urllib
import random
import os
import webbrowser
from Searchprocess import search


class searchscreen():

    def __init__(self):
        self.listings = ""
        self.listingposition = 0


    def Initialize_Searchprocess(self, myprice, reviews, mybrand):

        # Determines whether user chose a laptop or a desktop in earlier page in order to pass the correct links
        # Had to program it like this because of a problem with tkinter not letting me return values
        if Interface1.laptopordesktop == "laptop":
            links_tosearch = ["https://www.hsn.com/shop/laptops/ec0033",
                              "http://www.microcenter.com/category/4294967288/Laptops-Notebooks",
                              "http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=17"]

        elif Interface1.laptopordesktop == "desktop":
            links_tosearch = ["https://www.hsn.com/shop/desktop-computers/ec0031?akamai-feo=off",
                              "http://www.microcenter.com/category/4294967292/All-Desktops",
                              "http://www.tigerdirect.com/applications/category/category_tlc.asp?CatId=6"]

        # Starts the data-collection process through all the websites in the Searchprocess file.
        search1 = search(myprice, reviews, mybrand, links_tosearch)
        search1.hsn()
        search1.microcenter()
        search1.tigerdirect()
        # Starts the process to store all the data together in a dictionary
        self.listings = search1.compare()


    def results_screen(self):

        self.searchscreen_root = Tkinter.Toplevel()
        self.searchscreen_root.geometry("600x300")
        self.searchscreen_root.title("searchresults")

        self.searchtitle = Tkinter.Label(self.searchscreen_root, text="Search Results", bg="white", font="fixedsys")
        self.searchtitle.pack(fill=Tkinter.X)

        # Displays a page indicating there are no results if there are no suitable listings
        if len(self.listings) == 0:
            Noresultstext = Tkinter.Label(self.searchscreen_root,text = "Sorry, there are no results available.",
                                          fg = "darkgrey",font = "fixedsys" )
            Noresultstext.pack()
            Noresultstext.place(x = 140, y = 170)

            Noresultsphotold = ImageTk.PhotoImage(Image.open(r"programphotos\sad.jpg"))
            Noresultsphoto = Tkinter.Label(self.searchscreen_root, image = Noresultsphotold)
            Noresultsphoto.Image = Noresultsphotold
            Noresultsphoto.pack()
            Noresultsphoto.place(x = 260, y = 90)

        else:
            def openlink():
                # link to listings
                webbrowser.open_new(self.listings.values()[self.listingposition][2])


            linkbutton = Tkinter.Button(self.searchscreen_root,
                                    text=self.listings.values()[0][2],
                                    fg="darkgrey", bd=0, command=openlink)
            linkbutton.pack(side = Tkinter.BOTTOM)


            def fontsize():
                titlelength = len(self.listings.keys()[self.listingposition].split())

                if titlelength < 10:
                    return 12
                elif titlelength < 20:
                    return 10
                else:
                    return 8

            result_title = Tkinter.Label(self.searchscreen_root, text=self.listings.keys()[0],
                                    fg="darkgrey", font=("arial", fontsize()))

            result_title.pack()

            urllib.urlretrieve(self.listings.values()[0][1], "firstphoto" + ".jpg")

            # Loads and displays the first image and title then deletes the image so its not saved on the hard drive
            PILfirstphotold = Image.open("firstphoto" + ".jpg")
            # Configures the size of the image
            PILfirstphotoconfig = PILfirstphotold.resize((240, 170), Image.ANTIALIAS)
            firstphotoLd = ImageTk.PhotoImage(PILfirstphotoconfig)

            photo = Tkinter.Label(self.searchscreen_root, image=firstphotoLd, bg="darkgrey", bd=2)
            photo.image = firstphotoLd


            photo.pack()
            photo.place(x=80, y=75)
            # Removes the photo from laptopfinder file.
            os.remove("firstphoto" + ".jpg")


            def starrating():

                if int(self.listings.values()[self.listingposition][3]) != 0:
                    starlength = "programphotos" + "/" + str(self.listings.values()[self.listingposition][3]) + "star.png"

                else:
                    starlength = "programphotos/0star.png"

                return starlength

            starget = starrating()
            starimgLd = ImageTk.PhotoImage(Image.open(starget))

            starimg = Tkinter.Label(self.searchscreen_root, image = starimgLd, bg = "darkgrey",  bd = 2)
            starimg.pack()
            starimg.place(x = 350, y = 90)


            def seereviews_visible():
                # Asks if the star rating isnt 0
                if int(self.listings.values()[self.listingposition][3]) != 0:
                    seereviews_text = "(See Reviews)"

                else:
                    seereviews_text = ""

                return seereviews_text


            def seereviews_link():
                webbrowser.open_new(self.listings.values()[self.listingposition][2])


            seereviews = Tkinter.Button(self.searchscreen_root, font = "fixedsys", bd = 0,
                                       fg = "darkgrey", text = seereviews_visible(),
                                        command = seereviews_link)
            seereviews.pack()
            seereviews.place(x = 373, y = 147)


            # Loads and displays the listing position
            position = Tkinter.Label(self.searchscreen_root, text = "0/" + str(len(self.listings.keys()) - 1),
                                 fg = "darkgrey", font = "fixedsys")
            position.pack()
            position.place(x = 290, y = 260)

            # Loads and displays the price
            pricelabel = Tkinter.Label(self.searchscreen_root, text = "Price: " + "$" +
                                        str(self.listings.values()[0][0]),
                                        font = ("fixedsys", 15), fg = "darkgrey")

            pricelabel.pack()
            pricelabel.place(x = 370, y = 200)


            def getphoto():
                try:
                    randomphotoname = str(random.randint(1, 1000000))
                    # Downloads the image file from techbargain.com
                    photolink = self.listings.values()[self.listingposition][1]
                    urllib.urlretrieve(photolink, randomphotoname + ".jpg")
                    # Loads and displays the image
                    PILphotold = Image.open(randomphotoname + ".jpg")
                                         # Changes img size to a default
                    PILphotold_config = PILphotold.resize((240, 170), Image.ANTIALIAS)
                    listingphoto = ImageTk.PhotoImage(PILphotold_config)

                    photo.config(image=listingphoto)
                    photo.image = listingphoto
                    photo.pack()
                    photo.place(x=80, y=75)
                    # Removes the photo from laptopfinder file.
                    os.remove(randomphotoname + ".jpg")

                except:
                    print "download error"


            def morelistings():
                self.listingposition += 1
                # If scrolled to the end of the listings switch back to the first listing
                if self.listingposition > len(self.listings.keys()) - 1:
                    self.listingposition = 0

                print self.listingposition
                # Changes photo forward
                getphoto()
                # Change listings title forward
                result_title.config(text=self.listings.keys()[self.listingposition], font = ("arial", fontsize()))
                # Change listing number label forward
                position.config(text = str(self.listingposition) + "/" + str(len(self.listings.keys()) - 1))
                #   Change listing link forward
                linkbutton.config(text=str(self.listings.values()[self.listingposition][2]))

                # Change price label forward
                pricelabel.config(text="Price: " + "$" +
                                   str(self.listings.values()[self.listingposition][0]))

                starimgLd_config = ImageTk.PhotoImage(Image.open(starrating()))
                starimg.config(image=starimgLd_config)
                starimg.image = starimgLd_config
                # Configures the See Reviews link to be visible or invisible
                seereviews.config(text = seereviews_visible())

            def lesslistings():
                self.listingposition -= 1
                # If scrolled to the start of the listings switch back to the last listing
                if self.listingposition < 0:
                    self.listingposition = len(self.listings.keys()) - 1
                # Changes photo backward
                getphoto()
                # Change listings title backward
                result_title.config(text=self.listings.keys()[self.listingposition], font = ("arial", fontsize()))
                # Change listing number label backward
                position.config(text=str(self.listingposition) + "/" + str(len(self.listings.keys()) - 1))
                # Change listing link backward
                linkbutton.config(text=str(self.listings.values()[self.listingposition][2]))

                starimgLd_config = ImageTk.PhotoImage(Image.open(starrating()))
                starimg.config(image=starimgLd_config)
                starimg.image = starimgLd_config
                # Change price label backward
                pricelabel.config(text="Price: " + "$" +
                                   str(self.listings.values()[self.listingposition][0]))
                # Configures the See Reviews link to be visible or invisible
                seereviews.config(text=seereviews_visible())


            # Loads and displays the left and right arrows
            moreresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\rightarrow.png"))
            moreresultsarrow = Tkinter.Button(self.searchscreen_root, image=moreresultsimgld, bd=0, command=morelistings)
            moreresultsarrow.pack()
            moreresultsarrow.place(x=560, y=130)

            lessresultsimgld = ImageTk.PhotoImage(Image.open(r"programphotos\leftarrow.png"))
            lessresultsarrow = Tkinter.Button(self.searchscreen_root, image=lessresultsimgld, bd=0, command=lesslistings)
            lessresultsarrow.pack()
            lessresultsarrow.place(x=0, y=130)

            self.searchscreen_root.mainloop()


class parameterscreen():

    def __init__(self, txt):
        # If i use Tkinter.Tk() for the parameter screen root the images dont work?
        self.p_root = Tkinter.Toplevel()
        self.p_root.title("Pc finder")
        self.p_root.geometry("540x300")

        self.budget1 = 0
        self.goodreviews_onoroff = False

        self.brandchoices = []
        #loads and displays the parameterscreen title
        paramlabel = Tkinter.Label(self.p_root, font="fixedsys", text=txt, bg="white")
        paramlabel.pack(fill = Tkinter.BOTH)


    # Function for the parameter screen budget scale
    def range(self):
        self.pricerange = Tkinter.Scale(self.p_root, from_=0, to=2000, label="Budget", fg="darkgrey",
                                        orient=Tkinter.VERTICAL, length=250,                   #used root background
                                        sliderlength=14, bd=1, font="fixedsys", troughcolor = self.p_root.cget("bg"),
                                        )

        self.pricerange.pack()
        self.pricerange.place(x=5, y=32)

    
    def choosecomputerbrand(self):

        def hpimgchg():
            # Changes button to a different image to let user know brand is selected.

            # Is  there a better solution for changing the images when I click on the button?
            # I would make this into a function so i dont have to add an extra 75 lines but
            # tkinters command doesnt let me pass.

            if self.hpbrand.image == self.hpimg:
                hpselected = ImageTk.PhotoImage(Image.open(r"programphotos\hphover.jpg"))
                self.hpbrand.config(image=hpselected)
                self.hpbrand.image = hpselected
                # Adds keywords to brand choices
                self.brandchoices.extend(("hp", "Hp", "HP"))

            elif self.hpbrand.image != self.hpimg:
                self.hpbrand.config(image=self.hpimg)
                self.hpbrand.image = self.hpimg

                for hpremove in ["hp", "Hp", "HP"]:  # I guess just using 3 .removes would be easier to read but
                    self.brandchoices.remove(hpremove)  # I gotta save that 1 line of code :)

            print self.brandchoices

        # Read this before hpimgchg
        self.hpimg = ImageTk.PhotoImage(Image.open(r"programphotos\hp.jpg"))
        self.hpbrand = Tkinter.Button(self.p_root, image=self.hpimg, bd=0, command=hpimgchg)
        self.hpbrand.image = self.hpimg
        self.hpbrand.pack()
        self.hpbrand.place(x=140, y=80)

        # Same as above. Repeats 4 more times
        def dellimgchg():
            if self.dellbrand.image == self.dellimg:
                dellselected = ImageTk.PhotoImage(Image.open(r"programphotos\dellselected.png"))
                self.dellbrand.config(image=dellselected)
                self.dellbrand.image = dellselected

                self.brandchoices.extend(("dell", "Dell", "DELL"))


            elif self.dellbrand.image != self.dellimg:
                self.dellbrand.config(image=self.dellimg)
                self.dellbrand.image = self.dellimg

                for hpremove in ["dell", "Dell", "DELL"]:
                    self.brandchoices.remove(hpremove)

        self.dellimg = ImageTk.PhotoImage(Image.open(r"programphotos\dell.png"))
        self.dellbrand = Tkinter.Button(self.p_root, image=self.dellimg, bd=0, command=dellimgchg)
        self.dellbrand.image = self.dellimg
        self.dellbrand.pack()
        self.dellbrand.place(x=210, y=80)

        def appleimgchg():
            if self.applebrand.image == self.appleimg:
                appleselected = ImageTk.PhotoImage(Image.open(r"programphotos\appleselected.png"))
                self.applebrand.config(image=appleselected)
                self.applebrand.image = appleselected

                self.brandchoices.extend(("apple", "Apple", "APPLE"))

            elif self.applebrand.image != self.appleimg:
                self.applebrand.config(image=self.appleimg)
                self.applebrand.image = self.appleimg

                for hpremove in ["apple", "Apple", "APPLE"]:
                    self.brandchoices.remove(hpremove)

        self.appleimg = ImageTk.PhotoImage(Image.open(r"programphotos\apple.png"))
        self.applebrand = Tkinter.Button(self.p_root, image=self.appleimg, bd=0, command=appleimgchg)
        self.applebrand.image = self.appleimg
        self.applebrand.pack()
        self.applebrand.place(x=280, y=80)

        def microsoftimgchg():
            if self.microsoftbrand.image == self.microsoftimg:
                microsoftselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\microsoftselected.png"))
                self.microsoftbrand.config(image=microsoftselected)
                self.microsoftbrand.image = microsoftselected

                self.brandchoices.extend(("microsoft", "Microsoft", "MICROSOFT"))

            elif self.microsoftbrand.image != self.microsoftimg:
                self.microsoftbrand.config(image=self.microsoftimg)
                self.microsoftbrand.image = self.microsoftimg

                for hpremove in ["microsoft", "Microsoft", "MICROSOFT"]:
                    self.brandchoices.remove(hpremove)

        self.microsoftimg = ImageTk.PhotoImage(
            Image.open(r"programphotos\microsoft.png"))
        self.microsoftbrand = Tkinter.Button(self.p_root, image=self.microsoftimg, bd=0, command=microsoftimgchg)
        self.microsoftbrand.image = self.microsoftimg
        self.microsoftbrand.pack()
        self.microsoftbrand.place(x=350, y=80)

        def lenovoimgchg():
            if self.lenovobrand.image == self.lenovoimg:
                lenovoselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\lenovoselected.png"))
                self.lenovobrand.config(image=lenovoselected)
                self.lenovobrand.image = lenovoselected

                self.brandchoices.extend(("lenovo", "Lenovo", "LENOVO"))

            elif self.lenovobrand.image != self.lenovoimg:
                self.lenovobrand.config(image=self.lenovoimg)
                self.lenovobrand.image = self.lenovoimg

                for hpremove in ["lenovo", "Lenovo", "LENOVO"]:
                    self.brandchoices.remove(hpremove)

        self.lenovoimg = ImageTk.PhotoImage(Image.open(r"programphotos\lenovo.png"))
        self.lenovobrand = Tkinter.Button(self.p_root, image=self.lenovoimg, bd=0, command=lenovoimgchg)
        self.lenovobrand.image = self.lenovoimg
        self.lenovobrand.pack()
        self.lenovobrand.place(x=140, y=150)

        def acerimgchg():
            if self.acerbrand.image == self.acerimg:
                acerselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\acerselected.jpg"))
                self.acerbrand.config(image=acerselected)
                self.acerbrand.image = acerselected

                self.brandchoices.extend(("acer", "Acer", "ACER"))

            elif self.acerbrand.image != self.acerimg:
                self.acerbrand.config(image=self.acerimg)
                self.acerbrand.image = self.acerimg

                for hpremove in ["acer", "Acer", "ACER"]:
                    self.brandchoices.remove(hpremove)

        self.acerimg = ImageTk.PhotoImage(Image.open(r"programphotos\acer.jpg"))
        self.acerbrand = Tkinter.Button(self.p_root, image=self.acerimg, bd=0, command=acerimgchg)
        self.acerbrand.image = self.acerimg
        self.acerbrand.pack()
        self.acerbrand.place(x=210, y=150)

        def razerimgchg():
            if self.razerbrand.image == self.razerimg:
                razerselected = ImageTk.PhotoImage(
                    Image.open(r"programphotos\razerselected.jpg"))
                self.razerbrand.config(image=razerselected)
                self.razerbrand.image = razerselected

                self.brandchoices.extend(("razer", "Razer", "RAZER"))

            elif self.razerbrand.image != self.razerimg:
                self.razerbrand.config(image=self.razerimg)
                self.razerbrand.image = self.razerimg

                for hpremove in ["razer", "Razer", "RAZER"]:
                    self.brandchoices.remove(hpremove)

        self.razerimg = ImageTk.PhotoImage(Image.open(r"programphotos\razer.png"))
        self.razerbrand = Tkinter.Button(self.p_root, image=self.razerimg, bd=0, command=razerimgchg)
        self.razerbrand.image = self.razerimg
        self.razerbrand.pack()
        self.razerbrand.place(x=280, y=150)

        def msiimgchg():
            if self.msibrand.image == self.msiimg:
                self.msiselected = ImageTk.PhotoImage(Image.open(r"programphotos\msiselected.jpg"))
                self.msibrand.config(image=self.msiselected)
                self.msibrand.image = self.msiselected

                self.brandchoices.extend(("msi", "Msi", "MSI"))

            elif self.msibrand.image != self.msiimg:
                self.msibrand.config(image=self.msiimg)
                self.msibrand.image = self.msiimg

                for hpremove in ["msi", "Msi", "MSI"]:
                    self.brandchoices.remove(hpremove)

        self.msiimg = ImageTk.PhotoImage(Image.open(r"programphotos\msi.png"))
        self.msibrand = Tkinter.Button(self.p_root, image=self.msiimg, bd=0, command=msiimgchg)
        self.msibrand.image = self.msiimg
        self.msibrand.pack()
        self.msibrand.place(x=350, y=150)

    def goodreviews(self):

        def switch():
            if self.goodreviews_onoroff == False:
                self.goodreviews_onoroff = True

            else:
                self.goodreviews_onoroff = False

            print self.goodreviews_onoroff


        goodreview_switch = Tkinter.Checkbutton(self.p_root, text = "Only show listings with good reviews.",
                                                font = "fixedsys", fg = "darkgrey", command = switch)
        goodreview_switch.pack()
        goodreview_switch.place(x = 110, y = 260)


    def findbutton(self):

        def buttoncommand():

            self.searchtrigger = searchscreen()
            self.searchtrigger.Initialize_Searchprocess(self.pricerange.get(), self.goodreviews_onoroff, self.brandchoices)
            self.searchtrigger.results_screen()

        # Button that triggers the search class in the search file
        searchbutton = Tkinter.Button(self.p_root, text="FIND", font="fixedsys", fg="darkgrey",
                                      width=8, command=buttoncommand)

        searchbutton.pack()
        searchbutton.place(x=450, y=260)

    def paramterwidgets(self):
        #starts all parameter screen widgets
        self.choosecomputerbrand()
        self.range()
        self.goodreviews()
        self.findbutton()


class screen():
    def __init__(self):
        print "tacos"
        self.laptopordesktop = ""

    # Startup screen and its widgets
    def startscreen(self):
        self.root = Tkinter.Tk()
        self.root.title("Pc finder")
        self.root.geometry("440x200")

        #loads and displays the title for the startup screen
        startscreen_title = Tkinter.Label(self.root, font="fixedsys", text="What kind of computer would you like to find?",
                               width=40, bg="white")
        startscreen_title.pack(side=Tkinter.TOP, fill=Tkinter.X)

        #loads and displats the desktop image
        self.dtImageLd = ImageTk.PhotoImage(Image.open(r"programphotos\desktop.png"))
        dtImage = Tkinter.Label(self.root, image=self.dtImageLd)
        dtImage.pack(side=Tkinter.LEFT)
        dtImage.place(x=45, y=45)

        #loads and displays the laptop image
        self.ltImageLd = ImageTk.PhotoImage(Image.open(r"programphotos\laptop.png"))
        ltImage = Tkinter.Label(self.root, image=self.ltImageLd)
        ltImage.pack(side=Tkinter.RIGHT)
        ltImage.place(x=275, y=40)

        def Dtchangescreen():
            # Starts parameter screen(desktop version).
            self.laptopordesktop = "desktop"
            parameterscreen1 = parameterscreen("What kind of desktop would you like to find?")
            parameterscreen1.paramterwidgets()

        # Buttons
        b1 = Tkinter.Button(self.root, font="fixedsys", text="Desktops",
                            bg=self.root.cget("bg"), command=Dtchangescreen
                            )   #gets default background
        b1.pack()
        b1.place(x=65, y=160)

        def Ltchangescreen():
            # Starts parameter screen(laptop version)
            self.laptopordesktop = "laptop"
            parameterscreen1 = parameterscreen("What kind of laptop would you like to find?")
            parameterscreen1.paramterwidgets()

        b2 = Tkinter.Button(self.root, font="fixedsys", text="Laptops",
                            bg=self.root.cget("bg"), command=Ltchangescreen
                            )

        b2.pack()
        b2.place(x=305, y=160)

        #

# Starts the startup screen

Interface1 = screen()

def main():
    #starts the first GUI screen
    Interface1.startscreen()
    Interface1.root.mainloop()

if __name__ == "__main__":
    main()
