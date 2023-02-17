from flask import Flask, request, jsonify
from flask_cors import CORS
from config import db, SECRET_KEY
from os import path, getcwd, environ
from dotenv import load_dotenv
from models.user import User
from models.projects import Projects
from models.experiences import Experiences
from models.certification import Certification
from models.skills import Skills
from models.personalDetails import PersonalDetails
from models.education import Education

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.secret_key = SECRET_KEY

    db.init_app(app)
    print("DB Initialized Successfully")

    with app.app_context():
        @app.route("/signup",methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)
            new_user = User(
                username = data['username']
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify(msg = "user added successfully")
        
        @app.route("/add_personal_details",methods=['POST'])
        def add_personal_details():
            username = request.args.get('username')
            user = User.query.filter_by(username = username).first()

            personal_data = request.get_json()

            new_personal_details = PersonalDetails(
            name= personal_data['name'],
            email = personal_data['email'],
            phone = personal_data['phone'],
            address = personal_data['address'],
            linkedin_url=personal_data['linkedin_url'],
            user_id=user.id
            )

            db.session.add(new_personal_details)
            db.session.commit()
            return jsonify(msg="Personal details added successfully")

        @app.route("/add_project", methods=['POST'])
        def add_project():
            recv_username= request.args.get('username')
            user= User.query.filter_by(username=recv_username).first()

            project_data= request.get_json()
            for data in project_data["data"]:
                new_project= Projects(
                    name= data['name'],
                    desc= data['description'],
                    start_date= data['start_date'],
                    end_date= data['end_date'],
                    user_id= user.id
            )
            
            db.session.add(new_project)
            db.session.commit()
            return jsonify(msg = "Project added successfully")

        @app.route("/experience", methods=['POST'])
        def experience():
            recv_username= request.args.get('username')
            user= User.query.filter_by(username=recv_username).first()

            experience_data= request.get_json()
            for data in experience_data["data"]:
                new_experience= Experiences(
                    company_name= data['name'],
                    role_desc= data['description'],
                    start_date= data['start_date'],
                    end_date= data['end_date'],
                    user_id= user.id
            )
            
            db.session.add(new_experience)
            db.session.commit()
            return jsonify(msg = "Experience added successfully")

        @app.route("/add_skills", methods=['POST'])
        def add_skills():
            recv_username= request.args.get('username')
            user= User.query.filter_by(username=recv_username).first()

            skills_data= request.get_json()
            for data in skills_data["data"]:
                new_skills= Skills(
                    name= data['name'],
                    desc= data['description'],
                    start_date= data['start_date'],
                    end_date= data['end_date'],
                    user_id= user.id
            )
            
            db.session.add(new_skills)
            db.session.commit()
            return jsonify(msg = "Skills added successfully")

        @app.route("/education", methods=['POST'])
        def education():
            recv_username= request.args.get('username')
            user= User.query.filter_by(username=recv_username).first()

            education_data= request.get_json()
            for data in education_data["data"]:
                new_education= Education(
                    school_name= data['name'],
                    degree_name= data['description'],
                    start_date= data['start_date'],
                    end_date= data['end_date'],
                    user_id= user.id
                )
                db.session.add(new_education)
                db.session.commit()
            return jsonify(msg = "Education added successfully")


        @app.route("/get_resume_project", methods=['GET'])
        def get_resume_project():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()

            personal_details = PersonalDetails.query.filter_by(user_id=user.id).first()
            experiences = Experiences.query.filter_by(user_id=user.id).all()
            projects = Projects.query.filter_by(user_id=user.id).all()
            educations = Education.query.filter_by(user_id=user.id).all()
            certificates = Certification.query.filter_by(user_id=user.id).all()
            skills = Skills.query.filter_by(user_id=user.id).all()

            resume_data = {
                "name": personal_details.name,
                "email": personal_details.email,
                "phone": personal_details.phone,
                "address": personal_details.address,
                "linkedin_url": personal_details.linkedin_url
            }

            experiences_data = []
            projects_data = []
            educations_data = []
            certificates_data = []
            skills_data = []

            #* Experiences
            for exp in experiences:
                experiences_data.append(
                    {
                        "company_name": exp.company_name,
                        "role": exp.role,
                        "role_desc": exp.role_desc,
                        "start_date": exp.start_date,
                        "end_date": exp.end_date
                    }
                )

            resume_data["experiences"] = experiences_data




        #db.drop_all()
        db.create_all()
        db.session.commit()

        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
