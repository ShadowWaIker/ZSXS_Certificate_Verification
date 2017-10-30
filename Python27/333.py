#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponse
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping

def hello_pdf(request):
    rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('song', '/home/yisl04/.fonts/simsun.ttc'))
    pdfmetrics.registerFont(TTFont('fs', '/home/yisl04/.fonts/simfang.ttf'))
    pdfmetrics.registerFont(TTFont('hei', '/home/yisl04/.fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('yh', '/home/yisl04/.fonts/msyh.ttf'))
    
    #�������壺���桢б�塢���塢��б��
    addMapping('cjk', 0, 0, 'song')    #normal
    addMapping('cjk', 0, 1, 'fs')    #italic
    addMapping('cjk', 1, 0, 'hei')    #bold
    addMapping('cjk', 1, 1, 'yh')    #italic and bold
   
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'
    
    temp = StringIO()
    p = canvas.Canvas(temp)
    
    #Ĭ��(0, 0)�������½ǣ��˴���ԭ��(0,0)���Ϻ������ƶ�������ĳߴ綼��������ԭ�����õ�
    #ע�⣺�ƶ�ԭ��ʱ����������Ϊ��������ϵҲ������Ϊ+x������Ϊ+y
    p.translate(0.5*inch, 0.5*inch)
    #��������
    p.setFont('song', 16)
    #������ɫ������ɫ�����ɫ
    p.setStrokeColorRGB(0.2, 0.5, 0.3)
    p.setFillColorRGB(1, 0, 1)
    #��һ������
    p.rect(0, 0, 3*inch, 3*inch, fill=1)
    #��ת���ַ���
    p.rotate(90)
    p.setFillColorRGB(0, 0, 0.77)
    p.drawString(3*inch, -3*inch, "���������ǣ��Ǻǣ�".encode("utf-8"))
    p.rotate(-90)
    p.setFont('yh', 16)
    p.drawString(0, 0, "drawStringĬ�ϲ����У�".encode("utf-8"))
    #����ͼƬ
    p.drawImage("/home/yisl04/public_html/yisl04.png", 5*inch, 5*inch, inch, inch)
    #����drawString�����
    L = simpleSplit('simpleSplit ֻ������ drawString Ӣ�Ķ��С�'.encode("utf-8"), 'yh', 16, 9*inch)
    y = 9*inch
    for t in L:
        p.drawString(0, y, t)
        y -= p._leading

    #Paragraph�����Ķ���(����ժ��)
    def wrap(self, availWidth, availHeight):
    # work out widths array for breaking
        self.width = availWidth
        leftIndent = self.style.leftIndent
        first_line_width = availWidth - (leftIndent+self.style.firstLineIndent) - self.style.rightIndent
        later_widths = availWidth - leftIndent - self.style.rightIndent
        try:
            self.blPara = self.breakLinesCJK([first_line_width, later_widths])
        except:
            self.blPara = self.breakLines([first_line_width, later_widths])
        self.height = len(self.blPara.lines) * self.style.leading
        return (self.width, self.height)
    Paragraph.wrap = wrap

    #���Ķ��л�����ʹ���������ּ򵥵ķ���
    #from reportlab.lib.styles import ParagraphStyle
    #ParagraphStyle.defaults['wordWrap']="CJK"

    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.fontName = 'song'
    style.fontSize = 16
    #�����о�
    style.leading = 20
    #��������
    style.firstLineIndent = 32
    Pa = Paragraph('<b>�����Ǵ���</b>��<i>������б��</i>, <strike>����ɾ����</strike>, <u>�����»���</u>, <sup>�����ϱ�</sup>, <em>������ǿ��</em>, <font color=#ff0000>���Ǻ�ɫ</font>'.encode("utf-8"), style)

    Pa.wrapOn(p, 6*inch, 8*inch)
    Pa.drawOn(p, 0, 5*inch)
    
    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response