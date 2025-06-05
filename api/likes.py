from flask import Blueprint, current_app, request, jsonify
import json

likes_bp = Blueprint('likes', __name__)

def load_db():
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)
    
def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

@likes_bp.route('/like/<int:image_id>', methods=["POST"])
def toggle_like(image_id):
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id es requerido'}), 400
    
    db = load_db()
    
    # Buscar la imagen
    image_found = False
    for image in db['images']:
        if image['id'] == image_id:
            image_found = True
            
            # Inicializar likes si no existe
            if 'likes' not in image:
                image['likes'] = []
            
            # Verificar si el usuario ya dio like
            user_liked = user_id in image['likes']
            
            if user_liked:
                # Remover like
                image['likes'].remove(user_id)
                liked = False
            else:
                # Agregar like
                image['likes'].append(user_id)
                liked = True
            
            save_db(db)
            
            return jsonify({
                'success': True,
                'liked': liked,
                'likes_count': len(image['likes'])
            }), 200
    
    if not image_found:
        return jsonify({'error': 'Imagen no encontrada'}), 404

@likes_bp.route('/likes/<int:image_id>', methods=["GET"])
def get_likes(image_id):
    db = load_db()
    
    for image in db['images']:
        if image['id'] == image_id:
            likes = image.get('likes', [])
            return jsonify({
                'likes': likes,
                'likes_count': len(likes)
            }), 200
    
    return jsonify({'error': 'Imagen no encontrada'}), 404