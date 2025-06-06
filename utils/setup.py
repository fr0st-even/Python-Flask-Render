from flask import Blueprint, request, jsonify
from db_sqlite import query_db, modify_db
import sqlite3

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/like/<int:image_id>', methods=["POST"])
def toggle_like(image_id):
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id es requerido'}), 400
    
    # Verificar que la imagen existe
    image_exists = query_db(
        'SELECT id FROM images WHERE id = ?',
        (image_id,), one=True
    )
    
    if not image_exists:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    # Verificar si el usuario ya dio like
    existing_like = query_db(
        'SELECT id FROM likes WHERE image_id = ? AND user_id = ?',
        (image_id, user_id), one=True
    )
    
    if existing_like:
        # Remover like
        modify_db(
            'DELETE FROM likes WHERE image_id = ? AND user_id = ?',
            (image_id, user_id)
        )
        liked = False
    else:
        # Agregar like
        try:
            modify_db(
                'INSERT INTO likes (image_id, user_id) VALUES (?, ?)',
                (image_id, user_id)
            )
            liked = True
        except sqlite3.IntegrityError:
            # En caso de que se trate de insertar un like duplicado
            return jsonify({'error': 'El like ya existe'}), 400
    
    # Obtener el conteo actual de likes
    likes_count = query_db(
        'SELECT COUNT(*) as count FROM likes WHERE image_id = ?',
        (image_id,), one=True
    )['count']
    
    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    }), 200

@likes_bp.route('/likes/<int:image_id>', methods=["GET"])
def get_likes(image_id):
    # Verificar que la imagen existe
    image_exists = query_db(
        'SELECT id FROM images WHERE id = ?',
        (image_id,), one=True
    )
    
    if not image_exists:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    # Obtener todos los likes de la imagen
    likes = query_db(
        'SELECT user_id FROM likes WHERE image_id = ?',
        (image_id,)
    )
    
    user_ids = [like['user_id'] for like in likes]
    
    return jsonify({
        'likes': user_ids,
        'likes_count': len(user_ids)
    }), 200