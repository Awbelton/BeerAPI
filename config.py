from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import beer, user, review, time, datetime

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser(bundle_errors=True)

# Validation to ensure beer/user/review exists
def error(_id, sel):
    if sel == 1:
        if _id not in BEER.keys():
            abort(404, message="Beer {} is not in the database".format(_id))
    if sel == 2:
        if _id not in USERS.keys():
            abort(404, message="User {} is not in the database".format(_id))
    if sel == 3:
        if _id not in REVIEWS.keys():
            abort(404, message="Review {} is not in the database".format(_id))

# Dict to hold all values (for formatting)
BEER = {}
USERS = {}
REVIEWS = {}

# Populate dicts above with db
for i in beer.getBeers(0, 2):
    BEER[i[0]] = {'IBU': i[1], 'Calories': i[2], 'ABV': i[3], 'Brewery': i[4], 'Style': i[5],
                  'UID': i[6], 'Date': str(i[7]), 'Reviews': [{'Aroma': i[1], 'Appearance': i[2], 
                  'Taste': i[3], 'Overall': i[4], 'User': i[5]} for i in beer.getReviews(i[0])]}
for i in user.getUsers(0, 2):
    USERS[i[0]] = {'Username': i[1], 'Password': i[2]}
for i in review.getReviews(0, 2):
    REVIEWS[i[0]] = {'UID': i[1], 'Beer': i[2], 'Aroma': i[3], 'Appearance': i[4],
                     'Taste': i[5], 'Overall': i[6]}

# Beer Classes
class Beer(Resource):
    # REST methods
    def get(self, beer_id):
        error(beer_id, 1)
        return BEER[beer_id]

    def delete(self, beer_id):
        error(beer_id, 1)
        beer.delBeer(beer_id)
        del BEER[beer_id]
        return '', 204

    def put(self, beer_id):
        error(beer_id, 1)

        # Get current values
        vals = [i for i in beer.getBeers(beer_id, 1)[1:6]]

        # parser arguments
        parser.add_argument('ibu', type=str, required=False)
        parser.add_argument('calories', type=int, required=False)
        parser.add_argument('abv', type=str, required=False)
        parser.add_argument('brewery', type=str, required=False)
        parser.add_argument('style', type=str, required=False)
        args = parser.parse_args()
        newVals = [args['ibu'], args['calories'], args['abv'], args['brewery'], args['style']]

        # Check for updates
        for i in range(len(newVals)):
            if newVals[i] != None:
                vals[i] = newVals[i]

        # Update db
        details = (vals[0], vals[1], vals[2], vals[3], vals[4], beer_id)
        beer.updateBeer(details)

        # Update BEER dict
        BEER[beer_id] = {'IBU': vals[0], 'Calories': vals[1], 'ABV': vals[2],
                         'Brewery': vals[3], 'Style': vals[4]}

        # Remove arguments from parser
        parser.remove_argument('ibu')
        parser.remove_argument('calories')
        parser.remove_argument('abv')
        parser.remove_argument('brewery')
        parser.remove_argument('style')

        return BEER[beer_id], 201


class BeerList(Resource):
    def get(self):
        return BEER

    def post(self):
        # parser arguments
        parser.add_argument('uid', type=str, required=True)
        parser.add_argument('ibu', type=str, required=True)
        parser.add_argument('calories', type=int, required=True)
        parser.add_argument('abv', type=str, required=True)
        parser.add_argument('brewery', type=str, required=True)
        parser.add_argument('style', type=str, required=True)
        args = parser.parse_args()

        # Get timestamp of addition
        current_time = time.time()
        current_timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

        # Validate user & beer
        userExists = user.getUsers(args['uid'], 1)
        added_beer = beer.checkAdd(args['uid'])

        if userExists == None:
            return {"Message": "User does not exist."}
        if added_beer != None:
            return {"Message": "User has already added a beer today."}

        # Increment id
        self.beer_id = beer.getAmt()+1

        # Add new beer to DB
        details = (self.beer_id, args['ibu'], args['calories'], args['abv'], args['brewery'],
                   args['style'], args['uid'], current_timestamp)
        beer.addBeer(details)

        # Add to BEER dict
        BEER[int(self.beer_id)] = {'IBU': args['ibu'], 'Calories': args['calories'], 'ABV': args['abv'],
                         'Brewery': args['brewery'], 'Style': args['style'], 'UID': args['uid'],
                         'Date': str(current_timestamp)}

        # Remove arguments from parser
        parser.remove_argument('uid')
        parser.remove_argument('ibu')
        parser.remove_argument('calories')
        parser.remove_argument('abv')
        parser.remove_argument('brewery')
        parser.remove_argument('style')

        return BEER[self.beer_id], 201


