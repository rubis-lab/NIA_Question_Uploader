from json.tool import main
import requests
import json
import pandas as pd

endpoint = 'https://api.niaapi.com/'
# 3a07741ac1e20827c6da27e0299b0aabd9c86b48
# print result 
def print_result(response):
    parsed = json.loads(response.content)
    print(json.dumps(parsed, indent=4))

# post_question
def post_question(authorId,subject,topic,difficulty):           
    fill_info = {
        "authorId": authorId,
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty 
    }
    response = requests.post(f'{endpoint}nia/question', json=fill_info) 
    data = response.json()
    questionID = data['questionId']
    return questionID

# post_baseQuestion
def post_baseQuestion(questionID, stage ,subQuestionURL):           
    fill_info = {
        "questionId": questionID,
        "stage": stage,
        "contentUrl": subQuestionURL,
        "guidelineUrl": "https://nia.com/guideline/XXXX-XXXX"
        }
    response = requests.post(f'{endpoint}nia/subquestion', params={'subquestionType': 'SHORT_ANSWER'},json=fill_info) 
    data = response.json()
    #print(data)

# post_comprehensionQuestion
def post_comprehensionQuestion(questionID, stage ,subQuestionURL):           
    fill_info = {
        "questionId": questionID,
        "stage": stage,
        "contentUrl": subQuestionURL,
        "guidelineUrl": "https://nia.com/guideline/XXXX-XXXX"
        }
    response = requests.post(f'{endpoint}nia/subquestion', params={'subquestionType': 'SHORT_ANSWER'},json=fill_info) 
    data = response.json()
    #print(data)

# post_emotionQuestion
def post_emotionQuestion(questionID, stage ,subQuestionURL):           
    fill_info = {
        "questionId": questionID,
        "stage": stage,
        "contentUrl": subQuestionURL,
        "guidelineUrl": "https://nia.com/guideline/XXXX-XXXX"
        }
    response = requests.post(f'{endpoint}nia/subquestion', params={'subquestionType': 'SHORT_ANSWER'},json=fill_info) 
    data = response.json()
    #print(data)

def getAttribute():
    df = pd.read_excel("mathSubquestion.xlsx", engine = "openpyxl")

    new_header = df.iloc[1]
    df = df[0:]
    df.columns = new_header 

    global q_id
    q_id = 0
    #print(q_id)

    for i in range(2,len(df)): 
        if df.loc[i,'Stage'] == "BASE":
            authorId = str(df.loc[i,'authorId'])
            subject = str(df.loc[i,'Subject'])
            topic = str(df.loc[i,'Topic'])
            difficulty = str(df.loc[i,'Difficulty'])
            print(authorId, subject,topic,difficulty)
            questionID = post_question(authorId,subject,topic,difficulty)

            stage = str(df.loc[i,'Stage'])
            subQuestionURL = str(df.loc[i,'subQuestionURL'])
            post_baseQuestion(questionID, stage ,subQuestionURL)
            q_id = questionID

        elif df.loc[i,'Stage'] == "COMPREHENSION":
            stage = str(df.loc[i,'Stage'])
            subQuestionURL = str(df.loc[i,'subQuestionURL'])
            post_comprehensionQuestion(q_id,stage,subQuestionURL)
            #print(2222)

        elif df.loc[i,'Stage'] == "EMOTION":
            stage = str(df.loc[i,'Stage'])
            subQuestionURL = str(df.loc[i,'subQuestionURL'])
            post_emotionQuestion(q_id,stage,subQuestionURL)
            #print(3333)

        
if __name__ == "__main__":
    # post_question()
    getAttribute()
