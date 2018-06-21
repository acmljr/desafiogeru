from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import SignedCookieSessionFactory


def notfound(request):
    return HTTPNotFound('Not found, bro.')


def add_views(config):
    config.add_route('home', '/')
    config.add_route('quotes', '/quotes')
    config.add_route('random_quote', '/quotes/random')
    config.add_route('spec_quote', '/quotes/{quote_number}')


if __name__ == '__main__':
    config = Configurator()
    add_views(config)
    config.add_notfound_view(notfound, append_slash=True)
    config.scan('views')
    my_session_factory = SignedCookieSessionFactory('tantofaz')
    config.set_session_factory(my_session_factory)

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
