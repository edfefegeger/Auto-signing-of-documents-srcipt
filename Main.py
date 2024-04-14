import os
import PyPDF2
from PIL import Image
from io import BytesIO
from tkinter import Tk, filedialog
import random

def overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates, width_image1, height_image1, width_image1_1, height_image1_1, width_image2, height_image2):
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
            image1_resized = resize_image(image1, new_width=width_image1, new_height=height_image1)
            image1_1_resized = resize_image(image1, new_width=width_image1_1, new_height=height_image1_1)
            image2_resized = resize_image(image2, new_width=width_image2, new_height=height_image2)
            image2_2_resized = resize_image(image2, new_width=width_image2_2, new_height=height_image2_2)

            # Применяем случайные изменения к первому изображению
            image1_resized = apply_random_transforms(image1_resized)
            image1_1_resized = apply_random_transforms(image1_1_resized)

            # Применяем случайные изменения ко второму изображению
            image2_resized = apply_random_transforms2(image2_resized)
            image2_2_resized = apply_random_transforms2(image2_2_resized)

            # Преобразуем изображения в PDF страницы для наложения
            image1_pdf = image_to_pdf(image1_resized)
            image1_1_pdf = image_to_pdf(image1_1_resized)
            image2_pdf = image_to_pdf(image2_resized)
            image2_2_pdf = image_to_pdf(image2_2_resized)

            # Наложение первого изображения по указанным координатам
            page.mergeTranslatedPage(image1_pdf.getPage(0), x, y)

            # Наложение второго изображения по координатам
            if i + 1 in coordinates:
                page.mergeTranslatedPage(image2_pdf.getPage(0), x, y)

            # Наложение дополнительных изображений по координатам вида "страница_1"
            if f"{i + 1}_1" in coordinates:
                x_additional, y_additional = coordinates[f"{i + 1}_1"]
                page.mergeTranslatedPage(image1_1_pdf.getPage(0), x_additional, y_additional)
                page.mergeTranslatedPage(image2_2_pdf.getPage(0), x_additional, y_additional)

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

def apply_random_transforms(image):
    # Случайные параметры для изменения изображения
    rotation_angle = random.randint(rotation_angle1, rotation_angle2)  # Случайный угол поворота (-10 градусов до 10 градусов)
    scale_factor_horizontal = random.uniform(scale_factor_horizontal1, scale_factor_horizontal2)   # Случайный масштаб по горизонтали (от 80% до 120%)
    scale_factor_vertical = random.uniform(scale_factor_vertical1, scale_factor_vertical2)   # Случайный масштаб по вертикали (от 80% до 120%)

    # Масштабирование изображения по горизонтали и вертикали
    new_width = int(image.width * scale_factor_horizontal)
    new_height = int(image.height * scale_factor_vertical)
    resized_image = image.resize((new_width, new_height), resample=Image.BICUBIC)

    # Поворот изображения после масштабирования
    rotated_image = resized_image.rotate(rotation_angle, expand=True, resample=Image.BICUBIC)

    return rotated_image





def apply_random_transforms2(image):
    # Случайные параметры для изменения изображения
    rotation_angle = random.randint(rotation_angle1_1, rotation_angle2_2)  # Случайный угол поворота (-10 градусов до 10 градусов)
    scale_factor = random.uniform(0.8, 1.2)   # Случайный масштаб (от 0.8 до 1.2)

    # Применяем поворот и масштабирование к изображению
    image = image.rotate(rotation_angle, resample=Image.BICUBIC)

    return image

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

    # Запрос пользовательских параметров для изображений
    width_image1 = int(input("Введите ширину для подписи: "))
    height_image1 = int(input("Введите высоту для подписи: "))
    width_image1_1 = int(input("Введите ширину для второй подписи: "))
    height_image1_1 = int(input("Введите высоту для второй подписи: "))
    width_image2 = int(input("Введите ширину для печати: "))
    height_image2 = int(input("Введите высоту для печати: "))
    width_image2_2 = int(input("Введите ширину для второй печати: "))
    height_image2_2 = int(input("Введите высоту для второй печати: "))

    coordinates1 = int(input("Введите кординаты для страницы 2 (1): "))
    coordinates1_1 = int(input("Введите кординаты для страницы 2 (2): "))
    coordinates2 = int(input("Введите кординаты для страницы 3 (1): "))
    coordinates2_2 = int(input("Введите кординаты для страницы 3 (2): "))


    rotation_angle1 = int(input("Введите первую точку диапазона случайного вращения для подписи (Пример: -10): "))
    rotation_angle2 = int(input("Введите вторую точку диапазона случайного вращения для подписи (Пример: 10): "))
    scale_factor_horizontal1 = float(input("Введите первую точку случайного масштаба по горизонтали для подписи. Пример: 0.8 (от 80%): "))
    scale_factor_horizontal2 = float(input("Введите вторую точку случайного масштаба по горизонтали для подписи. Пример: 1.2 (до 120%): "))
    scale_factor_vertical1 = float(input("Введите первую точку случайного масштаба по вертикали для подписи. Пример: 0.8 (от 80%): "))
    scale_factor_vertical2 = float(input("Введите вторую точку случайного масштаба по вертикали для подписи. Пример: 1.2 (до 120%): "))

    rotation_angle1_1 = int(input("Введите первую точку диапазона случайного вращения для печати (Пример: -10): "))
    rotation_angle2_2 = int(input("Введите вторую точку диапазона случайного вращения для печати (Пример: 10): "))

    # Диалоговое окно для выбора файла PDF
    pdf_path = filedialog.askopenfilename(title="Выберите PDF-файл", filetypes=[("PDF files", "*.pdf")])

    if pdf_path:
        image1_path = filedialog.askopenfilename(title="Выберите файл с подписью")
        image2_path = filedialog.askopenfilename(title="Выберите файл с печатью")

        # Основные координаты для страниц PDF
        base_coordinates = {}

        # Заполняем словарь base_coordinates до страницы 1000 с шагом 3
        for page_number in range(2, 1001, 3):
            if page_number + 1 <= 1000:
                base_coordinates[page_number] = (coordinates1, coordinates1_1)  # Для страницы подписи
                base_coordinates[page_number + 1] = (coordinates2, coordinates2_2)  # Для страницы печати

        # Генерация дополнительных координат на основе основных страниц
        coordinates = generate_additional_coordinates(base_coordinates)
        print('Обработка...')
        overlay_images_on_pdf(pdf_path, image1_path, image2_path, coordinates, width_image1, height_image1, width_image1_1, height_image1_1, width_image2, height_image2)
        print("Документ обработан")
        

        # Наложение изображений на PDF

#Введите ширину для подписи: 300
#Введите высоту для подписи: 120
#Введите ширину для второй подписи: 300
#Введите высоту для второй подписи: 120
#Введите ширину для печати: 150
#Введите высоту для печати: 150
#Введите ширину для второй печати: 150
#Введите высоту для второй печати: 150

#2: (70, 70),  
#3: (70, 200)

    #rotation_angle = random.randint(-10, 10)  # Случайный угол поворота (-10 градусов до 10 градусов)
    #scale_factor_horizontal = random.uniform(0.8, 1.2)   # Случайный масштаб по горизонтали (от 80% до 120%)
    #scale_factor_vertical = random.uniform(0.8, 1.2)   # Случайный масштаб по вертикали (от 80% до 120%)