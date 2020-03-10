#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import types
import subprocess
import re
import os
from time import strftime, gmtime
import yaml
import string
from pkgutil import iter_modules

def Singleton(cls):
    _instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance


class MySession:
    _datas = {}
    
    def get(self, key, default=None):
        return self._datas.get(key, default)
    
    def set(self, key, value):
        self._datas[key] = value
        
        
class MyConfig():
    datas = []
    
    def get(self, attr, default=None):
        try:
            return getattr(self, attr)
        except KeyError:
            return default
    
    def load(self, fi="config.yml"):
        if os.path.exists(fi):
            with open(fi, 'r') as fi:
                self.datas = yaml.safe_load(fi)
        self.on_load()
    
    def on_load(self):
        pass
            
            
class MyLog():
    def __init__(self, fo="log.txt"):
        self.fo = fo
        
    def message(self, msg, status):
        MyCore.debug(msg, status)
        self._write(strftime(status+"    %Y-%m-%d %H:%M:%S", gmtime())+" - "+msg)
    
    def success(self, msg):
        MyCore.debug(msg, "OK")
        self._write(strftime("OK    %Y-%m-%d %H:%M:%S", gmtime())+" - "+msg)
        
    def info(self, msg):
        MyCore.debug(msg, "INFO")
        self._write(strftime("INFO  %Y-%m-%d %H:%M:%S", gmtime())+" - "+msg)
        
    def warning(self, msg):
        MyCore.debug(msg, "WARN")
        self._write(strftime("WARN  %Y-%m-%d %H:%M:%S", gmtime())+" - "+msg)
        
    def error(self, msg):
        MyCore.debug(msg, "ERROR")
        self._write(strftime("ERROR %Y-%m-%d %H:%M:%S", gmtime())+" - "+msg)
            
    def _write(self, msg):
        with open(self.fo, "a") as tmp_fo:
            tmp_fo.write('{}\n'.format(msg))
                

    # from operator import itemgetter, attrgetter, methodcaller
    # sorted (t, key=itemgetter(1,2))  # tri sur 2 colonnes !!
    # sorted (o, key=attrgetter('grade', 'nom'), reverse=True)  # tri sur 2 attributs descendant !!
    # sorted (o, key=methodcaller('method1', 'method2'))  # tri sur 2 methodes !!
        
        
class MyStr():
    @staticmethod
    def camelize(string):
        """
        >>> MyStr.camelize('example_Text to_Camelize')
        'exampleTextToCamelize'
        """
        return string[0].lower() + re.sub(r"(?:_| )(.)", lambda m: m.group(1).upper(), string[1:])
    
    @staticmethod
    def pascalize(string):
        """
        >>> MyStr.pascalize('example_Text to_Pascalize')
        'ExampleTextToPascalize'
        """
        return re.sub(r"(?:^|_| )(.)", lambda m: m.group(1).upper(), string)

    @staticmethod
    def spinalize(string):
        """
        >>> MyStr.spinalize('example_Text to_Spinalize')
        'example-text-to-spinalize'
        """
        return re.sub(r"(?:_| )", "-", string.lower())

    @staticmethod
    def snakelize(string):
        """
        >>> MyStr.snakelize('example_Text to_Snakelize')
        'example_text_to_snakelize'
        """
        return re.sub(r"(?:-| )", "_", string.lower())

    @staticmethod
    def capitalize_first_letter(string):
        """
        >>> MyStr.capitalize_first_letter('example_Text to_capitalize_first_letter')
        'Example_Text to_capitalize_first_letter'
        """
        return string[0].upper()+string[1:]

    @staticmethod
    def capitalize_each_word(string):
        """
        >>> MyStr.capitalize_each_word('example_Text to_capitalize_each_word')
        'Example_Text to_capitalize_each_word'
        """
        return string[0].upper()+string[1:]

    @staticmethod
    def to_list(string, separator=" "):
        """
        >>> MyStr.to_list('example|Text|to|list', '|')
        ['example', 'Text', 'to', 'list']
        """
        return string.split(separator)
    
    @staticmethod
    def valid_filename(s):
        s = re.sub("[à]", "a", s)
        s = re.sub("[é|è|ê]", "e", s)
        s = re.sub("[É]", "E", s)
        s = re.sub("[ô]", "o", s)
        s = re.sub("[Ô]", "O", s)
        s = re.sub("[û]", "u", s)
        
        valid_chars = "&/-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in s if c in valid_chars)
            

