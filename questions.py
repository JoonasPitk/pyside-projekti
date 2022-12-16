import html
import random
import requests

API_OSOITE = 'https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple'
VARAKYSYMYKSET = {
    'results': [
        {
            'question': 'Kysymys A',
            'correct_answer': 'Oikea',
            'incorrect_answers': ['Väärä 1', 'Väärä 2', 'Väärä 3'],
        },
        {
            'question': 'Kysymys A',
            'correct_answer': 'Oikea',
            'incorrect_answers': ['Väärä 1', 'Väärä 2', 'Väärä 3'],
        },
        {
            'question': 'Kysymys A',
            'correct_answer': 'Oikea',
            'incorrect_answers': ['Väärä 1', 'Väärä 2', 'Väärä 3'],
        },
    ],
}


def lataa_kysymykset_netista():
    try:
        vastaus = requests.get(API_OSOITE, timeout=0.5)
        tiedot = vastaus.json()
    except requests.exceptions.RequestException:
        tiedot = VARAKYSYMYKSET
    kysymykset_ja_vastaukset = []
    for juttu in tiedot['results']:
        kysymys = juttu['question']
        oikea_vastaus = juttu['correct_answer']
        vaarat_vastaukset = juttu['incorrect_answers']
        vastaukset = ['*' + oikea_vastaus] + vaarat_vastaukset
        random.shuffle(vastaukset)
        tekstit = [
            html.unescape(teksti)
            for teksti in [kysymys] + vastaukset
        ]
        kysymykset_ja_vastaukset.append(tekstit)
    return kysymykset_ja_vastaukset


if __name__ == '__main__':
    import pprint
    pprint.pprint(lataa_kysymykset_netista())
