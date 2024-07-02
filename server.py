from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "admin password"})
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == 'admin_password':  # replace with your actual password
            session['logged_in'] = True
            return redirect(request.args.get('next') or url_for('subdomain_home'))
        else:
            form.password.errors.append('Invalid password')
    return render_template_string(login_template, form=form)


@app.before_request
def require_login():
    # Do not require login for the main home and login routes
    if request.endpoint not in ['main_home', 'login'] and not session.get('logged_in'):
        return redirect(url_for('login', next=request.url))


@app.route('/', subdomain='sub')
def subdomain_home():
    return 'Hello from the subdomain!'


@app.route('/')
def main_home():
    # Automatically detect the current domain and construct the subdomain URL
    current_domain = request.host
    subdomain_url = f"http://sub.{current_domain}"
    return render_template_string(main_home_template, subdomain_url=subdomain_url)


login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            background-color: rgba(173, 216, 230, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .login-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        input[type="password"] {
            padding: 10px;
            width: calc(100% - 22px);
            margin-bottom: 10px;
        }
        input[type="submit"] {
            padding: 10px;
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.password.label }}
            {{ form.password(size=32) }}
            {% for error in form.password.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
            {{ form.submit() }}
        </form>
    </div>
</body>
</html>
"""

main_home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Main Home</title>
    <style>
        body {
            background-color: rgba(173, 216, 230, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .content-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        a {
            display: block;
            margin-top: 20px;
            text-decoration: none;
            color: #4CAF50;
            font-weight: bold;
        }
        a:hover {
            color: #45a049;
        }
    </style>
</head>
<body>
    <div class="content-container">
        <h1>Welcome to the Main Domain</h1>
        <p>This is the main domain. Visit the admin panel on the subdomain for more features.</p>
        <a href="{{ subdomain_url }}">Go to Admin Panel</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
