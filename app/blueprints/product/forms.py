from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import Length, Optional
from wtforms.validators import ValidationError


class OptionalDecimalField(DecimalField):
    """可选的 DecimalField，允许为空"""
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0] and valuelist[0].strip():
            # 只有当有值时才处理
            super().process_formdata(valuelist)
        else:
            # 空值时设置为 None
            self.data = None
    
    def pre_validate(self, form):
        # 跳过默认的必填验证，让自定义的验证逻辑处理
        pass


class ProductForm(FlaskForm):
    product_name = StringField('商品名称', validators=[
        Length(max=50, message='商品名称最多50个字符')
    ])
    category_id = SelectField('商品分类', coerce=int)
    price = OptionalDecimalField('价格')
    condition_level = SelectField('商品成色', choices=[
        ('全新', '全新'),
        ('九成新', '九成新'),
        ('八成新', '八成新'),
        ('七成新', '七成新'),
        ('七成新以下', '七成新以下'),
    ])
    description = TextAreaField('商品描述', validators=[
        Length(max=1000, message='描述最多1000个字符')
    ])
    trade_location = StringField('交易地点', validators=[
        Length(max=255)
    ])
    submission_token = HiddenField()
    submit_draft = SubmitField('保存草稿')
    submit_publish = SubmitField('提交审核')
    
    def validate(self, extra_validators=None):
        # 先执行基础验证
        if not super().validate(extra_validators=extra_validators):
            return False
        
        # 如果是提交审核，进行严格验证
        if self.submit_publish.data:
            # 商品名称必填
            if not self.product_name.data or not self.product_name.data.strip():
                self.product_name.errors.append('请填写商品名称')
                return False
            
            # 商品名称长度限制
            if len(self.product_name.data.strip()) > 50:
                self.product_name.errors.append('商品名称最多50个字符')
                return False
            
            # 分类必选
            if not self.category_id.data:
                self.category_id.errors.append('请选择分类')
                return False
            
            # 价格必填
            if not self.price.data:
                self.price.errors.append('请输入价格')
                return False
            
            # 检查价格范围
            if self.price.data:
                from decimal import Decimal
                if self.price.data < Decimal('0.01'):
                    self.price.errors.append('价格必须大于或等于0.01')
                    return False
                if self.price.data > Decimal('99999.99'):
                    self.price.errors.append('价格必须小于或等于99999.99')
                    return False
            
            # 成色必选
            if not self.condition_level.data:
                self.condition_level.errors.append('请选择成色')
                return False
            
            # 描述必填且长度足够
            if not self.description.data or len(self.description.data.strip()) < 10:
                self.description.errors.append('商品描述需要10~1000个字符')
                return False
            
            if len(self.description.data.strip()) > 1000:
                self.description.errors.append('商品描述最多1000个字符')
                return False
            
            # 交易地点必填
            if not self.trade_location.data or not self.trade_location.data.strip():
                self.trade_location.errors.append('请输入交易地点')
                return False
        
        return True
