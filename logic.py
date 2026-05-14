import os
import webbrowser
import datetime
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape
gtk_path = r'C:\Program Files\GTK3-Runtime Win64\bin'
if os.path.exists(gtk_path):
    os.add_dll_directory(gtk_path)
from weasyprint import HTML

class ResumeLogic:
    def __init__(self):
        #相対パスの取得
        self.base_path = os.path.dirname(os.path.abspath(__file__))
    
    #入力情報の受け取り
    def input_user_data(self, user_data):
        self.user_data = user_data
    
    #証明写真の差し替え、正常ならユーザが指定したパスを返す
    def update_id_photo(self, selected_source_path):
        try:
            return selected_source_path
            
        except PermissionError:
            text="エラー: ID_photo.png が他のソフトで開かれているため上書きできませんでした。"
            return text
        except Exception as e:
            text=f"予期せぬエラー: {e}"
            return text
        
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