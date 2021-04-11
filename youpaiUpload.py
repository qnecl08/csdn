import threading

import time

from upyun import upyun

import appWatch
import csdnDownDb

up = upyun.UpYun('daixiazai', 'dandinglong', 'zc59763451')
class youpaiWatch(threading.Thread):
    appWatch={}
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.watchUpload()
        except Exception as e:
            print(str(e))
            return False

    def __init__(self,appWatch):
        threading.Thread.__init__(self)
        self.appWatch=appWatch
    def watchUpload(self):
        while 1:
            try:
                time.sleep(5)
                files=csdnDownDb.getFileToUpload()
                for file in files:
                    try:
                        print("代上传文件",files)
                        with open(file['path']+file['file_name'], 'rb') as f:
                            res = up.put('/up/'+file['file_name'], f, checksum=False)
                            print(res)
                            if res['created-date']:
                                csdnDownDb.updateFileStep(file['id'],1)
                                self.appWatch.uploadCount+=1
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))

if __name__ == "__main__":
    appwatch=appWatch.SelfWatch()
    t=youpaiWatch(appwatch)
    t.start()
    while 1:
        time.sleep(3)