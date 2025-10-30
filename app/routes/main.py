from flask import Blueprint, render_template, request, current_app

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')


@bp.route('/chat/<conversation_id>')
def chat_with_id(conversation_id):
    """Chat interface with a specific conversation"""
    return render_template('index.html', conversation_id=conversation_id)