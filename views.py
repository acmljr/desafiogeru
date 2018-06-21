import random

from pyramid.response import Response
from pyramid.view import view_config

from desafiogeru.python_rest import QuotesAPI
from desafiogeru.DB import Accesses, session_add

quotes = QuotesAPI.QuoteAPI()

@view_config(route_name='home')
def home_view(request):
    session_add(request)
    return Response('<title>Desafio Geru 1.0</title><h1>Alguma coisa '
                    'Qualquer</h1>')


@view_config(route_name='quotes')
@view_config(route_name='spec_quote')
def quotes_view(request):
    session_add(request)
    if 'quote_number' in request.matchdict:
        return Response(quotes.get_quote(request.matchdict['quote_number']))
    items = ''
    for q in quotes.get_quotes():
        items += f'<li>{q}</li>'
    return Response(f'<ul>{items}</ul>')


@view_config(route_name='random_quote')
def random_quote(request):
    session_add(request)
    num = random.randint(0, len(quotes.get_quotes()) - 1)
    return Response(f'Quote number {num}: {quotes.get_quote(num)}')
