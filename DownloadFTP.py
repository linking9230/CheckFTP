import ftplib

class ftpfile():

    def __init__(self,localpath,remotepath):
        host = '**************'
        user = '*********'
        password = '************'
        buffer_size = 8192
        port = '21'

        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        ftp.cwd('/Symbol Guides')

        fp = open(localpath, 'wb')
        ftppath='RETR /Symbol Guides/' + remotepath
        ftp.retrbinary(ftppath, fp.write, buffer_size)

        fp.close()
        ftp.quit()


