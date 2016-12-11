from django.core.management.base import BaseCommand, CommandError
import requests
from django.utils import timezone
from mords_api.models import Book, Entry, Word
from pprint import pprint


class Command(BaseCommand):
    help = 'crawl dictionary data from urban dictionary'

    def handle(self, *args, **options):
        book, created = Book.objects.get_or_create(name='youdao',
                                                   defaults={'update_date': timezone.now()},
                                                   )
        words = Word.objects.filter(is_info_get=False)
        query_times = 0
        for i, word in enumerate(words):
            text = word.text
            url = 'http://fanyi.youdao.com/openapi.do?keyfrom=ZedWord&key=1257551139&type=data&doctype=json&version=1.1&q='
            url += text
            if query_times == 999:
                raise CommandError('Exceeding the hourly query limit of 1000, aborting.')
            r = requests.get(url)
            query_times += 1
            try:
                r.json()["basic"]
            except Exception as e:
                print(e)
                continue
            # pprint(r.json())
            if r.json()["basic"]:
                basic = r.json()["basic"]
                # pprint(basic)

                try:
                    word.us_pho = basic["us-phonetic"]
                except Exception as e:
                    print(e)

                try:
                    word.uk_pho = basic["uk-phonetic"]
                except Exception as e:
                    print(e)

                try:
                    basic["explains"]
                except Exception as e:
                    print(e)
                else:
                    explains = '\n'.join(basic["explains"])
                    try:
                        print(explains)
                    except Exception as e:
                        print(e)
                    entry, e_created = Entry.objects.get_or_create(
                        word=word,
                        book=book,
                        defaults={'update_date': timezone.now(),
                                  'defn': explains
                                  },
                    )

                    if e_created:
                        try:
                            print('Entry ' + entry.word.text + ' created, ' + str(i) + ' of ' + str(len(words)))
                        except Exception as e:
                            print(e)
                    else:
                        entry.defn = explains
                        entry.update_date = timezone.now()
                        entry.save()
                        try:
                            print('Entry ' + entry.word.text + ' updated, ' + str(i) + ' of ' + str(len(words)))
                        except Exception as e:
                            print(e)

                    word.update_date = timezone.now()
                    word.is_info_get = True
                    word.save()
                    book.update_date = timezone.now()
                    book.save()

        self.stdout.write(self.style.SUCCESS('Successfully fetched data from youdao API.'))
