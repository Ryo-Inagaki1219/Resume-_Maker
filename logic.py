import os
import webbrowser
import datetime
import json
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape
gtk_path = r'C:\Program Files\GTK3-Runtime Win64\bin'
if os.path.exists(gtk_path):
    os.add_dll_directory(gtk_path)
from weasyprint import HTML

class Photologic:
    def __init__(self):
        #相対パスの取得と保存パスの作成
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.default_path=os.path.abspath("select_photo.png")

    def get_default_path(self):
        return self.default_path

    def search_photo(self,search_path):
            if os.path.exists(search_path):
                return True
            else:
                return False

class Keeplogic:
    def __init__(self):
        #相対パスの取得と保存パスの作成
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.keepjson_path=os.path.join(self.base_path, "keep.json")

    def search_json(self):
        if os.path.exists(self.keepjson_path):
            return True
        else:
            return False

    def search_picture(self,image_path):
            if os.path.exists(image_path):
                return True
            else:
                return False
    
    def load_json(self):
        with open(self.keepjson_path, 'r', encoding='utf-8') as json_open:
            return json.load(json_open)

    def write_json(self,task_data):
        with open(self.keepjson_path, 'w',encoding='utf-8') as f:
            json.dump(task_data, f)



class ResumeLogic:
    def __init__(self):
        #相対パスの取得
        self.base_path = os.path.dirname(os.path.abspath(__file__))
    
    #入力情報の受け取り
    def input_user_data(self, user_data):
        self.user_data = user_data
        
    #データの展開とPDFの作成
    def generate_pdf(self, output_filename, template_filename="template.html"):
    
        #本日の日付を取得して整形
        now = datetime.datetime.now()
        formatted_date = f"{now.year}年 {now.month}月 {now.day}日"

        render_data = {
            "current_date": formatted_date,
            **self.user_data 
        }

        #テンプレートの読み込みとレンダリング
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(template_filename)
        html_out = template.render(render_data)

        # PDF発行
        HTML(string=html_out,base_url=self.base_path).write_pdf(output_filename)
        webbrowser.open(output_filename)