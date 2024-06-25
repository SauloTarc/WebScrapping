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
        
        # Encontrar todas as categorias disponíveis
        labels = soup.find_all('b', class_='label')
        
        for label in labels:
            categoria = label.get_text(strip=True)
            next_element = label.find_next_sibling()

            if next_element.name == 'br':
                informacoes = next_element.find_next_sibling(string=True)
                if informacoes:
                    informacoes = informacoes.strip()
                else:
                    informacoes = ""
            else:
                informacoes = ""

            data.append({'Categoria': categoria, 'Nomes': informacoes})
        
        save_to_csv(data, csv_filename)
    else:
        print('Não foi possível obter o conteúdo HTML.')

if __name__ == "__main__":
    main()