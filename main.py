import customtkinter
from customtkinter.windows.ctk_tk import tkinter
import requests
import webbrowser

class AboutFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure((1), weight=1)

        self.label = customtkinter.CTkLabel(self, text="Source Code", text_color="#198ab4",cursor="hand2")
        self.label.grid(row=0, column=0, padx=20)
        self.label.bind("<Button-1>", lambda e:self.open_url("https://github.com/harshshah6/Github-Repo-Size-Calculator"))

        self.labe2 = customtkinter.CTkLabel(self, text="Made by LEGENDARY STREAMER", justify=tkinter.RIGHT)
        self.labe2.grid(row=0, column=1, padx=(0,20), sticky="e")
    
    def open_url(self,url):
        webbrowser.open_new_tab(url)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("400x150")
        self.grid_columnconfigure((0, 1), weight=1)

        self.inputtext = customtkinter.CTkEntry(self,width=400,height=30,placeholder_text="Github Repo Url Here")
        self.inputtext.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.button = customtkinter.CTkButton(self, text="GET REPO SIZE", command=self.button_callback)
        self.button.grid(row=0, column=1, padx=(0,20), pady=20, sticky="ew", columnspan=2)

        self.frame_output = customtkinter.CTkFrame(self)
        self.frame_output.grid(row=1, column=0, padx=(20,20), pady=(0,20), sticky="nsew", columnspan=2)
        
        self.textview = customtkinter.CTkLabel(self.frame_output, text="...", justify=tkinter.LEFT)
        self.textview.grid(row=0, column=0, padx=20, pady=(20,20), sticky="w")

        self.aboutframe = AboutFrame(self)
        self.aboutframe.grid(row=2, columnspan=2, padx=(20,20), pady=(0,20), sticky="nsew")
        
    def button_callback(self):
        giturl = self.inputtext.get().replace("https://github.com/","")
        self.inputtext.delete(0,last_index=len(self.inputtext.get()))
        print(giturl)
        if(giturl == ''):
            return
        try:
            size = (requests.get(f"https://api.github.com/repos/{giturl}").json().get('size'))

            def getSize(size_in_kb):
                kb = 1024
                mb = kb * 1024
                gb = mb * 1024
                tb = gb * 1024
                if size_in_kb < kb:
                    return size_in_kb, "KB"
                elif size_in_kb < mb:
                    return size_in_kb / 1024, "MB"
                elif size_in_kb < gb:
                    return size_in_kb / (1024 * 1024), "GB"
                elif size_in_kb < tb:
                    return size_in_kb / (1024 * 1024 * 1024), "TB"
                else:
                    return size_in_kb / (1024 * 1024 * 1024 * 1024), "PB"
                
            converted_size, unit = getSize(size)
            print(f"{converted_size:.2f} {unit}")
            self.textview.configure(True,text=f"https://github.com/{giturl}\n\nSize = {converted_size:.2f} {unit}\n\nSize In KB = {size}")
        except Exception as e:
            self.textview.configure(True,text=repr(e))
        

app = App()
app.wm_title("Github Repo Size Calculator")
app.mainloop()