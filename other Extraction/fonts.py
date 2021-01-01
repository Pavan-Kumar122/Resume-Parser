import PyPDF2
from PyPDF2 import PdfFileReader
from pprint import pprint
import docx


def walk(obj, fnt, emb):
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        if [x for x in fontkeys if x in obj]:  # test to see if there is FontFile
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb


if __name__ == '__main__':
    fname = 'reesume.pdf'
    pdf = PdfFileReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        obj = page.getObject()
        if type(obj) == PyPDF2.generic.ArrayObject:
            for i in obj:
                if hasattr(i, 'keys'):
                    f, e = walk(i, fonts, embedded)
                    fonts = fonts.union(f)
                    embedded = embedded.union(e)
        else:
            f, e = walk(obj['/Resources'], fonts, embedded)
            fonts = fonts.union(f)
            embedded = embedded.union(e)
    print('Font List')
    pprint(sorted(list(fonts)))
