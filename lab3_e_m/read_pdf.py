from pypdf import PdfReader

reader=PdfReader("Dispensa laboratorio.pdf")

with open("trans.txt","a") as f: 
    for i in range(36,37):
        page=reader.pages[i]
        text=page.extract_text()
        f.write(text)
