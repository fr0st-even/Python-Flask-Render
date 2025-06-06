from flask import Blueprint, request, jsonify
import base64
from db_sqlite import query_db, modify_db

images_bp = Blueprint('images', __name__)

@images_bp.route('/images', methods=["GET"])
def get_images():
    # Obtener todas las imágenes con información del usuario
    images = query_db('''
        SELECT 
            i.id,
            i.user_id,
            i.filename,
            i.filedata,
            i.created_at,
            u.username
        FROM images i
        JOIN users u ON i.user_id = u.id
        ORDER BY i.created_at DESC
    ''')
    
    # Convertir a lista de diccionarios y agregar comentarios y likes
    result = []
    for image in images:
        image_dict = dict(image)
        
        # Obtener comentarios para esta imagen
        comments = query_db('''
            SELECT 
                c.text,
                c.user_id,
                u.username,
                c.created_at
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.image_id = ?
            ORDER BY c.created_at ASC
        ''', (image['id'],))
        
        image_dict['comments'] = [dict(comment) for comment in comments]
        
        # Obtener likes para esta imagen
        likes = query_db('''
            SELECT user_id FROM likes WHERE image_id = ?
        ''', (image['id'],))
        
        image_dict['likes'] = [like['user_id'] for like in likes]
        
        result.append(image_dict)
    
    return jsonify(result)

@images_bp.route('/upload', methods=["POST"])
def upload():
    user_id = request.form['user_id']
    file = request.files['image']
    
    if file:
        file_data = file.read()  # Leyendo como binario
        encoded_data = base64.b64encode(file_data).decode('utf-8')

        # Insertar imagen en la base de datos
        image_id = modify_db('''
            INSERT INTO images (user_id, filename, filedata) 
            VALUES (?, ?, ?)
        ''', (int(user_id), file.filename, encoded_data))
        
        return jsonify({
            'message': 'Imagen subida',
            'image_id': image_id
        }), 201
    
    return jsonify({'error': 'No se recibió la imagen'}), 400