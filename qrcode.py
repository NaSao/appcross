import uuid

url = 'https://mystical-healer-168312.appspot.com/qcode'
   
def QRCode_generator():
    width = 200
    length = 200   
    data = url+'?uuid='+ str(uuid.uuid5(uuid.NAMESPACE_DNS, 'crossmode'))
    return 'http://chart.apis.google.com/chart?cht=qr'+'&chs='+ str(width)+'x' + str(length) + '&chl='+ data

print QRCode_generator()

