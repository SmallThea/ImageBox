from app import ImageBoxApp

if __name__ == "__main__":
    app = ImageBoxApp()
    app.iconbitmap(default='src/icon.ico')
    app.title("ImageBox")
    app.geometry("800x600")
    app.resizable(width=False, height=False)
    app.mainloop()