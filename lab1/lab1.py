import csv
import random
import statistics
from concurrent.futures import ThreadPoolExecutor
import os

def generate_csv_files():
    print("Генерация CSV файлов...\n")
    
    for i in range(1, 6):
        filename = f'data_{i}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Category', 'Value'])
            
            for _ in range(20):
                category = random.choice(['A', 'B', 'C', 'D'])
                
                value = round(random.uniform(1, 100), 2)
                
                writer.writerow([category, value])
        
        print(f"Создан файл: {filename}")

def process_file(filename):
    data = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            category = row[0]
            value = float(row[1])
            
            if category not in data:
                data[category] = []
            
            data[category].append(value)
    
    results = {}
    
    for category, values in data.items():
        median = statistics.median(values)
        
        if len(values) > 1:
            std_dev = statistics.stdev(values)
        else:
            std_dev = 0.0
        
        results[category] = {
            'median': round(median, 2),
            'std_dev': round(std_dev, 2)
        }
    
    return filename, results

def process_all_files():
    print("\n" + "="*60)
    print("ОБРАБОТКА ФАЙЛОВ")
    print("="*60 + "\n")
    
    files = [f'data_{i}.csv' for i in range(1, 6)]

    all_medians = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_file, files))
    
    for filename, file_results in results:
        print(f"{filename}:")
        
        for category in sorted(file_results.keys()):
            median = file_results[category]['median']
            std_dev = file_results[category]['std_dev']
            print(f"  {category}, медиана: {median}, отклонение: {std_dev}")
            all_medians.append(median)
        
        print()
    
    if all_medians:
        median_of_medians = statistics.median(all_medians)
        if len(all_medians) > 1:
            std_dev_of_medians = statistics.stdev(all_medians)
        else:
            std_dev_of_medians = 0.0
        print("="*60)
        print(f"Медиана медиан: {round(median_of_medians, 2)}")
        print(f"Отклонение медиан: {round(std_dev_of_medians, 2)}")
        print("="*60)

def main():
    generate_csv_files()
    
    process_all_files()

if __name__ == "__main__":
    main()
