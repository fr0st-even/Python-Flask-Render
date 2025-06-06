from flask import Blueprint, request, jsonify
from db_sqlite import query_db, modify_db

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/comment/<int:image_id>', methods=["POST"])
def add_comment(image_id):
    data = request.json  # Trae el user_id y el text
    
    # Verificar que la imagen existe
    image_exists = query_db(
        'SELECT id FROM images WHERE id = ?',
        (image_id,), one=True
    )
    
    if not image_exists:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    # Verificar que el usuario existe
    user_exists = query_db(
        'SELECT id FROM users WHERE id = ?',
        (data["user_id"],), one=True
    )
    
    if not user_exists:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Insertar comentario
    comment_id = modify_db('''
        INSERT INTO comments (image_id, user_id, text) 
        VALUES (?, ?, ?)
    ''', (image_id, data["user_id"], data["comment"]))
    
    # Obtener el comentario insertado con información del usuario
    new_comment = query_db('''
        SELECT 
            c.id,
            c.text,
            c.user_id,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
    ''', (comment_id,), one=True)
    
    return jsonify({
        'message': 'Comentario agregado',
        'comment': dict(new_comment)
    }), 201

@comments_bp.route('/comments/<int:image_id>', methods=["GET"])
def get_comments(image_id):
    # Obtener todos los comentarios de una imagen
    comments = query_db('''
        SELECT 
            c.id,
            c.text,
            c.user_id,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.image_id = ?
        ORDER BY c.created_at ASC
    ''', (image_id,))
    
    return jsonify([dict(comment) for comment in comments])