from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import URLForm
import requests
from bs4 import BeautifulSoup

def scrape_view(request):
    data = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract tables
                tables = soup.find_all('table')
                table_data = []
                for table in tables:
                    headers = [header.text for header in table.find_all('th')]
                    rows = []
                    for row in table.find_all('tr'):
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]
                        rows.append(cols)
                    table_data.append({'headers': headers, 'rows': rows})

                # Extract images
                images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
                
                data = {'tables': table_data, 'images': images}
            except requests.RequestException as e:
                form.add_error('url', f'Error fetching the URL: {e}')
    else:
        form = URLForm()

    return render(request, 'scraper/scrape.html', {'form': form, 'data': data})
