import evaluation as eval
from tqdm import tqdm

class testing:
    def __init__(self):
        self.evaluation = eval.evaluation()

    #testing
    def test(self):
        valSet = self.evaluation.classifier.testingSet.to_dict(orient="records")
        total = len(valSet)
        T = 0
        F = 0
        for i in tqdm(valSet):
            if i["type"].lower() == "ham":
                type = "not spam"
            else:
                type = "spam"
            if self.evaluation.evaluate(i["text"]) == type:
                T += 1
            else:
                F += 1
        accuracy = T/total*100
        failing = F/total*100
        return f"accuracy = {accuracy}%\nfailing rate = {failing}%"
