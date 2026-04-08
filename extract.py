import re
from bs4 import BeautifulSoup

def clean_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # remove all <script> tags
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script'):
        script.decompose()
        
    for template in soup.find_all('template'):
        template.decompose()

    # remove next specific links
    for link in soup.find_all('link'):
        if link.get('href', '').startswith('/_next'):
            link.decompose()
            
    # Add Tailwind CSS CDN
    tailwind_script = soup.new_tag('script')
    tailwind_script['src'] = 'https://cdn.tailwindcss.com'
    soup.head.append(tailwind_script)
    
    # Configure tailwind font
    tailwind_config = soup.new_tag('script')
    tailwind_config.string = "tailwind.config = { theme: { extend: { fontFamily: { sans: ['Inter', 'sans-serif'], } } } }"
    soup.head.append(tailwind_config)
    
    # Add Inter font
    font_link1 = soup.new_tag('link', rel='preconnect', href='https://fonts.googleapis.com')
    font_link2 = soup.new_tag('link', rel='preconnect', href='https://fonts.gstatic.com', crossorigin='')
    font_link3 = soup.new_tag('link', href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap', rel='stylesheet')
    soup.head.append(font_link1)
    soup.head.append(font_link2)
    soup.head.append(font_link3)
    
    # fix images
    for img in soup.find_all('img'):
        if img.get('src') and img['src'].startswith('/'):
            img['src'] = 'https://www.guedesatualizacoes.com' + img['src']
            
    # Fix body styles if any NextJS wrapper
    for div in soup.find_all('div', hidden=True):
        div.decompose()
        
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    clean_html('site.html', 'index.html')
