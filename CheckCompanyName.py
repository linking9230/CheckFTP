import time
from DownloadFTP import ftpfile
from GetLastFile import getlastfile
from CompareFile import comparefile
from SendEmail import send_email

t=time.time()
dateary=time.localtime(t)
today = time.strftime("%Y%m%d", dateary)

list=['149','125','126']

def remotename(code):
    if code=='125':
        return '125 - US Equity Markets - OTC Composite.txt'
    elif code=='126':
        return '126 - US Equity Markets - Composite.txt'
    elif code=='149':
        return '149 - Cboe BZX Top.txt'
def localname(code):
    return '************** CBOE Market Data\\' + code +'\\' + code + '_'+ today + '.txt'

for code in list:

    latest_path='****************** CBOE Market Data\\' + code
    latest_file=getlastfile(latest_path)

    localpath = localname(code)
    remotepath = remotename(code)

    #从FTP下载文件
    ftpfile(localpath,remotepath)

    #对比文件，并生成Excel
    comparefile(localpath,latest_file,code,today)


#发送邮件
host='smtp.office365.com'
from_account='**************'
from_password='**************'
to_account='*****************'
subject='**************CBOE data daily check ' + today

content =  '''\
Hi all,

Please find difference list between today’s CBOE data and yesterday’s.

Thanks!

Best Regards,

********* '''

attc_name='diff_'+ today +'.xlsx'
attc_file='********************* CBOE Market Data\\'+attc_name

send_email(host,from_account,from_password,to_account,subject,content,attc_name,attc_file)