# User Classes
class User(Resource):
    # REST methods
    def get(self, uid):
        error(uid, 2)
        return USERS[uid]

class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        # parser arguments
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('pw', type=str, required=True)
        args = parser.parse_args()

        # Increment id
        self.user_id = user.getAmt()+1

        # Add to db
        details = (self.user_id, args['user'], args['pw'])
        user.addUser(details)

        # Add to USERS dict
        USERS[int(self.user_id)] = {'Username': args['user'], 'Password': args['pw']}

        # Remove arguments from parser
        parser.remove_argument('user')
        parser.remove_argument('pw')

        return USERS[self.user_id], 201

# Review Classes
class Review(Resource):
    # REST methods
    def get(self, rid):
        error(rid, 3)
        return REVIEWS[rid]

    def delete(self, rid):
        error(rid, 3)
        review.delReview(rid)
        del REVIEWS[rid]
        return '', 204

    def put(self, rid):
        error(rid, 3)

        # Get current values
        vals = [i for i in review.getReviews(rid, 1)[3:6]]

        # parser arguments
        parser.add_argument('uid', type=int, required=True)
        parser.add_argument('beerid', type=int, required=True)
        parser.add_argument('aroma', type=int, required=False)
        parser.add_argument('appearance', type=int, required=False)
        parser.add_argument('taste', type=int, required=False)
        args = parser.parse_args()
        newVals = [args['aroma'], args['appearance'], args['taste']]

        # Check for updates
        for i in range(len(newVals)):
            if newVals[i] != None:
                vals[i] = newVals[i]

        self.overall = vals[0] + vals[1] + vals[2]

        details = (rid, vals[0],
                   vals[1], vals[2], self.overall)
        review.updateReview(details)
        REVIEWS[int(rid)] = {'UID': args['uid'], 'Beer': args['beerid'],
                                   'Aroma': vals[0], 'Appearance': vals[1],
                                   'Taste': vals[2], 'Overall': self.overall}

        # Remove arguments from parser
        parser.remove_argument('uid')
        parser.remove_argument('beerid')
        parser.remove_argument('aroma')
        parser.remove_argument('appearance')
        parser.remove_argument('taste')
        
        return REVIEWS[rid], 201

class ReviewList(Resource):
    def get(self):
        return REVIEWS

    def post(self):
        # parser arguments
        parser.add_argument('uid', type=int, required=True)
        parser.add_argument('beerid', type=int, required=True)
        parser.add_argument('aroma', type=int, required=True)
        parser.add_argument('appearance', type=int, required=True)
        parser.add_argument('taste', type=int, required=True)
        args = parser.parse_args()

        # Validate aroma, appearance, and taste
        if int(args['aroma']) > 5 or int(args['appearance']) > 5 or int(args['taste']) > 10:
            return {"Message": "Invalid value for aroma, appearance, or taste"}

        # Validate user & beer
        userExists = user.getUsers(args['uid'], 1)
        beerExists = beer.getBeers(args['beerid'], 1)

        if userExists == None or beerExists == None:
            return {"Message": "User or Beer does not exist."}

        # Increment id
        self.review_id = review.getAmt() + 1

        # Calculate overall score
        self.overall = int(args['aroma']) + int(args['appearance']) + int(args['taste'])

        # Add to DB
        details = (self.review_id, args['uid'], args['beerid'], args['aroma'],
                   args['appearance'], args['taste'], self.overall)
        review.addReview(details)

        # Add to REVIEWS dict
        REVIEWS[int(self.review_id)] = {'UID': args['uid'], 'Beer': args['beerid'],
                                   'Aroma': args['aroma'], 'Appearance': args['appearance'],
                                   'Taste': args['taste'], 'Overall': self.overall}

        # Add Review to BEERS dict
        BEER[int(args['beerid'])]['Reviews'].append({'Aroma': args['aroma'], 'Appearance': args['appearance'], 
                                                'Taste': args['taste'], 'Overall': self.overall, 'User': args['uid']})

        # Remove arguments from parser
        parser.remove_argument('uid')
        parser.remove_argument('beerid')
        parser.remove_argument('aroma')
        parser.remove_argument('appearance')
        parser.remove_argument('taste')

        return REVIEWS[self.review_id], 201

# Routes
api.add_resource(BeerList, '/beer')
api.add_resource(Beer, '/beer/<int:beer_id>')
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<int:uid>')
api.add_resource(ReviewList, '/review')
api.add_resource(Review, '/review/<int:rid>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
