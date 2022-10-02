
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from application.database import get_db
from application.settings import SERVER_HOST, SERVER_PORT

from links.schemas import Link
from links.queries import SQL_INSERT_SHORT_LINK, SQL_INSERT_INTO_HISTORY, \
    SQL_GET_VISITS_FOR_LAST_DAY
from links.model import Link as LinkModel


router = APIRouter()


@router.post(path='/urls/')
def create_short_url(
    link: Link,
    db: Session = Depends(get_db)
):
    if not link.prepare_url():
        raise HTTPException(status_code=400, detail='''It's not a URL''')

    cursor = db.execute(SQL_INSERT_SHORT_LINK, {'long_url': link.long_url})
    record = cursor.fetchone()

    shot_url = record.short_url
    result = f'http://{SERVER_HOST}:{SERVER_PORT}/urls/{shot_url}'

    return result


@router.get(
    path='/urls/{short_url}'
)
def get_orig_url(
    short_url: str,
    db: Session = Depends(get_db)
):

    # TODO подключить redis для более быстрого выбора знаметых ссылок, 
    # добавить алгоритм пометки популярности для уменьшения кол-ва промоха по кешу
    result = db.query(LinkModel).filter(
        LinkModel.short_url == short_url,
        LinkModel.deleted == False
    ).first()
    
    if not result:
        raise HTTPException(status_code=400, detail='URL not found')

    # TODO вынести в селери, чтобы не торимозить клиентскую выдачу данных
    db.execute(SQL_INSERT_INTO_HISTORY, {'link': result.id})

    return RedirectResponse(result.long_url)


@router.get(path='/urls/{short_url}/stats')
def get_stats(
    short_url: str,
    db: Session = Depends(get_db)
):
    result = db.execute(
        SQL_GET_VISITS_FOR_LAST_DAY,
        {'short_url': short_url}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=400, detail='URL not found')

    return result.count


@router.put(path='/urls/{short_url}')
def update_short_url(
    short_url: str,
    new_link: Link,
    db: Session = Depends(get_db)
):
    if not new_link.prepare_url():
        raise HTTPException(status_code=400, detail='''It's not a URL''')

    cur_link: LinkModel = db.query(LinkModel).filter(
        LinkModel.short_url == short_url,
        LinkModel.deleted == False
    ).first()

    if not cur_link:
        raise HTTPException(status_code=400, detail='URL not found')

    cur_link.long_url = new_link.long_url

    return cur_link


@router.delete(path='/urls/{short_url}')
def delete_url(
    short_url: str,
    db: Session = Depends(get_db)
):
    result = db.query(LinkModel).where(
        LinkModel.short_url == short_url,
        LinkModel.deleted == False
    ).update({'deleted': True})

    if result == 0:
        raise HTTPException(status_code=400, detail='URL not found')

    return
