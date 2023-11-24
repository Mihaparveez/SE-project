from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"Book(name={self.name}, author={self.author}, year={self.year})"

#db.create_all()

books={}

book_put_args = reqparse.RequestParser()
book_put_args.add_argument("name",type=str,help="Name of the Book required", required=True)
book_put_args.add_argument("author",type=str,help="Author of the Book required", required=True)
book_put_args.add_argument("year",type=int,help="Publish year of the Book required", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("name",type=str,help="Name of the Book required")
book_update_args.add_argument("author",type=str,help="Author of the Book required")
book_update_args.add_argument("year",type=int,help="Publish year of the Book required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'author':fields.String,
    'year':fields.Integer
}

class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result= BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Could not find book with that Id..")
        return result
    
    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        result= BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, message="Book Id taken..")
        book = BookModel(id=book_id,name=args['name'], author=args['author'], year=args['year'])
        db.session.add(book)
        db.session.commit()
        return book, 201
    
    @marshal_with(resource_fields)
    def patch(self, book_id):
        args = book_update_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Book doesn't exist, cannot update")

        if args['name']:
            result.name=args['name']
        if args['author']:
            result.author=args['author']
        if args['year']:
            result.year = args['year']

        db.session.commit()
        return result
    
    def delete(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Book doesn't exist, cannot delete")

        db.session.delete(result)
        db.session.commit()
        return '', 204
    
    # def delete(self, book_id):
    #     abort_not_exist(book_id)
    #     del books[book_id]
    #     return '', 204
    
api.add_resource(Book,"/book/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)