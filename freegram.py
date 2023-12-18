import os
import colorama
import requests
from PIL import Image, ImageFilter, ImageDraw, ImageOps
import mysql.connector as mys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class freegram(QWidget):
    def __init__(self):
        super().__init__()

        # Freegram folder ochish
        try: 
            f=open("C:/Freegram/chek.txt","w")
            f.write("True")
        except:
            os.mkdir('c:/Freegram')
        else:
            f.close()

        # icon 
            # programma ilk marotaba ishga tushurilganda iconka internetdan kochirib olinadi, keyngi ishga tushurishlarda kochirib olingan rasmni ishlatadi(ishga tushurishda vaqtdan yutush uchun)
        try: 
            f=open("C:/Freegram/icon_freegram.jpg","rb")
        except:
            try: 
                icon=requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/800px-Heart_coraz%C3%B3n.svg.png")
            except: 
                print(colorama.Fore.BLUE+"Freegramni "+colorama.Fore.RED+"ishga tushurish uchun siz "+colorama.Fore.GREEN+"internetga "+colorama.Fore.RED+"ulangan bo'lishimgiz kerak!\nqayta uruning!") 
                return 
            else:
                f=open("C:/Freegram/icon_freegram.jpg","wb")
                f.write(icon.content)
        f.close()


        if self.mysql_connection()==False:
            return
        
        self.setFixedSize(1200,700)
        self.setWindowIcon(QIcon("C:/Freegram/icon_freegram.jpg"))
        self.setWindowTitle("Freegram")

        self.setStyleSheet("background-color: #003B46;")
    # profil tanlash
        self.profile_choice()

        self.kursor.execute("use Freegram_managment;")
        self.kursor.execute("select * from freegram_users;")
        userss=self.kursor.fetchall()
        self.users=[]
        for i in userss:
            self.users.append(i[0])

        os.system("cls")
        print(colorama.Fore.GREEN+"Muvofaqiyatli ishga tushurildi",colorama.Fore.RESET+"!")

        self.show()


    def photo_edit(self,path):
        def make_square():
        #kvadrat
            original_image = Image.open(path)
            width, height = original_image.size
        
            new_size = min(width, height)
            left = (width - new_size) // 2
            top = (height - new_size) // 2
            right = left + new_size
            bottom = top + new_size
            
            cropped_image = original_image.crop((left, top, right, bottom))
            squared_image = ImageOps.fit(cropped_image, (new_size, new_size))
        # aylana formasiga otkazish
            mask = Image.new("L", squared_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, squared_image.size[0], squared_image.size[1]), fill=255)
            circular_image = ImageOps.fit(squared_image, mask.size, centering=(0.5, 0.5))
            circular_image.putalpha(mask)
            circular_image.save(path)

        #compress
            circular_image.filter(ImageFilter.GaussianBlur())
            circular_image.thumbnail((100,100))
            circular_image.save(path)

        make_square()
        
        

