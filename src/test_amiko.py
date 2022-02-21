import functions as fs
import unittest
import sqlite3

con = sqlite3.connect('Amiko.db', check_same_thread=False)
cur=con.cursor()

class TestAmikoBot(unittest.TestCase):

  
    def test_tagcheck1(self):
       check="Электроника 📱"
       self.assertEqual(fs.tagCheck(check), None)
    def test_tagcheck2(self):
       check="asdadsads"
       self.assertEqual(fs.tagCheck(check), 'Ну нет, выбери уже существующие тэги!')
    def test_adduserCheck(self):
       id=298794557
       un="owilover"
       self.assertEqual(fs.addUser(id,un),"Старый Пользователь")
    def test_adduserCheck2(self):
       id=42112341234
       un="owalLavr"
       cur.execute("DELETE FROM Users WHERE IdUser=?",(id,))
       con.commit()
       self.assertEqual(fs.addUser(id,un),"Новый Пользователь")
       
    def test_offCheck(self):
       id=298794557
       self.assertIsNotNone(fs.showUrOff(id))
       
    def test_offCheck2(self):
       id=298731132
       self.assertEqual(fs.showUrOff(id),"")
    def test_updateOff(self):
       id=298794557
       what="descr"
       new="Плюшевая игрушка, пережившая многое..."
       yes=fs.updateOff(id,what,new)
       self.assertAlmostEqual(str(yes[0]),"Описание обновлено! Желаете поменять что-нибудь ещё в этом объявлении?")
       
       
       
       
