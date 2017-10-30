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
    
    #设置字体：常规、斜体、粗体、粗斜体
    addMapping('cjk', 0, 0, 'song')    #normal
    addMapping('cjk', 0, 1, 'fs')    #italic
    addMapping('cjk', 1, 0, 'hei')    #bold
    addMapping('cjk', 1, 1, 'yh')    #italic and bold
   
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'
    
    temp = StringIO()
    p = canvas.Canvas(temp)
    
    #默认(0, 0)点在左下角，此处把原点(0,0)向上和向右移动，后面的尺寸都是相对与此原点设置的
    #注意：移动原点时，向右向上为正，坐标系也是向右为+x，向上为+y
    p.translate(0.5*inch, 0.5*inch)
    #设置字体
    p.setFont('song', 16)
    #设置颜色，画笔色和填充色
    p.setStrokeColorRGB(0.2, 0.5, 0.3)
    p.setFillColorRGB(1, 0, 1)
    #画一个矩形
    p.rect(0, 0, 3*inch, 3*inch, fill=1)
    #旋转文字方向
    p.rotate(90)
    p.setFillColorRGB(0, 0, 0.77)
    p.drawString(3*inch, -3*inch, "我是吴仁智，呵呵！".encode("utf-8"))
    p.rotate(-90)
    p.setFont('yh', 16)
    p.drawString(0, 0, "drawString默认不换行！".encode("utf-8"))
    #插入图片
    p.drawImage("/home/yisl04/public_html/yisl04.png", 5*inch, 5*inch, inch, inch)
    #设置drawString最大宽度
    L = simpleSplit('simpleSplit 只能用于 drawString 英文断行。'.encode("utf-8"), 'yh', 16, 9*inch)
    y = 9*inch
    for t in L:
        p.drawString(0, y, t)
        y -= p._leading

    #Paragraph下中文断行(网上摘抄)
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

    #中文断行还可以使用下面这种简单的方法
    #from reportlab.lib.styles import ParagraphStyle
    #ParagraphStyle.defaults['wordWrap']="CJK"

    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.fontName = 'song'
    style.fontSize = 16
    #设置行距
    style.leading = 20
    #首行缩进
    style.firstLineIndent = 32
    Pa = Paragraph('<b>这里是粗体</b>，<i>这里是斜体</i>, <strike>这是删除线</strike>, <u>这是下划线</u>, <sup>这是上标</sup>, <em>这里是强调</em>, <font color=#ff0000>这是红色</font>'.encode("utf-8"), style)

    Pa.wrapOn(p, 6*inch, 8*inch)
    Pa.drawOn(p, 0, 5*inch)
    
    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response