# profil rasmlari
    def profile_choice(self):
        def profil_img(path):
            def compress(path):
                img=Image.open(path)
                img.filter(ImageFilter.GaussianBlur())
                img.thumbnail((100,100))
                img.save(path)
            
            def circle_shape(path):
                original_image = Image.open(path)
                mask = Image.new("L", original_image.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, original_image.size[0], original_image.size[1]), fill=255)
                circular_image = ImageOps.fit(original_image, mask.size, centering=(0.5, 0.5))
                circular_image.putalpha(mask)
                circular_image.save(path)

            try:
                f=open(path,'rb')
            except:
                profile_img=requests.get("https://img.freepik.com/premium-vector/register-now-icon-in-flat-style-registration-vector-illustration-on-isolated-background-member-notification-sign-business-concept_157943-757.jpg")
                f=open(path,'wb')
                f.write(profile_img.content)

                circle_shape(path)
                compress(path)
            finally:
                f.close()
                    
        profil_img("C:/Freegram/profile_default_img1.png")
        profil_img("C:/Freegram/profile_default_img2.png")
    # profil ismini aniqlash
        def profil_name(default_name,mysql_account_name):
            try:
                self.kursor.execute(f"use {mysql_account_name};")
            except:
                return default_name
            else:
                self.kursor.execute("select * from account_info;")
                name=self.kursor.fetchall()
                if len(name[0][0])<15:
                    return name[0][0]
                else:
                    return name[0][0][0:12]+'...'
            
        account_name1=profil_name('Profil 1','profile_1')
        account_name2=profil_name('Profil 2','profile_2')


        # profile elements declaration
        self.profile_button1=QPushButton(self)
        self.profile_button2=QPushButton(self)
        
        self.profile_label1=QLabel(self)
        self.profile_label2=QLabel(self) 

        self.profile_name1=QPushButton(account_name1,self)
        self.profile_name2=QPushButton(account_name2,self)     

        self.logo=QLabel("Freegram",self)

        self.profile_choice_elements=[self.profile_button1,self.profile_button2,self.profile_label1,self.profile_label2,self.profile_name1,self.profile_name2]


    #tugmalar
        self.profile_button1.setGeometry(440,240,150,180)
        self.profile_button2.setGeometry(610,240,150,180)
        self.profile_label1.setGeometry(464,260,100,100)
        self.profile_label2.setGeometry(634,260,100,100)
        self.logo.setGeometry(15,10,200,50)
        self.profile_name1.setGeometry(443,375,145,20)
        self.profile_name2.setGeometry(613,375,145,20)

        self.profile_button1.setStyleSheet("""background-color: #07575B;
                                              border-radius: 20px;
                                              border-style: solid;
                                              border-width: 1px;
                                              border-color: #66A5AD""")
        self.profile_button2.setStyleSheet("""background-color: #07575B;
                                              border-radius: 20px;
                                              border-style: solid;
                                              border-width: 1px;
                                              border-color: #66A5AD""")
        self.profile_label1.setStyleSheet("border-radius: 50px; ")
        self.profile_label2.setStyleSheet("border-radius: 50px; ")
        self.logo.setStyleSheet("""color: white;""")
        self.profile_name1.setStyleSheet("""background-color: #07575B;
                                            color: white;
                                              border-radius: 20px""")
        self.profile_name2.setStyleSheet("""background-color: #07575B;
                                            color: white;
                                              border-radius: 20px""")
        self.logo.setFont(QFont("calibri",25))
        self.profile_name1.setFont(QFont("calibri",11))
        self.profile_name2.setFont(QFont("calibri",11))
        
        self.profile_label1.setPixmap(QPixmap("C:/Freegram/profile_default_img1.png"))
        self.profile_label2.setPixmap(QPixmap("C:/Freegram/profile_default_img2.png"))

        self.profile_button1.clicked.connect(lambda:self.profil_action("profile_1","profile_default_img1.png"))
        self.profile_button2.clicked.connect(lambda:self.profil_action("profile_2","profile_default_img2.png"))
        self.profile_name1.clicked.connect(lambda:self.profil_action("profile_1","profile_default_img1.png"))
        self.profile_name2.clicked.connect(lambda:self.profil_action("profile_2","profile_default_img2.png"))

    


    def mysql_connection(self,mysql_user='root',mysql_password='root',again=False):
        # ushbu funksiyada MySql da  sizning useringiz root va passwordingiz ham root bolsa hech nima soralmaydi, agar boshqa bolsa bir marotaba soraladi holos, keyngi ishga tushurishlarda soralmaydi!

        mysql_user=mysql_user
        mysql_password=mysql_password
        try:
            f=open('c:/Freegram/mysql_account_Freegram.txt','r')
        except:
            try:
                self.connection=mys.connect(user=mysql_user,password=mysql_password,host='localhost')
            except:
                os.system("cls")
                print("Freegramga Hush Kelibsiz!")
                if again==True:
                    print(colorama.Fore.RED+"User yoki password xato!"+colorama.Fore.RESET+"\n",end='')
                mysql_user=input("Mysql Useringiz: ")
                mysql_password=input("Mysql Passwordingiz: ")
                return self.mysql_connection(mysql_user,mysql_password,True)

                
            else:
                f=open('c:/Freegram/mysql_account_Freegram.txt','w')
                f.write(f"User:{mysql_user} Password:{mysql_password}")
        else:
            mysql_account=f.read()
            mysql_account=mysql_account.split()
            mysql_user=mysql_account[0].split(":")[1]
            mysql_password=mysql_account[1].split(":")[1]
        
        try:
            self.connection=mys.connect(user=mysql_user,password=mysql_password,host='localhost')
            self.kursor=self.connection.cursor()
            try: 
                self.kursor.execute("create database Freegram_managment;")
            except:
                ...
            else:
                users=["@abdukholiq23","@gpt_gram","@Freegram_news"]
                self.kursor.execute("use Freegram_managment;")
                self.kursor.execute("create table Freegram_users(user varchar(255));")
                for i in users:
                    self.kursor.execute(f"""insert into Freegram_users(user) values ("{i}");""")
                    self.connection.commit()
        except:
            print(colorama.Fore.RED+"MySQlingiz ishlamayapti!")
            return False
        else:
            return True
        
    def profil_action(self,profile_name,profile_photo):
        try:
            self.kursor.execute(f"use {profile_name};")
        except:
            self.registration(profile_name,profile_photo)
        else:
            self.ultimate_workplase()
    
    def registration(self,profile_name,profile_photo):
        def back_function(registration_elements):
            for i in registration_elements:
                i.hide()
            if os.path.exists("C:/Freegram/temporary_profile_img.png"):
                os.remove("C:/Freegram/temporary_profile_img.png")
        
        def profile_photo_choice():
            FileDialog=QFileDialog().getOpenFileName(self,"Rasmni tanlang: ","","Image Files (*.jpeg *.png *.jpg)")
            if len(FileDialog[0])>0:
                f=open(FileDialog[0],"rb")
                f1=open("C:/Freegram/temporary_profile_img.png",'wb+')
                f1.write(f.read())
                f.close()
                f1.close()
                self.photo_edit("C:/Freegram/temporary_profile_img.png")
                self.registration_photo_label.setPixmap(QPixmap("C:/Freegram/temporary_profile_img.png"))
        
        def registration_lineedit_control():
            
            if len(self.registration_name_lineedit.text())>255:
                self.registration_warning_name_toolong.show()
            else:
                self.registration_warning_name_toolong.hide()
                
            if len(self.registration_lastname_lineedit.text())>255:
                self.registration_warning_lastname_toolong.show()
            else:
                self.registration_warning_lastname_toolong.hide()
            
            if len(self.registration_user_lineedit.text())>255:
                self.registration_warning_user_toolong.show()
            else:
                self.registration_warning_user_toolong.hide()
                
            if len(self.registration_user_lineedit.text())==0:
                self.registration_user_lineedit.setText("@")

            if self.registration_user_lineedit.text() in self.users:
                self.registration_warning_user_alreadytaken.show()
            else:
                self.registration_warning_user_alreadytaken.hide()
            
            if self.registration_name_lineedit.text()!="":
                self.registration_warning_name_required.hide()
            if self.registration_lastname_lineedit.text()!="":
                self.registration_warning_lastname_required.hide()
            if self.registration_user_lineedit.text()!="@":
                self.registration_warning_user_required.hide()
            
        def finally_button_check():
            check=True
            if self.registration_name_lineedit.text()=="":
                self.registration_warning_name_required.show()
                check=False
            
            if self.registration_lastname_lineedit.text()=="":
                self.registration_warning_lastname_required.show()
                check=False

            if self.registration_user_lineedit.text()=="@":
                self.registration_warning_user_required.show()
                check=False
            
            if self.registration_warning_user_alreadytaken.isVisible():
                check=False
            
            if self.registration_warning_name_toolong.isVisible():
                check=False

            if self.registration_warning_lastname_toolong.isVisible():
                check=False
                
            if self.registration_warning_user_toolong.isVisible():
                check=False
            
            if check:
                finall_action_register()
            
        def finall_action_register(profile_name=profile_name):
            name=self.registration_name_lineedit.text()
            lastname=self.registration_lastname_lineedit.text()
            user=self.registration_user_lineedit.text()

            self.kursor.execute(f"create database {profile_name};")
            self.kursor.execute(f"use {profile_name};")
            self.kursor.execute("create table account_info(name varchar(255), lastname varchar(255), user varchar(255));")
            self.kursor.execute(f"""insert into account_info (name,lastname,user) values ("{name}","{lastname}","{user}");""")
            self.connection.commit()
            self.kursor.execute("use Freegram_managment;")
            self.kursor.execute(f"""insert into Freegram_users(user) values ("{user}");""")
            self.connection.commit()

            if os.path.exists("C:/Freegram/temporary_profile_img.png"):
                f=open("C:/Freegram/temporary_profile_img.png","rb")
                f1=open(f"C:/Freegram/{profile_photo}","wb")
                f1.write(f.read())
                f.close()
                f1.close()
            
            back_function(registration_elements_to_close)
            for i in self.profile_choice_elements:
                i.hide()
            
            self.start_messaging()

                    
        self.registration_main_label=QLabel(self)
        self.registration_welcom_label=QLabel("Welcome!",self)
        self.registration_back_button=QPushButton("←",self)
        self.registration_photo_label=QLabel(self)
        self.registration_setphoto_button=QPushButton("set",self)
        self.registration_name_label=QLabel("First name",self)
        self.registration_name_lineedit=QLineEdit(self)
        self.registration_lastname_label=QLabel("Last name",self)
        self.registration_lastname_lineedit=QLineEdit(self)
        self.registration_user_label=QLabel("User",self)
        self.registration_user_lineedit=QLineEdit("@",self)
        self.registration_finally_button=QPushButton("REGISTER",self)
        self.registration_warning_name_toolong=QLabel("too long",self)
        self.registration_warning_lastname_toolong=QLabel("too long",self)
        self.registration_warning_user_toolong=QLabel("too long",self)
        self.registration_warning_user_alreadytaken=QLabel("already taken",self)
        self.registration_warning_name_required=QLabel("required",self)
        self.registration_warning_lastname_required=QLabel("required",self)
        self.registration_warning_user_required=QLabel("required",self)


        registration_elements_to_open=[self.registration_main_label,self.registration_welcom_label,self.registration_back_button,self.registration_photo_label,self.registration_setphoto_button,self.registration_name_label,self.registration_name_lineedit,self.registration_lastname_label,self.registration_lastname_lineedit,self.registration_user_label,self.registration_user_lineedit,self.registration_finally_button]
        registration_elements_to_close=[self.registration_main_label,self.registration_welcom_label,self.registration_back_button,self.registration_photo_label,self.registration_setphoto_button,self.registration_name_label,self.registration_name_lineedit,self.registration_lastname_label,self.registration_lastname_lineedit,self.registration_user_label,self.registration_user_lineedit,self.registration_finally_button,self.registration_warning_name_toolong,self.registration_warning_lastname_toolong,self.registration_warning_user_toolong,self.registration_warning_user_alreadytaken,self.registration_warning_name_required,self.registration_warning_lastname_required,self.registration_warning_user_required]

        self.registration_main_label.setGeometry(400,100,400,500)
        self.registration_welcom_label.setGeometry(510,130,180,40)
        self.registration_back_button.setGeometry(410,110,40,40)
        self.registration_photo_label.setGeometry(550,190,100,100)
        self.registration_setphoto_button.setGeometry(575,300,50,25)
        self.registration_name_label.setGeometry(450,330,100,20)
        self.registration_name_lineedit.setGeometry(450,355,300,30)
        self.registration_lastname_label.setGeometry(450,400,100,20)
        self.registration_lastname_lineedit.setGeometry(450,425,300,30)
        self.registration_user_label.setGeometry(450,470,100,20)
        self.registration_user_lineedit.setGeometry(450,495,300,30)
        self.registration_finally_button.setGeometry(500,545,200,35)
        self.registration_warning_name_toolong.setGeometry(680,385,70,20)
        self.registration_warning_lastname_toolong.setGeometry(680,455,70,20)
        self.registration_warning_user_toolong.setGeometry(680,525,70,20)
        self.registration_warning_user_alreadytaken.setGeometry(660,525,100,20)
        self.registration_warning_name_required.setGeometry(680,385,70,20)
        self.registration_warning_lastname_required.setGeometry(680,455,70,20)
        self.registration_warning_user_required.setGeometry(680,525,70,20)

        self.registration_main_label.setStyleSheet("""background-color: #07575B;
                                                    border-radius: 20px;
                                                    border-style: solid;
                                                    border-width: 2px;
                                                    border-color: #66A5AD""")
        self.registration_welcom_label.setStyleSheet("""color: white;
                                                     background-color: #07575B;""")
        self.registration_back_button.setStyleSheet("""background-color: #07575B;
                                                    color: white;
                                                    border-radius: 10px""")
        self.registration_photo_label.setStyleSheet("""border-radius: 50px""")
        self.registration_setphoto_button.setStyleSheet("""border-radius: 10px;
                                                        border-width: 1px;
                                                        border-style: solid;
                                                        background-color: #66A5AD;
                                                        border-color: #C4DFE6;
                                                        color: white;""")
        self.registration_name_label.setStyleSheet("""background: #07575B;
                                                   color: white""")
        self.registration_lastname_label.setStyleSheet("""background-color: #07575B;
                                                       color: white""")
        self.registration_user_label.setStyleSheet("""background-color: #07575B;
                                                   color: white""")
        self.registration_name_lineedit.setStyleSheet("""background-color: #044951;
                                                      border-style: solid;
                                                      border-width: 1px;
                                                      border-radius: 10px;
                                                      border-color: #66A5AD;
                                                      color: white""")
        self.registration_lastname_lineedit.setStyleSheet("""background-color: #044951;
                                                      border-style: solid;
                                                      border-width: 1px;
                                                      border-radius: 10px;
                                                      border-color: #66A5AD;
                                                      color: white""")
        self.registration_user_lineedit.setStyleSheet("""background-color: #044951;
                                                      border-style: solid;
                                                      border-width: 1px;
                                                      border-radius: 10px;
                                                      border-color: #66A5AD;
                                                      color: white""")
        self.registration_finally_button.setStyleSheet("""background-color: #66A5AD;
                                                       color: white;
                                                       border-radius: 15px;
                                                       border-style: solid;
                                                       border-color: #C4DFE6;
                                                       border-width: 2px""")
        self.registration_warning_name_toolong.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_lastname_toolong.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_user_toolong.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_user_alreadytaken.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_name_required.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_lastname_required.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        self.registration_warning_user_required.setStyleSheet("""color: red;
                                                            background-color: #07575B""")
        
        self.registration_welcom_label.setFont(QFont("calibri",25))
        self.registration_back_button.setFont(QFont("calibri",15))
        self.registration_setphoto_button.setFont(QFont("calibri",10))
        self.registration_name_label.setFont(QFont("calibri",10))
        self.registration_lastname_label.setFont(QFont("calibri",10))
        self.registration_user_label.setFont(QFont("calibri",10))
        self.registration_name_lineedit.setFont(QFont("calibri",11))
        self.registration_lastname_lineedit.setFont(QFont("calibri",11))
        self.registration_user_lineedit.setFont(QFont("calibri",11))
        self.registration_finally_button.setFont(QFont("calibri",11))
        self.registration_warning_name_toolong.setFont(QFont("calibri",10))
        self.registration_warning_lastname_toolong.setFont(QFont("calibri",10))
        self.registration_warning_user_toolong.setFont(QFont("calibri",10))
        self.registration_warning_user_alreadytaken.setFont(QFont("calibri",10))
        self.registration_warning_name_required.setFont(QFont("calibri",10))
        self.registration_warning_lastname_required.setFont(QFont("calibri",10))
        self.registration_warning_user_required.setFont(QFont("calibri",10))


        self.registration_name_lineedit.textChanged.connect(registration_lineedit_control)
        self.registration_lastname_lineedit.textChanged.connect(registration_lineedit_control)
        self.registration_user_lineedit.textChanged.connect(registration_lineedit_control)

        self.registration_back_button.clicked.connect(lambda:back_function(registration_elements_to_close))
        self.registration_setphoto_button.clicked.connect(profile_photo_choice)
        self.registration_finally_button.clicked.connect(finally_button_check)

        self.registration_photo_label.setPixmap(QPixmap(f"C:/Freegram/{profile_photo}"))

        for i in registration_elements_to_open:
            i.show()


    def start_messaging(self):
        def start_messaging():
            for i in self.start_messaging_elements:
                i.hide()
            return self.ultimate_workplase()
        self.start_messaging_succesfullyregistered_label=QLabel("Successfully registered!",self)
        self.start_messaging_startmessaging_button=QPushButton("Start messaging",self)

        self.start_messaging_succesfullyregistered_label.setGeometry(400,250,700,100)
        self.start_messaging_startmessaging_button.setGeometry(525,350,200,50)

        self.start_messaging_succesfullyregistered_label.setStyleSheet("""color: white""")
        self.start_messaging_startmessaging_button.setStyleSheet("""color: white;
                                                                 background-color: #66A5AD;
                                                                 border-radius: 15px;
                                                                 border-style: solid;
                                                                 border-width: 2px;
                                                                 border-color: #C4DFE6""")

        self.start_messaging_succesfullyregistered_label.setFont(QFont("calibri",30))
        self.start_messaging_startmessaging_button.setFont(QFont("calibri",15))


        self.start_messaging_elements=[self.start_messaging_succesfullyregistered_label,self.start_messaging_startmessaging_button]

        for i in self.start_messaging_elements:
            i.show()
        
        self.start_messaging_startmessaging_button.clicked.connect(start_messaging)
    
    def ultimate_workplase(self):
        print("soon")


   
if "__main__"==__name__:
    os.system("cls")
    app=QApplication([])
    ilova=freegram()
    app.exec()