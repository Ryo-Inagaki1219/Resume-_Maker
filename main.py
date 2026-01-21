# main.py
from logic import ResumeLogic
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

"""
    文字数制限の判定
    P 現在の入力文字列
    max_len 仕様上の文字制限
"""
def character_limit(P,max_len):
    try:
        limit = int(max_len)
        # 判定ロジック
        return len(P) <= limit
    except ValueError:
        return False


#ラベルとEntryを縦並びにしたカスタムウィジェット
class LabeledEntry(tk.Frame):

    def __init__(self, parent, label_text, entry_size=30):
        super().__init__(parent)
        
        self.pack(pady=0,anchor="w")

        # 左側のラベル
        self.label = tk.Label(self, text=label_text)
        self.label.pack(pady=0,anchor="w")

        # 右側の入力欄
        self.entry = tk.Entry(self,width=entry_size)
        self.entry.pack(expand=True, anchor="w")

    def get_text(self):
        return self.entry.get()

#年　月　内容の入力欄
class DayEntry(tk.Frame):

    def __init__(self,parent):
        super().__init__(parent)
        self.vcmd = self.register(character_limit)
        self.pack()

        self.year_entry = tk.Entry(self,
                          width=5,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 4))
        self.year_entry.pack(side="left", padx=0)

        self.month_entry = tk.Entry(self,
                          width=3,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 2))
        self.month_entry.pack(side="left", padx=1)

        self.text_organization = tk.Entry(self,width=40)
        self.text_organization.pack(side="left", padx=1)
    
    def get_data(self):
        self.data={"year":self.year_entry.get(),"month":self.month_entry.get(),"organization":self.text_organization.get()}
        return self.data
        

#経歴と資格のGUI
class CareerSet(tk.LabelFrame):
    def __init__(self,parent,title,row_count):
        super().__init__(parent,text=title,pady=5)
        self.pack(anchor="w")

        self.header_frame=tk.Frame(self)
        self.header_frame.pack(fill=tk.BOTH, expand=True)

        self.year_label=tk.Label(self.header_frame, text="年")
        self.year_label.pack(side="left", padx=18)

        self.month_label=tk.Label(self.header_frame, text="月")
        self.month_label.pack(side="left", padx=5)

        self.organization_label=tk.Label(self.header_frame,text=title)
        self.organization_label.pack(anchor="s")

        self.DayEntry_list=[]
        for i in range(row_count):
            new_DayEntry = DayEntry(self)
            self.DayEntry_list.append(new_DayEntry)
        
    def get_data(self,key_name):
        count:int=1
        self.data_list ={}
        for  that_DayEntry in self.DayEntry_list:
            self.data_list[key_name+str(count)]={**that_DayEntry.get_data()}
            count+=1
            
        return self.data_list
            

#住所及び連絡先のGUIクラス
class ContactSet(tk.LabelFrame):

    def __init__(self,parent,title):
        super().__init__(parent,text=title,pady=5)
        self.pack(pady=2,anchor="w")
        self.vcmd = self.register(character_limit)

        self.furigana=LabeledEntry(self, "住所(ふりがな)",60)
        self.main_text=LabeledEntry(self, "住所(漢字)",60)


      
        self.telephone_number=LabeledEntry(self, "電話番号")
        self.email_address=LabeledEntry(self, "e-mail")
        self.create_post_code()
    
    #郵便番号のGUI作成
    def create_post_code(self):
        self.post_code_frame=tk.Frame(self)
        self.post_code_frame.pack(anchor="w")
        
        self.post_code_label1 = tk.Label(self.post_code_frame,text="郵便番号" )
        self.post_code_label1.pack(anchor="w")

        self.post_code_first = tk.Entry(self.post_code_frame,
                          width=4,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 3))
        self.post_code_first.pack(side="left", padx=0)

        self.post_code_label2 = tk.Label(self.post_code_frame,text="-" )
        self.post_code_label2.pack(side="left", padx=0)

        self.post_code_latter = tk.Entry(self.post_code_frame,
                          width=5,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 4))
        self.post_code_latter.pack(side="left", padx=0)
    
    #情報送信の関数
    def get_data(self):
        """郵便番号のレイアウト崩れの対策の為、未入力の際は3文字と4文字の空文字を挿入"""
        self.post_code_firs_value=self.post_code_first.get()
        if self.post_code_first.get()=="":
            self.post_code_firs_value="　　　" 
        
        self.post_code_latter_value=self.post_code_latter.get()
        if self.post_code_latter.get()=="":
            self.post_code_latter_value="　　　　"
        
        self.data= {"post_code":self.post_code_firs_value+"-"+self.post_code_latter_value,
                "main_text":self.main_text.get_text(),
                "furigana":self.furigana.get_text(),
                "telephone_number":self.telephone_number.get_text(),
                "email_address":self.email_address.get_text()}
        return self.data

        

    
class MainGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logic = ResumeLogic()

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=15)
        self.option_add("*Entry.font", default_font)
        
        self.title("title")
        self.geometry("800x610")
        self.outer_frame = tk.Frame(self)
        self.outer_frame.pack(fill=tk.BOTH, expand=1)
        
        self.main_canvas = tk.Canvas(self.outer_frame)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        self.main_frame = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((50,0), window=self.main_frame, anchor="nw")

        self.photo_frme = tk.Frame(self.main_frame)
        self.photo_frme.pack(anchor="w")
        self.photo_label=tk.Label(self.photo_frme,width=45,bg="LightGrey")
        self.photo_label.pack(side="left")
        self.photo_select_button=tk.Button(self.photo_frme,text="写真を選択",command=self.photo_select,width=10)
        self.photo_select_button.pack(side="left",padx=5)



        self.furigana_entry = LabeledEntry(self.main_frame, "名前(ふりがな)")
        self.kanji_entry=LabeledEntry(self.main_frame, "名前(漢字)")

        self.furigana_entry.pack(pady=0)
        self.kanji_entry.pack(pady=0)
        
        self.vcmd = self.register(character_limit)
        self.create_birth_date()

        self.gender_entry=LabeledEntry(self.main_frame, "性別")
        self.current_address=ContactSet(self.main_frame,"現住所")
        self.contact_information=ContactSet(self.main_frame,"連絡先")
        self.history_list=CareerSet(self.main_frame,"経歴・学歴",20)
        self.qualified_list=CareerSet(self.main_frame,"免許・資格",11)

        self.pr_label = tk.Label(self.main_frame, text="志望の動機、特技、好きな学科、アピールポイントなど")
        self.pr_label.pack(anchor="w")
        self.pr_text = tk.Text(self.main_frame, width=83, height=9)
        self.pr_text.pack(anchor="w")

        self.free_label = tk.Label(self.main_frame, text="本人希望記入欄（特に給料・職種・勤務時間・勤務地・その他についての希望などがあれば記入)")
        self.free_label.pack(anchor="w")
        self.free_text = tk.Text(self.main_frame, width=83, height=6)
        self.free_text.pack(anchor="w")



        
        self.btn_action = tk.Button(
            self.main_frame,
            text="実行ボタン",
            command=self.create_pdf,
            width=20,
            height=2
        )
        self.btn_action.pack(pady=5)
    
    #フォルダから写真を選択する
    def photo_select(self):
        idir="C:\\" 
        filetype = [("画像ファイル", "*.jpg;*.png;*.jpeg")]
        self.selected_path = filedialog.askopenfilename(filetypes=filetype, initialdir=idir)
        self.photo_label["text"]=self.logic.update_id_photo(self.selected_path)

    #生年月日のGUI作成
    def create_birth_date(self):
        
        self.birth_date_label1 = tk.Label(self.main_frame, text="生年月日")
        self.birth_date_label1.pack(anchor="w")

        self.birth_date_frame=tk.Frame(self.main_frame)
        self.birth_date_frame.pack(anchor="w")
            
        self.birth_date_year = tk.Entry(self.birth_date_frame,
                          width=5,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 4))
        self.birth_date_year.pack(side="left", padx=0)

        self.birth_date_label2 = tk.Label(self.birth_date_frame, text="年",  anchor="e")
        self.birth_date_label2.pack(side="left", padx=0)

        self.birth_date_month = tk.Entry(self.birth_date_frame,
                          width=3,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 2))
        self.birth_date_month.pack(side="left", padx=0)

        self.birth_date_label3 = tk.Label(self.birth_date_frame, text="月", anchor="e")
        self.birth_date_label3.pack(side="left", padx=0)

        self.birth_date_day = tk.Entry(self.birth_date_frame,
                          width=3,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 2))
        self.birth_date_day.pack(side="left", padx=0)

        self.birth_date_label3 = tk.Label(self.birth_date_frame, text="日", anchor="e")
        self.birth_date_label3.pack(side="left", padx=0)

        self.birth_date_label4 = tk.Label(self.birth_date_frame, text="(満", anchor="e")
        self.birth_date_label4.pack(side="left", padx=2)

        self.old_entry= tk.Entry(self.birth_date_frame,
                          width=3,
                          validate="key", 
                          validatecommand=(self.vcmd, '%P', 2))
        self.old_entry.pack(side="left", padx=0)
        self.birth_date_label4 = tk.Label(self.birth_date_frame, text=")歳", anchor="e")
        self.birth_date_label4.pack(side="left", padx=0)



    #GUIより情報取得、PDF発行
    def create_pdf(self):
        self.user_inputs = {
            "user_name": { "kanji": self.kanji_entry.get_text(), "furigana": self.furigana_entry.get_text()},
            "birth_date":{"year":self.birth_date_year.get(),"month":self.birth_date_month.get(),"day":self.birth_date_day.get()},
            "old":self.old_entry.get(),
            "gender":self.gender_entry.get_text(),
            "current_address":{
                    **self.current_address.get_data()
            },
            "contact_information":{
                **self.contact_information.get_data()
            },

            **self.history_list.get_data("history"),
            **self.qualified_list.get_data("qualified"),

            "pr_text":self.pr_text.get("1.0", tk.END),
            "free_text":self.free_text.get("1.0", tk.END)
        }

        self.logic.input_user_data(self.user_inputs)

        #PDF発行命令
        self.output_file = "my_resume.pdf"
        self.logic.generate_pdf(self.output_file)

if __name__ == "__main__":
    #main()
    gui=MainGui()
    gui.mainloop()