import customtkinter as tk
import evaluation
import testing

#run prediction of text given
def runEvaluation(text):
    return evaluation.evaluation().evaluate(text)

#run testing on the classifier
def runTesting():
    return testing.testing().test()

#main window
def main():
    #theme
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("dark-blue")

    #create the window
    window = tk.CTk()
    window.title("Niave Bayes Text Spam Classifier")
    window.geometry("600x400")

    #click on the testing button
    def click():
        text = runTesting()
        label = tk.CTkLabel(master=window,
                            text= text)
        label.place(x=190, y=50)

    #buttons
    button = tk.CTkButton(window, text = "Run Testing",
                          command = click)
    button.place(x=230, y=165)

    # prediction window
    def evaluationWindow():
        # theme
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")

        # create the window
        windoww = tk.CTkToplevel(window)
        windoww.title("Evaluation")
        windoww.geometry("600x400")

        # create a label
        label2 = tk.CTkLabel(master=windoww,
                            text="Please enter the text for evaluation",
                            width=100,
                            height=30,
                            corner_radius=7)
        label2.place(x=170, y=50)

        # make a textbox
        textbox = tk.CTkEntry(windoww, width=500, height=500)
        textbox.pack(pady=110, padx=50)
        label3 = tk.CTkLabel(master=windoww,
                            text="")
        label3.place(x=270, y=300)

        # click on button
        def click():
            text = textbox.get()
            eva = runEvaluation(text)
            label3.configure(text=eva)

        # make a button
        button3 = tk.CTkButton(windoww, text="Run",
                              command=click)
        button3.place(x=230, y=335)

    button2 = tk.CTkButton(window, text = "Run Evaluation",
                           command = evaluationWindow)
    button2.place(x=230, y=205)

    window.mainloop()

if __name__ == '__main__':
    main()
