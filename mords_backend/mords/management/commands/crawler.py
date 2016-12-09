from django.core.management.base import BaseCommand, CommandError
import requests
import re
from bs4 import BeautifulSoup
from django.utils import timezone
from mords_api.models import Book, Entry, Word


class Command(BaseCommand):
    help = 'crawl dictionary data from urban dictionary'

    def handle(self, *args, **options):
        # raise CommandError('Poll "%s" does not exist' % poll_id)
        page_num = 1
        words = []
        links = []
        url = 'http://www.urbandictionary.com/yesterday.php'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print (soup.prettify())
        for tag in soup.find_all('a'):
            if 'define' in tag['href']:
                # print(tag.text)
                words.append(tag.text)
                links.append(tag['href'])
            if 'Last' in tag.text:
                page_num = int(tag['href'].split('=')[-1])

        for page in range(2, page_num+1):
            url = 'http://www.urbandictionary.com/yesterday.php'+'?page='+str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            # print (soup.prettify())
            for tag in soup.find_all('a'):
                if 'define' in tag['href']:
                    # print(tag.text)
                    words.append(tag.text)
                    links.append(tag['href'])

        # print(words, links, page_num)
        print(len(words), len(links), page_num)

        base_url = 'http://www.urbandictionary.com/'
        for i in range(0, len(words)):
            r = requests.get(base_url+links[i])
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                meaning = soup('div', {'class': 'meaning'})[0].text
                example = soup('div', {'class': 'example'})[0].text
            except Exception as e:
                print(e)
                meaning = ''
                example = ''

            try:
                meaning = meaning.decode('utf-8').replace('\n', '').replace('\r', '').encode('utf-8')
            except Exception as e:
                print(e)
            try:
                example = example.decode('utf-8').replace('\n', '').replace('\r', '').encode('utf-8')
            except Exception as e:
                print(e)

            # print(words[i], meaning, example)

            book, created = Book.objects.get_or_create(name='urban_dic_new')
            word, created = Word.objects.get_or_create(text=words[i],
                                                       defaults={'update_date': timezone.now()},
                                                       )
            entry, e_created = Entry.objects.get_or_create(
                word=word,
                defn=meaning,
                exmp=example,
                book=book,
                defaults={'update_date': timezone.now()},
            )

            if e_created:
                print('Entry '+entry.word.text+' created, '+str(i)+' of '+str(len(words)))
            else:
                print('Entry '+entry.word.text+' updated, '+str(i)+' of '+str(len(words)))

        book, created = Book.objects.get_or_create(name='urban_dic_new')
        book.update_date = timezone.now()
        book.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated vocabulary book: urban_dic_new'))