class MyFile():
    @staticmethod
    def load(fi, output_type=list):
        res = []
        with open(fi, 'r') as f:
            for ln in f:
                ln = re.sub(r'\n', '',ln)
                res.append(ln)
        return res
        
    @staticmethod
    def load_split(fi, split='|'):
        res = []
        with open(fi, 'r') as f:
            for ln in f:
                ln = re.sub(r'\n', '',ln)
                res.append(ln.split(split))
        return res
    
    @staticmethod
    def write(streami, fo):
        if isinstance(streami, (list, tuple)):
            with open(fo, "w") as tmp_fo:
                for ln in streami:
                    if ln[:-1] != '\n':
                        tmp_fo.write(ln+'\n')
                    else:
                        tmp_fo.write(ln)
        elif isinstance(streami, str): 
            with open(fo, "w") as tmp_fo:
                tmp_fo.write(streami)
    
    @staticmethod
    def append(streami, fo):
        if isinstance(streami, (list, tuple)):
            with open(fo, "a") as tmp_fo:
                tmp_fo.writelines(streami)
            

class MyOs:    
    class Cd:
        """exemple 
        with cd("my/path"):
            instructions
        """
        def __init__(self, newPath):
            self.newPath = os.path.expanduser(newPath)
            
        def __enter__(self):
            self.savedPath = os.getcwd()
            os.chdir(self.newPath)
            
        def __exit__(self, etype, value, traceback):
            os.chdir(self.savedPath)

    @staticmethod
    def count_line(fi):
        if os.path.exists(fi):
            return sum(1 for line in open(fi))
        else:
            return -1
        
#     @staticmethod
#     def is_diff(file1, file2, render=False):
#         try:
#             time_start = datetime.now()
#             subprocess.check_output("diff {} {}".format(file1, file2), shell=True)
#             if render:
#                 Cli.Render.alert("{:<100} {:>8}".format(file2, Cli.Render.time(time_start)), "SUCCESS")
#             return False
#         except subprocess.CalledProcessError as e:
#             if e.returncode == 1:
#                 if render:
#                     Cli.Render.alert("{:<100} {:>8}".format(file2, Cli.Render.time(time_start)), "WARNING")
#                 return True
#             else:
#                 Cli.Render.alert("{:<100} {:>8}".format(file2, Cli.Render.time(time_start)), "DANGER")
#                 return True
        
    @staticmethod
    def ls_file(path, pattern=None):
        if pattern is None:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    yield f
        else:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    if re.match(pattern, f):
                        yield f
                    
    @staticmethod
    def first_file(path, pattern=None):
        if pattern is None:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    return f
        else:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    if re.match(pattern, f):
                        return f
                    
    @staticmethod
    def count_file(path, pattern=None):
        count = 0
        if pattern is None:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    count += 1
        else:
            for f in os.listdir(path):
                if os.path.isfile(path + f):
                    if re.match(pattern, f):
                        count += 1
        return count

#     @staticmethod
#     def cp(source, destination, confirm=False):
#         if confirm:
#             if Cli.Render.confirm("Copier le fichier "+source):
#                 shutil.copy(source, destination)
#         else:
#             shutil.copy(source, destination)
#     
#     @staticmethod        
#     def rm(filename, confirm=False):
#         if os.path.exists(filename):
#             try:
#                 if confirm:
#                     if Cli.Render.confirm("Supprimer le fichier "+filename):
#                         os.remove(filename)
#                 else:
#                     os.remove(filename)
#             except OSError as e:
#                 print("Error: {} - {}".format(e.filename, e.strerror))

