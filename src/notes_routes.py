from src.models import db, Note
from src.schemas import CreateNoteForm, UpdateNoteForm
from flask import request
from datetime import datetime
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError
import src.utils as utils


@utils.csrf.exempt
def create_note():
    body = CreateNoteForm()

    csrf_token = generate_csrf()
    body.csrf_token.data = csrf_token

    if body.validate_on_submit():
        try:
            note = Note(
                title=body.title.data,
                content=body.content.data,
            )
            if body.category.data:
                note.category = body.category.data

            db.session.add(note)
            db.session.commit()
            return {'status': 'success', 'data': {'note': note.to_dict()}}, 201
        except IntegrityError:
            db.session.rollback()
            return {'status': 'fail', 'message': 'Note with the same title already exists'}, 409

    else:
        return {'status': 'fail', 'errors': body.errors}, 400


@utils.csrf.exempt
def update_note(note_id):
    body = UpdateNoteForm()

    csrf_token = generate_csrf()
    body.csrf_token.data = csrf_token

    if body.validate_on_submit():
        note = Note.query.get(note_id)

        if note:
            if body.title.data:
                note.title = body.title.data
            if body.content.data:
                note.content = body.content.data
            if body.category.data:
                note.category = body.category.data
            if body.published.data:
                note.published = body.published.data

            note.updated_at = datetime.utcnow()
            db.session.commit()

            return {'status': 'success', 'data': {'note': note.to_dict()}}
        else:
            return {"status": "fail", 'message': f'Note with id {note_id} not found'}, 404
    else:
        return {'status': 'fail', 'errors': body.errors}, 400


def get_note(note_id):
    note = Note.query.get(note_id)

    if note:
        return {"status": "success", 'data': {'note': note.to_dict()}}
    else:
        return {"status": "fail", 'message': f'Note with id {note_id} not found'}, 404


@utils.csrf.exempt
def delete_note(note_id):
    note = Note.query.get(note_id)

    if note:
        db.session.delete(note)
        db.session.commit()
        return {'status': 'success', 'message': 'Note deleted successfully'}
    else:
        return {"status": "fail", 'message': f'Note with id {note_id} not found'}, 404


def get_notes():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('limit', default=10, type=int)

    notes = Note.query.paginate(page=page, per_page=per_page, error_out=False)

    note_list = [note.to_dict() for note in notes.items]
    result = {
        'status': 'success',
        'notes': note_list,
        'page': notes.pages,
        'limit': notes.per_page,
        'results': len(note_list)
    }

    return result
