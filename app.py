from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение моделей базы данных
class Ranks(db.Model):
    __tablename__ = 'ranks'
    id = db.Column(db.Integer, primary_key=True)
    Kindom = db.Column(db.String(50), nullable=False)
    Phylum = db.Column(db.String(50), nullable=False)
    Class = db.Column(db.String(50), nullable=False)
    Order = db.Column(db.String(50), nullable=False)
    Family = db.Column(db.String(50), nullable=False)
    Genus = db.Column(db.String(50), nullable=False)
    Species = db.Column(db.String(50), nullable=False)

class Cultivation_Methods(db.Model):
    __tablename__ = 'cultivation_methods'
    id = db.Column(db.Integer, primary_key=True)
    Culture_Medium = db.Column(db.String(50), nullable=False)
    Growth_Temperature = db.Column(db.String(50), nullable=False)
    Cultivation_Time = db.Column(db.String(50), nullable=False)

class Genomic_Data(db.Model):
    __tablename__ = 'genomic_data'
    id = db.Column(db.Integer, primary_key=True)
    Genomic_Sequence = db.Column(db.String(50), nullable=False)
    Sequence_File_Name = db.Column(db.String(50), nullable=False)

class General_Info(db.Model):
    __tablename__ = 'general_info'
    id = db.Column(db.Integer, primary_key=True)
    id_taxonomy = db.Column(db.Integer, db.ForeignKey('ranks.id'), nullable=False)
    id_Cultivation_Methods = db.Column(db.Integer, db.ForeignKey('cultivation_methods.id'), nullable=False)
    id_Genomic_Data = db.Column(db.Integer, db.ForeignKey('genomic_data.id'), nullable=False)
    Organization = db.Column(db.String(50), nullable=False)
    Collection_Number = db.Column(db.String(50), nullable=False)
    Isolation_Date = db.Column(db.DateTime, nullable=False)
    Isolation_Place = db.Column(db.String(50), nullable=False)
    Isolation_Source = db.Column(db.String(50), nullable=False)

    # Определение связей между таблицами
    taxonomy = db.relationship('Ranks', backref=db.backref('general_infos', lazy=True))
    cultivation_methods = db.relationship('Cultivation_Methods', backref=db.backref('general_infos', lazy=True))
    genomic_data = db.relationship('Genomic_Data', backref=db.backref('general_infos', lazy=True))

def create_tables():
    db.create_all()

# Определение маршрутов приложения
@app.route('/')
def index():
    ranks = Ranks.query.all()
    methods = Cultivation_Methods.query.all()
    genomic_data = Genomic_Data.query.all()
    general_info = General_Info.query.all()
    return render_template('index.html', ranks=ranks, methods=methods, genomic_data=genomic_data, general_info=general_info)

@app.route('/ranks')
def ranks():
    ranks = Ranks.query.all()
    return render_template('ranks.html', ranks=ranks)

@app.route('/new_rank', methods=['GET', 'POST'])
def new_rank():
    if request.method == 'POST':
        kindom = request.form['Kindom']
        phylum = request.form['Phylum']
        class_ = request.form['Class']
        order = request.form['Order']
        family = request.form['Family']
        genus = request.form['Genus']
        species = request.form['Species']

        new_rank = Ranks(Kindom=kindom, Phylum=phylum, Class=class_, Order=order, Family=family, Genus=genus, Species=species)
        db.session.add(new_rank)
        db.session.commit()

        return redirect(url_for('ranks'))

    return render_template('new_rank.html')

@app.route('/cultivation_methods')
def cultivation_methods():
    methods = Cultivation_Methods.query.all()
    return render_template('cultivation_methods.html', methods=methods)

@app.route('/new_cultivation_method', methods=['GET', 'POST'])
def new_cultivation_method():
    if request.method == 'POST':
        culture_medium = request.form['Culture_Medium']
        growth_temperature = request.form['Growth_Temperature']
        cultivation_time = request.form['Cultivation_Time']

        new_method = Cultivation_Methods(Culture_Medium=culture_medium, Growth_Temperature=growth_temperature, Cultivation_Time=cultivation_time)
        db.session.add(new_method)
        db.session.commit()

        return redirect(url_for('cultivation_methods'))

    return render_template('new_cultivation_method.html')

@app.route('/genomic_data')
def genomic_data():
    data = Genomic_Data.query.all()
    return render_template('genomic_data.html', genomic_data=data)

@app.route('/general_info')
def general_info():
    info = General_Info.query.all()
    return render_template('general_info.html', general_info=info)

@app.route('/new_genomic_data', methods=['GET', 'POST'])
def new_genomic_data():
    if request.method == 'POST':
        genomic_sequence = request.form['Genomic_Sequence']
        sequence_file_name = request.form['Sequence_File_Name']

        new_data = Genomic_Data(Genomic_Sequence=genomic_sequence, Sequence_File_Name=sequence_file_name)
        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for('genomic_data'))

    return render_template('new_genomic_data.html')

@app.route('/new_general_info', methods=['GET', 'POST'])
def new_general_info():
    if request.method == 'POST':
        id_taxonomy = request.form['id_taxonomy']
        id_Cultivation_Methods = request.form['id_Cultivation_Methods']
        id_Genomic_Data = request.form['id_Genomic_Data']
        organization = request.form['Organization']
        collection_number = request.form['Collection_Number']
        isolation_date = datetime.strptime(request.form['Isolation_Date'], '%Y-%m-%d')
        isolation_place = request.form['Isolation_Place']
        isolation_source = request.form['Isolation_Source']

        new_info = General_Info(id_taxonomy=id_taxonomy, id_Cultivation_Methods=id_Cultivation_Methods,
                                id_Genomic_Data=id_Genomic_Data, Organization=organization,
                                Collection_Number=collection_number, Isolation_Date=isolation_date,
                                Isolation_Place=isolation_place, Isolation_Source=isolation_source)
        db.session.add(new_info)
        db.session.commit()

        return redirect(url_for('general_info'))

    ranks = Ranks.query.all()
    methods = Cultivation_Methods.query.all()
    genomic_data = Genomic_Data.query.all()
    return render_template('new_general_info.html', ranks=ranks, methods=methods, genomic_data=genomic_data)

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
