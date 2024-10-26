from pypdf import PdfReader

reader=PdfReader("GGG-Millikan.pdf")

with open("trans.txt","a") as f: 
    for i in range(0,len(reader.pages)):
        page=reader.pages[i]
        text=page.extract_text()
        f.write(text)