
import sqlite3


def addUser(id, name):
    con = sqlite3.connect('Amiko.db', check_same_thread=False)
    cur=con.cursor()
    if (cur.execute("SELECT IdUser FROM Users WHERE IdUser=?",(id,)).fetchone() is None) :
        cur.execute("INSERT INTO Users (IdUser,Username) VALUES (?,?)",(str(id) , str(name))),
        con.commit()
        con.close()
        return "Новый Пользователь"
    else:
        cur.execute("UPDATE Users SET Username=? WHERE IdUser=?", (name,id,))
        con.commit()
        con.close()
        return "Старый Пользователь"
        
def showUrOff(id):
    con = sqlite3.connect('Amiko.db', check_same_thread=False)
    cur=con.cursor()
    counter=1;
    list="";
    for value in cur.execute("SELECT Name, PhotoId, Description FROM Offers WHERE UserId = ?", (id,)) :

        list=list+f'{counter}. {value[0]} \n'
        counter=counter+1;
    con.close()
    return list

def tagCheck(tag):
    if (tag!='Электроника 📱' and tag!='Игрушки 🧸' and tag!='Животные 🐶' and tag!='Другое 🤔'):
        check='Ну нет, выбери уже существующие тэги!'
        return check
    
def updateOff(id, what, new):
    con = sqlite3.connect('Amiko.db', check_same_thread=False)
    cur=con.cursor()
    answer1=""
    answer2=[]
    if (what=='descr'):
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            cur.execute("UPDATE Offers SET Description=? WHERE UserId=? AND PhotoId=? AND Name=? AND DateTime=?", (new,value[0],value[2],value[1],value[4]))
            con.commit();
            cur.execute("UPDATE Buffer SET Descr=? WHERE UserId=?",(new, value[0]))
            con.commit();
        
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            answer1="Описание обновлено! Желаете поменять что-нибудь ещё в этом объявлении?"
            answer2=value[2], value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5]
        return answer1, answer2
    if(what=='photo'):
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            cur.execute("UPDATE Offers SET PhotoId=? WHERE UserId=? AND Name=? AND Description=? AND DateTime=?", (new,value[0],value[1],value[3],value[4]))
            con.commit();
            cur.execute("UPDATE Buffer SET PhotoId=? WHERE UserId=?",(new, id))
            con.commit();
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            answer1="Фото обновлено! Желаете поменять что-нибудь ещё в этом объявлении?"
            answer2=value[2], value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5]
        return answer1, answer2
    if(what=='name'):
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            cur.execute("UPDATE Offers SET Name=? WHERE UserId=? AND PhotoId=? AND Description=? AND DateTime=?", (new,value[0],value[2],value[3],value[4]))
            con.commit();
            cur.execute("UPDATE Buffer SET Name=? WHERE UserId=?",(new, id))
            con.commit();   
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            answer1="Имя обновлено! Желаете поменять что-нибудь ещё в этом объявлении?"
            answer2=value[2], value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5]
        return answer1, answer2
    if(what=='tag'):
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            cur.execute("UPDATE Offers SET Tag=? WHERE UserId=? AND PhotoId=? AND Name=? AND Description =? AND DateTime=?", (new,value[0],value[2],value[1],value[3],value[4]))
            con.commit();
            cur.execute("UPDATE Buffer SET Tag=? WHERE UserId=?",(new, id))
            con.commit();
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (id,)) :
            answer1="Тэг обновлён! Желаете поменять что-нибудь ещё в этом объявлении?"
            answer2=value[2], value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5]
        return answer1, answer2
        
con = sqlite3.connect('Amiko.db', check_same_thread=False)
cur=con.cursor()
for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (433677194,)) :
            answer1="Описание обновлено! Желаете поменять что-нибудь ещё в этом объявлении?"
            answer2=value[2], value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5]
            print(answer1, answer2[1])
            
print(showUrOff(298794557))
print(tagCheck("Игрушки 🧸"))