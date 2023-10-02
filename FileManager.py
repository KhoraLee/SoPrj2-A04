import pandas as pd
from utility import *

class FileManager:

    def __init__(self):
        self.file_path = "./resource/TodoList_Datas.csv"
        try:
            self.df=pd.read_csv(self.file_path)
        except FileNotFoundError:
            self.df=pd.DataFrame({
                "작업 이름": [], "마감 날짜": [], "반복": []
            })
            self.df.to_csv(self.file_path, index=False)

    def sortTodoList(self):
        self.df=self.df.sort_values(by='마감 날짜')
        self.df.to_csv(self.file_path, index=False)

    def returnRowByIndex(self, index):
        return self.df.iloc[index]

    def deleteTodo(self, index):
        self.df.drop(index, inplace=True)
        self.df.to_csv(self.file_path, index=False)

    def filterTodoList(self):
        years_df = self.df[(self.df['반복']=="매년") & self.df['마감 날짜'].apply(filter_by_year)]
        month_df=self.df[(self.df['반복']=="매달") & self.df['마감 날짜'].apply(filter_by_month)]
        week_df=self.df[(self.df['반복']=="매주") & self.df['마감 날짜'].apply(filter_by_week)]
        none_df=self.df[(self.df['반복']=="없음") & self.df['마감 날짜'].apply(filter_by_day)]
        filter_df=pd.concat([years_df,month_df,week_df,none_df])
        return filter_df

    def isValidFile(self):
        for index,row in self.df.iterrows():
            row_data = {'index': index, 'data': row.to_dict()}
            if(is_valid_title(row_data['data']['작업 이름'])
                    and is_valid_date(row_data['data']['마감 날짜'])
                    and is_valid_deadline(row_data['data']['반복'])):
                continue
            else:
                print(f'오류: 데이터 파일 TodoList_Datas.csv에 문법 규칙과 의미 규칙에 위배되는 행이 {index+2}행에 존재합니다.')
                return False
        return True



