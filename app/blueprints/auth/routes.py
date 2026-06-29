from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import (
    LoginForm, RegisterForm, ForgotPasswordForm,
    ResetPasswordForm, ChangePasswordForm
)
from app.services import auth_service


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse.home'))
    form = LoginForm()
    if form.validate_on_submit():
        success, message, user = auth_service.authenticate_user(
            form.username.data,
            form.password.data,
            login_ip=request.headers.get('X-Forwarded-For', request.remote_addr)
        )
        if success:
            session.permanent = True
            login_user(user, remember=False)
            session['session_version'] = user.session_version
            flash(message, 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('browse.home'))
        flash(message, 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('browse.home'))
    # 检查是否有注册成功的标记（从登录页跳转回来的）
    register_success = session.pop('register_success', False)
    form = RegisterForm()
    action = request.form.get('action')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST' and action == 'send_otp':
        # 手动验证 phone 和 email，不需要验证整个表单
        phone = form.phone.data.strip() if form.phone.data else ''
        email = form.email.data.strip() if form.email.data else ''
        
        success, message = auth_service.send_register_otp(
            phone=phone if phone else None,
            email=email if email else None
        )
        
        if is_ajax:
            from flask import jsonify
            return jsonify({
                'success': success,
                'message': message
            })
        else:
            flash(message, 'success' if success else 'danger')
    
    elif form.validate_on_submit():
        success, message, user = auth_service.register_user(
            username=form.username.data,
            password=form.password.data,
            phone=form.phone.data,
            email=form.email.data,
            nickname=form.nickname.data,
            otp=form.otp.data,
            role=form.role.data
        )
        if success:
            # 在 session 中设置标记，用户下次打开注册页面时会清空密码
            session['register_success'] = True
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        flash(message, 'danger')
    
    return render_template('auth/register.html', form=form, register_success=register_success)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('reset_username', None)
    session.pop('reset_identifier', None)
    session.pop('session_version', None)
    logout_user()
    flash('您已退出登录。', 'info')
    return redirect(url_for('browse.home'), code=303)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('browse.home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        success, message = auth_service.send_password_reset_otp(form.username.data)
        flash(message, 'success' if success else 'warning')
        session['reset_identifier'] = form.username.data
        return redirect(url_for('auth.reset_password'))
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('browse.home'))
    identifier = session.get('reset_identifier') or session.get('reset_username', '')
    if not identifier:
        flash('请先输入账号获取验证码。', 'warning')
        return redirect(url_for('auth.forgot_password'))
    form = ResetPasswordForm(username=identifier)
    
    # 处理重新获取验证码的请求
    action = request.form.get('action')
    if request.method == 'POST' and action == 'resend_otp':
        success, message = auth_service.send_password_reset_otp(identifier)
        flash(message, 'success' if success else 'warning')
    
    elif form.validate_on_submit():
        success, message = auth_service.reset_password(
            identifier,
            form.otp.data,
            form.new_password.data
        )
        if success:
            session.pop('reset_username', None)
            session.pop('reset_identifier', None)
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        success, message = auth_service.change_password(
            current_user, form.old_password.data, form.new_password.data
        )
        flash(message, 'success' if success else 'danger')
        if success:
            session['session_version'] = current_user.session_version
    return render_template('auth/change_password.html', form=form)
