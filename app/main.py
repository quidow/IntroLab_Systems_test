from utils import get_download_link, download_file, get_news, write_news_to_file

if __name__ == "__main__":
    with open('companies.txt') as file:
        for line in file:
            company = line.strip()
            download_link = get_download_link(company)
            if not download_link:
                print(f'Company {company} was not found!')
                continue
            download_file(company, download_link)
            news = get_news(company)
            write_news_to_file(company, news)
