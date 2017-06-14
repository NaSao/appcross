
from PIL import Image
import qrcode
import uuid
import urllib
import urlparse



url = 'https://mystical-healer-168312.appspot.com/'
img_file = r'E:\qrcode.png'


def url_add_params(url, **params):
    '''add new params to web url'''
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    prlist[4] = urllib.urlencode(query)
    return urlparse.ParseResult(*prlist).geturl()

class DiscountQR:

    
    def QRcode_generator(self):
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,     
            box_size = 10,     
            border = 4,
    
        )

        
        data = url_add_params(url, uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'crossmode'))
        '''print url with uuid, it can be delete'''
        print data
        qr.add_data(data) 
        qr.make(fit=True)  
        img = qr.make_image()

        img = img.convert("RGBA")

        icon = Image.open("icon1.png")

        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img.paste(icon, (w, h), icon)

        img.save(img_file)
        img.show()


if __name__ == "__main__":
    qr1 = DiscountQR()
    qr1.QRcode_generator()
    

