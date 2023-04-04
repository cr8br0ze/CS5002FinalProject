import customtkinter as tk
import evaluation
import validation

#run prediction of text given
def runEvaluation(text):
    return evaluation.evaluation().evaluate(text)

#run validation on the classifier
def runValidation():
    return validation.validation().validate()

#prediction window
def evaluationWindow():
    #theme
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("dark-blue")

    # create the window
    window = tk.CTk()
    window.title("Evaluation")
    window.geometry("600x400")

    #create a label
    label = tk.CTkLabel(master=window,
                        text="Please enter the text for evaluation",
                        width=100,
                        height=30,
                        corner_radius=7)
    label.place(x=170, y=50)

    #make a textbox
    textbox = tk.CTkEntry(window, width=500, height=500)
    textbox.pack(pady=110, padx=50)

    #click on button
    def click():
        text = textbox.get()
        eva = runEvaluation(text)
        label = tk.CTkLabel(master=window,
                            text= eva)
        label.place(x=270, y=300)

    #make a button
    button = tk.CTkButton(window, text = "Run",
                          command = click)
    button.place(x=230, y=335)

#main window
def main():
    #theme
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("dark-blue")

    #create the window
    window = tk.CTk()
    window.title("Niave Bayes Text Spam Classifier")
    window.geometry("600x400")

    #click on the validation button
    def click():
        text = runValidation()
        label = tk.CTkLabel(master=window,
                            text= text)
        label.place(x=190, y=50)

    #buttons
    button = tk.CTkButton(window, text = "Run Validation",
                          command = click)
    button.place(x=230, y=165)
    button2 = tk.CTkButton(window, text = "Run Evaluation",
                           command = evaluationWindow)
    button2.place(x=230, y=205)

    window.mainloop()

if __name__ == '__main__':
    main()
