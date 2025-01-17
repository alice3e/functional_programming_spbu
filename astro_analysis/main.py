import cv2
import numpy as np
from skimage.measure import label, regionprops
import pandas as pd
import os
import requests
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
from PIL import Image

# Введите ваш API ключ
NASA_API_KEY = '-'  
# Функция для загрузки изображения с NASA API
def download_nasa_image():
    # URL для API запроса
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&count=10'  # Запрашиваем 25 случайных изображений
    response = requests.get(url)
    data = response.json()


    image_paths = []
    for i, item in enumerate(data):
        if 'url' in item and item['url'].endswith('.jpg'):
            image_url = item['url']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            image_path = f'lesson2/images/nasa_image_{i}.png'
            image.save(image_path)
            image_paths.append(image_path)
            print(f"Загружено изображение: {image_path}")

    return image_paths

# Функция для анализа одного изображения и рисования объектов
def analyze_image(image_path):
    print(f"Обработка изображения: {image_path}")

    # Загрузка изображения в градациях серого
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    original_image = cv2.imread(image_path)

    if image is None or original_image is None:
        print(f"Ошибка при загрузке изображения: {image_path}")
        return [], None

    # Бинаризация изображения
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)


    labeled_image = label(binary_image)
    regions = regionprops(labeled_image)

    # Сбор статистики по объектам
    objects_stats = []
    for region in regions:
        # Рассчитываем яркость объекта
        brightness = np.sum(image[region.coords[:, 0], region.coords[:, 1]])

        # Добавляем объект только если его яркость >= 5
        if brightness >= 5:
            stats = {
                'file': os.path.basename(image_path),
                'area': region.area,  # Площадь объекта
                'brightness': brightness,  # Яркость
                'centroid_x': region.centroid[1],  # Координаты центра объекта по оси X
                'centroid_y': region.centroid[0],  # Координаты центра объекта по оси Y
            }
            objects_stats.append(stats)

            # Получаем координаты для рисования прямоугольника
            minr, minc, maxr, maxc = region.bbox
            # Рисуем красный прямоугольник на оригинальном изображении
            cv2.rectangle(original_image, (minc, minr), (maxc, maxr), (0, 0, 255), 2)

    return objects_stats, original_image



def process_single_image(image_path):
    image_stats, annotated_image = analyze_image(image_path)


    if annotated_image is not None:
        output_path = f"lesson2/out/annotated_{os.path.basename(image_path)}"
        cv2.imwrite(output_path, annotated_image)
        print(f"Сохранено изображение с аннотацией: {output_path}")

    return image_stats


# Функция для обработки изображений
def process_images_parallel(image_paths):
    results = []

    # Параллельная обработка изображений с использованием ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        for image_stats in executor.map(process_single_image, image_paths):
            results.extend(image_stats)

    # Конвертация результатов в DataFrame для удобной работы и сохранения
    df = pd.DataFrame(results)
    df.to_csv('lesson2/out/astro_data_stats.csv', index=False)
    print("Сохранение завершено: 'astro_data_stats.csv'")


# Основная функция программы
if __name__ == '__main__':
    # Загружаем изображения с NASA API
    image_paths = download_nasa_image()

    # Проверяем, что изображения найдены
    if not image_paths:
        print("Не удалось загрузить изображения с NASA API.")
    else:
        # Параллельно обрабатываем изображения
        process_images_parallel(image_paths)
