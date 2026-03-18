import pandas as pd

# Попробуем прочитать файл
try:
    df = pd.read_excel('data/operations.xlsx')
    print("Файл успешно прочитан!")
    print(f"Количество строк: {len(df)}")
    print(f"Количество колонок: {len(df.columns)}")
    print(f"Названия колонок: {list(df.columns)}")
    print("\nПервые 5 строк:")
    print(df.head())
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
