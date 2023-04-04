import string
import Classifier as model

class evaluation:
    def __init__(self):
        self.classifier = model.Classifier("SMSSpamCollection")

    #prediction on the text given
    def evaluate(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation)).split()
        pSpam = self.classifier.pSpam()
        pTextSpam = self.classifier.pTextSpam(text)
        pNotSpam = self.classifier.pNotSpam()
        pTextNotSpam = self.classifier.pTextNotSpam(text)
        pSpamText = pSpam * pTextSpam
        pNotSpamText = pNotSpam * pTextNotSpam
        if pSpamText > pNotSpamText:
            return "spam"
        else:
            return "not spam"
