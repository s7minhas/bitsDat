def convert_pdf(path, outtype='txt', opts={}):
    import sys
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
    from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfparser import PDFDocument, PDFParser
    from pdfminer.pdfdevice import PDFDevice, TagExtractor
    from pdfminer.cmapdb import CMapDB
    import urllib2

    outfile = path[:-3] + outtype
    outdir = '/'.join(path.split('/')[:-1])

    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    codec = 'utf-8'
    pageno = 1
    scale = 1
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-D': laparams.writing_mode = v
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-O': outdir = v
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFDocument.debug = debug
    PDFParser.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager()
    if not outtype:
        outtype = 'txt'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'txt':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, outdir=outdir)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale, laparams=laparams, outdir=outdir)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return usage()

    fp = open(path, 'rb')
    process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password)
    fp.close()
    device.close()

    outfp.close()
    return
