from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models import User, GameAttempt, ValidIdentifier
from app import db, mail
from flask_mail import Message
from validate_docbr import CPF
import random
import string
import qrcode
from io import BytesIO
import base64

main = Blueprint('main', __name__)

def generate_prize_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def send_prize_email(user_email, prize_code):
    msg = Message('Parabéns! Você ganhou!',
                  sender='noreply@example.com',
                  recipients=[user_email])
    msg.body = f'Parabéns! Você ganhou R$50,00! Seu código de prêmio é: {prize_code}'
    mail.send(msg)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/validate-identifier', methods=['POST'])
def validate_identifier():
    cpf = request.form.get('identifier')
    if not cpf:
        return jsonify({'valid': False, 'message': 'CPF é obrigatório'})
    
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Valida o CPF
    cpf_validator = CPF()
    if not cpf_validator.validate(cpf):
        return jsonify({'valid': False, 'message': 'CPF inválido'})
    
    # Verifica se o CPF já foi usado
    existing_user = User.query.filter_by(cpf=cpf).first()
    if existing_user:
        return jsonify({'valid': False, 'message': 'Este CPF já participou da promoção'})
    
    session['cpf'] = cpf
    return jsonify({'valid': True})

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cpf = session.get('cpf')
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        if not cpf:
            return jsonify({'success': False, 'message': 'Sessão expirada'})
        
        # Create new user
        user = User(cpf=cpf, name=name, phone=phone)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify({'success': True})
    
    return render_template('register.html')

@main.route('/play')
def play():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
    
    user = User.query.get(user_id)
    if not user or user.credits_remaining <= 0:
        return redirect(url_for('main.result'))
    
    return render_template('play.html', credits=user.credits_remaining)

@main.route('/spin', methods=['POST'])
def spin():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Sessão expirada'})
    
    user = User.query.get(user_id)
    if not user or user.credits_remaining <= 0:
        return jsonify({'success': False, 'message': 'Sem créditos restantes'})
    
    # Create game attempt
    attempt = GameAttempt(user_id=user.id, attempt_number=4-user.credits_remaining)
    user.credits_remaining -= 1
    
    # First attempt never wins
    if attempt.attempt_number == 1:
        attempt.result = False
    else:
        # Check if user already won
        if user.is_winner:
            attempt.result = False
        else:
            # 1 in 3 chance of winning after first attempt
            # Limited to 122 total winners
            total_winners = User.query.filter_by(is_winner=True).count()
            if total_winners < 122 and random.random() < 0.33:
                attempt.result = True
                user.is_winner = True
                user.prize_code = generate_prize_code()
                # Here you would send the email with the prize code
                # send_prize_email(user.email, user.prize_code)
    
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'result': attempt.result,
        'credits_remaining': user.credits_remaining,
        'prize_code': user.prize_code if attempt.result else None
    })

@main.route('/result')
def result():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
    
    user = User.query.get(user_id)
    return render_template('result.html', user=user)

@main.route('/generate-qr')
def generate_qr():
    # Generate QR code for the registration URL
    registration_url = url_for('main.index', _external=True)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('qr.html', qr_code=img_str)
