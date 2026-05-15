from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from oauthlib.oauth2 import WebApplicationClient
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import requests
from src import db, mail
from src.models import User
from src.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm

auth = Blueprint('auth', __name__)

# OAuth Client Setup
google_client = None
facebook_client = None

def get_google_provider_cfg():
    try:
        return requests.get('https://accounts.google.com/.well-known/openid-configuration').json()
    except:
        return None

@auth.route('/oauth/login/<provider>')
def oauth_login(provider):
    if provider == 'google':
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            flash('Google OAuth is not configured. Please set up OAuth credentials.', 'danger')
            return redirect(url_for('auth.login'))
        
        client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        if not client_id:
            flash('Google OAuth credentials not configured. Please add GOOGLE_CLIENT_ID to .env file.', 'danger')
            return redirect(url_for('auth.login'))
        
        session['oauth_provider'] = 'google'
        authorization_endpoint = google_provider_cfg['authorization_endpoint']
        client = WebApplicationClient(client_id)
        
        # Use explicit redirect URI from config
        redirect_uri = current_app.config.get('OAUTH_REDIRECT_URI')
        print(f"Using redirect URI: {redirect_uri}")
        
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=['openid', 'email', 'profile'],
        )
        print(f"Full request URI: {request_uri}")
        return redirect(request_uri)
    
    elif provider == 'facebook':
        client_id = current_app.config.get('FACEBOOK_CLIENT_ID')
        if not client_id:
            flash('Facebook OAuth credentials not configured. Please add FACEBOOK_CLIENT_ID to .env file.', 'danger')
            return redirect(url_for('auth.login'))
        
        session['oauth_provider'] = 'facebook'
        authorization_endpoint = 'https://www.facebook.com/v18.0/dialog/oauth'
        client = WebApplicationClient(client_id)
        
        # Use explicit redirect URI
        redirect_uri = url_for('auth.oauth_callback', provider='facebook', _external=True)
        
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=['email'],
        )
        return redirect(request_uri)
    
    flash(f'{provider.title()} login is not supported.', 'danger')
    return redirect(url_for('auth.login'))

@auth.route('/oauth/callback/<provider>')
def oauth_callback(provider):
    if provider == 'google':
        client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            flash('Google OAuth credentials not configured.', 'danger')
            return redirect(url_for('auth.login'))
        
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            flash('Unable to connect to Google.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Get authorization code
        code = request.args.get('code')
        if not code:
            flash('Authorization failed.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Exchange code for tokens
        token_url = google_provider_cfg['token_endpoint']
        client = WebApplicationClient(client_id)
        
        # Use explicit redirect URI from config
        redirect_uri = current_app.config.get('OAUTH_REDIRECT_URI')
        
        try:
            token_response = requests.post(
                token_url,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data=client.prepare_request_body(
                    client_secret=client_secret,
                    code=code,
                    redirect_uri=redirect_uri,
                ),
            )
            
            token_data = token_response.json()
            client.parse_request_body_response(token_response.text)
            
            # Get user info
            userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
            uri, headers, body = client.add_token(userinfo_endpoint)
            userinfo_response = requests.get(uri, headers=headers)
            userinfo = userinfo_response.json()
            
            # Find or create user
            email = userinfo.get('email')
            if not email:
                flash('Could not get email from Google.', 'danger')
                return redirect(url_for('auth.login'))
            
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create new user from Google info
                username = userinfo.get('name', email.split('@')[0])
                # Ensure unique username
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(username=username, email=email)
                user.set_password('oauth_user_' + str(user.id))  # Random password
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash(f'OAuth error: {str(e)}', 'danger')
            return redirect(url_for('auth.login'))
    
    elif provider == 'facebook':
        client_id = current_app.config.get('FACEBOOK_CLIENT_ID')
        client_secret = current_app.config.get('FACEBOOK_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            flash('Facebook OAuth credentials not configured.', 'danger')
            return redirect(url_for('auth.login'))
        
        code = request.args.get('code')
        if not code:
            flash('Authorization failed.', 'danger')
            return redirect(url_for('auth.login'))
        
        try:
            # Exchange code for access token
            token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
            redirect_uri = url_for('auth.oauth_callback', provider='facebook', _external=True)
            token_response = requests.get(token_url, params={
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'code': code,
            })
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                flash('Failed to get access token from Facebook.', 'danger')
                return redirect(url_for('auth.login'))
            
            access_token = token_data['access_token']
            
            # Get user info
            userinfo_url = 'https://graph.facebook.com/me'
            userinfo_response = requests.get(userinfo_url, params={
                'fields': 'id,name,email',
                'access_token': access_token,
            })
            userinfo = userinfo_response.json()
            
            email = userinfo.get('email')
            if not email:
                flash('Facebook email permission required. Please grant email access.', 'danger')
                return redirect(url_for('auth.login'))
            
            user = User.query.filter_by(email=email).first()
            if not user:
                username = userinfo.get('name', email.split('@')[0])
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(username=username, email=email)
                user.set_password('oauth_user_' + str(user.id))
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash(f'OAuth error: {str(e)}', 'danger')
            return redirect(url_for('auth.login'))
    
    flash('OAuth callback failed.', 'danger')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different one.', 'danger')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if input is email or username
        identifier = form.username.data.strip()
        if '@' in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/email or password', 'danger')
            return render_template('login.html', form=form)
        
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to next page if exists
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        # Always show the same message to prevent email enumeration
        flash('If that email is registered, a password reset link has been sent.', 'info')
        if user:
            try:
                s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                token = s.dumps(user.email, salt='password-reset-salt')
                reset_url = url_for('auth.reset_password', token=token, _external=True)
                msg = Message(
                    subject='Reset Your To-Do App Password',
                    recipients=[user.email],
                    html=f'''
                    <div style="font-family:Inter,sans-serif;max-width:480px;margin:auto;padding:32px;background:#f8fafc;border-radius:12px;">
                        <h2 style="color:#0f172a;margin-bottom:8px;">Password Reset</h2>
                        <p style="color:#64748b;margin-bottom:24px;">Click the button below to reset your password. This link expires in <strong>30 minutes</strong>.</p>
                        <a href="{reset_url}" style="display:inline-block;background:#3b82f6;color:white;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:600;">Reset Password</a>
                        <p style="color:#94a3b8;font-size:13px;margin-top:24px;">If you didn't request this, just ignore this email.</p>
                    </div>
                    '''
                )
                mail.send(msg)
            except Exception as e:
                current_app.logger.error(f'Failed to send password reset email: {e}')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=1800)  # 30 minutes
    except SignatureExpired:
        flash('The password reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    except BadSignature:
        flash('Invalid or tampered reset link. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, token=token)
