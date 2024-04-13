import os
import PyPDF2
from PIL import Image
from io import BytesIO

def overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates):
    pdf_reader = PyPDF2.PdfFileReader(open(pdf_path, "rb"))
    pdf_writer = PyPDF2.PdfFileWriter()

    page_numbers = [2, 3, 4, 5]

    for i in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(i)
        pdf_writer.addPage(page)

        if (i + 1) in page_numbers:
            x, y = coordinates[i + 1]

            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)

            # Преобразование изображений в PDF страницы для наложения
            image1_pdf = image_to_pdf(image1)
            image2_pdf = image_to_pdf(image2)

            # Наложение первого изображения по указанным координатам
            page.mergeTranslatedPage(image1_pdf.getPage(0), x, y)

            # Наложение второго изображения поверх первого на той же странице
            page.mergeTranslatedPage(image2_pdf.getPage(0), x, y)  

    output_pdf_path = os.path.join(os.getcwd(), "output.pdf")

    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def image_to_pdf(image):
    temp_pdf = BytesIO()
    image.save(temp_pdf, format="PDF", resolution=100.0)
    temp_pdf.seek(0)
    return PyPDF2.PdfFileReader(temp_pdf)

if __name__ == "__main__":
    image1_path = "C:/Users/Super PC/Downloads/Подпись 2.png"
    image2_path = "C:/Users/Super PC/Downloads/печать ГКЗ.png"

    coordinates = {
        2: (70, 70),    # Пример координат для страницы 2
        3: (70, 200),   # Пример координат для страницы 3
        4: (70, 70),    # Пример координат для страницы 4
        5: (400, 500)   # Пример координат для страницы 5
    }

    pdf_path = "C:/Users/Super PC/Downloads/Договор готовый 1.pdf"

    overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates)
