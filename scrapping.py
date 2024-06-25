from bs4 import BeautifulSoup
from functions import save_to_csv, parse_informations, fetch_html

def main():
    url = "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p&nextAction=lnk&exprSearch=ID=039949&format=detailed.pft#1"

    html_content = fetch_html(url)
    
    if html_content:
        soup = parse_informations(html_content)
        
        # Preparar para salvar em CSV
        csv_filename = 'informacoes_filme.csv'
        data = []
        categoria = []
        names = []
        
        # Encontrar todas as categorias disponíveis
        labels = soup.find_all('b', class_='label')
        
        for label in labels:
            categoria.append(label.get_text(strip=True))

        for label in labels:
            nomes = label.find_next_sibling('br').find_all_next(string=True)
            nomes = '\n'.join([item.strip() for item in nomes if item.strip()])
            names.append(nomes)
        data.append({'Categoria': categoria, 'Nomes': names})
        
        save_to_csv(data, csv_filename)
                
    else:
        print('Não foi possível obter o conteúdo HTML.')

if __name__ == "__main__":
    main()