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

            # Открываем изображения
            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)

            # Изменяем размер изображений
            image1_resized = resize_image(image1, new_width=300, new_height=120)  # Пример нового размера (300x120)
            image2_resized = resize_image(image2, new_width=150, new_height=150)  # Пример нового размера (150x150)

            # Преобразуем изображения в PDF страницы для наложения
            image1_pdf = image_to_pdf(image1_resized)
            image2_pdf = image_to_pdf(image2_resized)

            # Наложение первого изображения по указанным координатам
            page.mergeTranslatedPage(image1_pdf.getPage(0), x, y)

            # Наложение второго изображения по координатам 2
            
            page.mergeTranslatedPage(image2_pdf.getPage(0), x, y)

            # Наложение второго изображения по координатам 2_1
            key_2_1 = str(i + 1) + "_1"  # Формируем правильный ключ для словаря
            if key_2_1 in coordinates:
                x2_1, y2_1 = coordinates[key_2_1]
                page.mergeTranslatedPage(image1_pdf.getPage(0), x2_1, y2_1)
                page.mergeTranslatedPage(image2_pdf.getPage(0), x2_1, y2_1)

    output_pdf_path = os.path.join(os.getcwd(), "output.pdf")

    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def image_to_pdf(image):
    temp_pdf = BytesIO()
    image.save(temp_pdf, format="PDF", resolution=100.0)
    temp_pdf.seek(0)
    return PyPDF2.PdfFileReader(temp_pdf)

def resize_image(image, new_width, new_height):
    return image.resize((new_width, new_height))

if __name__ == "__main__":
    image1_path = "C:/Users/Super PC/Downloads/Подпись 2.png"
    image2_path = "C:/Users/Super PC/Downloads/печать ГКЗ.png"

    coordinates = {
        2: (70, 70),     # Пример координат для страницы 2
        "2_1": (320, 70), # Дополнительные координаты для страницы 2_1
        3: (70, 200),    # Пример координат для страницы 3
        "3_1": (320, 200), # Дополнительные координаты для страницы 3_1
        5: (400, 500)    # Пример координат для страницы 5
    }

    pdf_path = "C:/Users/Super PC/Downloads/Договор готовый 1.pdf"

    overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates)
