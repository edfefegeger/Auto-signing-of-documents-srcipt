import os
import PyPDF2
from PIL import Image
from io import BytesIO
from tkinter import Tk, filedialog

def overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates):
    pdf_reader = PyPDF2.PdfFileReader(open(pdf_path, "rb"))
    pdf_writer = PyPDF2.PdfFileWriter()

    page_numbers = list(coordinates.keys())  # Используем страницы из указанных координат

    for i in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(i)
        pdf_writer.addPage(page)

        if (i + 1) in page_numbers:
            x, y = coordinates[i + 1]

            # Открываем изображения
            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)

            # Изменяем размер изображений
            image1_resized = resize_image(image1, new_width=width_image1, new_height=height_image1)  # Пример нового размера (300x120)
            image2_resized = resize_image(image2, new_width=width_image2, new_height=height_image2)  # Пример нового размера (150x150)

            # Преобразуем изображения в PDF страницы для наложения
            image1_pdf = image_to_pdf(image1_resized)
            image2_pdf = image_to_pdf(image2_resized)

            # Наложение первого изображения по указанным координатам
            page.mergeTranslatedPage(image1_pdf.getPage(0), x, y)

            # Наложение второго изображения по координатам
            if i + 1 in coordinates:
                page.mergeTranslatedPage(image2_pdf.getPage(0), x, y)

            # Наложение дополнительных изображений по координатам вида "страница_1"
            if f"{i + 1}_1" in coordinates:
                x_additional, y_additional = coordinates[f"{i + 1}_1"]
                page.mergeTranslatedPage(image1_pdf.getPage(0), x_additional, y_additional)
                page.mergeTranslatedPage(image2_pdf.getPage(0), x_additional, y_additional)

    output_pdf_path = os.path.join(os.getcwd(), "Result.pdf")

    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def image_to_pdf(image):
    temp_pdf = BytesIO()
    image.save(temp_pdf, format="PDF", resolution=100.0)
    temp_pdf.seek(0)
    return PyPDF2.PdfFileReader(temp_pdf)

def resize_image(image, new_width, new_height):
    return image.resize((new_width, new_height))

def generate_additional_coordinates(coordinates):
    additional_coordinates = {}

    for page, coord in coordinates.items():
        if isinstance(page, int):
            page_str = str(page)
            additional_key = f"{page_str}_1"
            additional_coordinates[additional_key] = (coord[0] + 250, coord[1])  # Пример смещения для x на 250

    coordinates.update(additional_coordinates)
    return coordinates

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Скрыть основное окно Tkinter
    width_image1 = int(input("Введите ширину для подписи: "))
    height_image1 = int(input("Введите высоту для подписи: "))
    width_image2 = int(input("Введите ширину для печати: "))
    height_image2 = int(input("Введите высоту для печати: "))

    # Диалоговое окно для выбора файла PDF
    pdf_path = filedialog.askopenfilename(title="Выберите PDF-файл", filetypes=[("PDF files", "*.pdf")])

    if pdf_path:
        image1_path = "C:/Users/Super PC/Downloads/Подпись 2.png"
        image2_path = "C:/Users/Super PC/Downloads/печать ГКЗ.png"

        # Основные координаты для страниц PDF
        base_coordinates = {
            2: (70, 70),     # Пример координат для страницы 2
            3: (70, 200),    # Пример координат для страницы 3
        }

        # Генерация дополнительных координат на основе основных страниц
        coordinates = generate_additional_coordinates(base_coordinates)

        overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates)
