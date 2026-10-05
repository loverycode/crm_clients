from django.http import HttpResponse


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{title}</title>
            <link rel="stylesheet" href="{bootstrap}">
        </head>
        <body>
            <nav class="navbar navbar-expand bg-light mb-4">
                <div class="container">
                    <a class="navbar-brand" href="/">CRM</a>
                    <a class="nav-link d-inline" href="/clients/">Клиенты</a>
                    <a class="nav-link d-inline" href="/deals/">Сделки</a>
                </div>
            </nav>
            <main class="container">{content}</main>
        </body>
        </html>"""


def index(requect):
    content = """
    <h1 class="display-4">CRM</h1>
        <p class="lead">
            Учёт клиентов, менеджеров, контактов и сделок.
        </p>
        <p>Основные разделы:</p>
        <a href="/clients/" class="btn btn-primary me-2">Клиенты</a>
        <a href="/deals/" class="btn btn-secondary">Сделки</a>
    """
    return HttpResponse(page('CRM', content))
