import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Quote, Author, Tag


def parse_data():

    url = 'http://quotes.toscrape.com/'

    data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.select('div[class=quote]')
    tags = []
    for el in content:

        quote = el.find('span', attrs={'class': 'text'}).text[1:-1].replace('\n', '')
        name = el.find('small', attrs={'class': 'author'}).text
        about = f"{url}{el.find('a')['href']}"
        tags.append(el.find('div', attrs={'class': 'tags'}).find('meta')['content'].split(','))

        data.append({
            'name': name,
            'quote': quote,
            'about': about,
            'tags': tags
        })

        '''
        author_request = requests.get(about)
        author_soup = BeautifulSoup(author_request.text, 'html.parser')
        author_content = author_soup.select('div[class=author-details]')

        for add_info in author_content:
            author_name = add_info.find('h3').text.split('\n')[0]
        '''

        return data


if __name__ == '__main__':
    store = parse_data()
    print(store)

    engine = create_engine("sqlite:///my_quotes.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for el in store:
        author = Author(name=el.get('name'))
        session.add(author)
    for el in store:
        for tag in el.get('tags'):
            author_tag = Tag(name=tag)
            session.add(author_tag)
    for index, el in enumerate(store):
        print(session.query(Author).filter(Author.name == el.get('name')).one())
        quote = Quote(name=el.get('name'), author_id=session.query(Author)
                      .filter(Author.name == el.get('name')).one().id)
        session.add(quote)

    session.commit()
    session.close()
