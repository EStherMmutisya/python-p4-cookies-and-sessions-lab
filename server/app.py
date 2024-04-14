from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.pop('page_views', None)
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views to 0 if it doesn't exist in session
    page_views = session.get('page_views', 0)
    
    # Increment page_views for each request
    page_views += 1
    session['page_views'] = page_views
    
    # Check if the user has viewed more than 3 pages
    if page_views > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Retrieve the article from the database
    article = Article.query.get_or_404(id)
    
    # Return article data in JSON response
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        # Add other article attributes as needed
    })

if __name__ == '__main__':
    app.run(port=5555)