#     @staticmethod
#     def cp_files(source, destination, recursive=False, force=False):
#         for file in glob.glob(source):
#             if os.path.isfile(file):
#                 dest_file = destination+os.path.split(file)[1]
#                 if os.path.isfile(dest_file):
#                     if not force:
#                         if os.stat(dest_file).st_size != os.stat(file).st_size:
#                             if Cli.Render.confirm('Ecraser ' + dest_file):
#                                 shutil.copy(file, dest_file)
#                     else:
#                         shutil.copy(file, dest_file)
#                 else:
#                     shutil.copy(file, dest_file)
                    
    # def subprocess(cmd=None, retry=False, render_error=True):
        # again = True
        # while again:
            # try:
                # time_start = datetime.now()
                # subprocess.check_call(cmd, shell=True)
                # Cli.Render.alert("{:<100} {:>8}".format(cmd, Cli.Render.time(time_start)), "SUCCESS")
                # again = False
            # except subprocess.CalledProcessError:
                # if(render_error):
                    # Cli.Render.alert('Erreur lors de l execution de ' + cmd, "DANGER")
                # if retry:
                    # if Cli.Render.confirm("Reessayer la commande " + cmd + "?") == False:
                        # again = False
                # else:
                    # again = False

    # def diff(file1, file2, output=None):
        # time_start = datetime.now()
        # if output is None:
            # rs = subprocess.call("diff {} {}".format(file1, file2), shell=True)
        # else:
            # rs = subprocess.call("diff {} {} > {}".format(file1, file2, output), shell=True)
        
        # if rs == 0:
            # Cli.Render.alert("{:<100} {:>8}".format("no diff", Cli.Render.time(time_start)), "SUCCESS")
        # if rs == 1:
            # Cli.Render.alert("{:<100} {:>8}".format("diff", Cli.Render.time(time_start)), "SUCCESS")
        # return rs
    
    @staticmethod                  
    def subprocess_output(cmd=None):
        return subprocess.check_output(cmd, shell=True)     
    
    @staticmethod
    def subprocess_check_call(cmd=None):
        return subprocess.check_call(cmd, shell=True)
    

class MyCore():
    @staticmethod
    def hasmethod(obj, name):
        return hasattr(obj, name) and type(getattr(obj, name)) == types.MethodType
    
    @staticmethod
    def debug(msg, etat=''):
        if etat == '':
            print('{}'.format(msg))
        else:
            print('{:10}{}'.format(etat, msg))
            
    @staticmethod
    def module_exists(module_name):
        return module_name in (name for loader, name, ispkg in iter_modules())


class MyCli():
    COLORS = {
        'SUCCESS' : '\033[1;32;40m',
        'INFO' : '\033[1;34;40m',
        'WARNING' : '\033[1;33;40m',
        'DANGER' : '\033[1;31;40m',
        'UNDERLINE' : '\033[4m',
        'BG_SUCCESS' : '\033[1;30;42m',
        'BG_INFO' : '\033[1;30;44m',
        'BG_WARNING' : '\033[1;30;43m',
        'BG_DANGER' : '\033[1;30;41m',
        'ENDC' : '\033[0m',
    }

    @staticmethod
    def key_press():
        print("")
        raw_input("Appuyer [Entrer] pour continuer")

       

    @staticmethod
    def color(content, color):
        if color in MyCli.COLORS:
            return MyCli.COLORS.get(color) + content + MyCli.COLORS.get("ENDC")
        else:
            return content

    @staticmethod
    def success(content):
        print(MyCli.color(content, "SUCCESS"))

    @staticmethod
    def info(content):
        print(MyCli.color(content, "INFO"))
    
    @staticmethod
    def warning(content):
        print(MyCli.color(content, "WARNING"))

    @staticmethod
    def danger(content):
        print(MyCli.color(content, "DANGER"))
    
# class MyMail():
#     def __init__(self):
#         self.config = MyConfig()
#     
#     @staticmethod
#     def send(to, subject, msg, sender=None):
#         if sender is None:
#             sender = self.config['core']['mail']['sender']
#         server = smtplib.SMTP(self.config['core']['mail']['host'], 587)
#         server.ehlo()
#         server.starttls()
#         server.login(self.config['core']['mail']['user'], self.config['core']['mail']['password'])
#         msg = """\
#         From: %s
#         To: %s
#         Subject: %s
# 
#         %s
#         """ % (sender, ", ".join(to), subject, msg)
#          
#         server.sendmail(self.config['core']['mail']['sender'], to, msg)
#         server.quit()
