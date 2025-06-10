import os
import subprocess
import re

def update_magnit_url(file_path, new_url):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    updated_content = re.sub(
        r'url = ".*?"',
        f'url = "{new_url}"',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def main():
    links_file = './4834-moloko-syr-yaytsa_links.txt'
    magnit_script = 'magnit.py'
    test_script = 'test.py'
    
    try:
        with open(links_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {links_file} not found.")
        return
    
    for url in urls:
        print(f"Processing URL: {url}")
        
        update_magnit_url(magnit_script, url)
        
        try:
            print("Running magnit.py...")
            result = subprocess.run(['python', magnit_script], capture_output=True, text=True)
            if result.returncode == 0:
                print("magnit.py executed successfully.")
                print(result.stdout)
            else:
                print(f"Error running magnit.py: {result.stderr}")
                continue
        except Exception as e:
            print(f"Exception while running magnit.py: {e}")
            continue
        
        try:
            print("Running test.py...")
            result = subprocess.run(['python', test_script], capture_output=True, text=True)
            if result.returncode == 0:
                print("test.py executed successfully.")
                print(result.stdout)
            else:
                print(f"Error running test.py: {result.stderr}")
        except Exception as e:
            print(f"Exception while running test.py: {e}")
            continue
        
        print("-" * 50)

if __name__ == "__main__":
    main()