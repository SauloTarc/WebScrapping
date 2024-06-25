from functions import save_to_csv, parse_informations, fetch_html

def main():
    url = "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p&nextAction=lnk&exprSearch=ID=039949&format=detailed.pft#1"

    html_content = fetch_html(url)
    
    if html_content:
        soup = parse_informations(html_content)
        
        csv_filename = 'informacoes_filme.csv'
        data = []
        
        labels = soup.find_all('b', class_='label')

        for label in labels:
            categoria = label.get_text(strip=True)
            
            texts = []
            
            next_element = label.find_next_sibling()

            while next_element and (next_element.name != 'b' or 'label' not in next_element.get('class', [])):
                if next_element.name == 'br':
                    next_element = next_element.find_next_sibling()
                    continue
                
                text = next_element.get_text(strip=True)
                if text:
                    texts.append(text)
                
                next_element = next_element.find_next_sibling()

            texto_completo = ' '.join(texts)
            data.append({'Categoria': categoria, 'Nomes': texto_completo.strip()})

        save_to_csv(data, csv_filename)
                
    else:
        print('Não foi possível obter o conteúdo HTML.')

if __name__ == "__main__":
    main()