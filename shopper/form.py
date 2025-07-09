from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
    普通表单类，用户登录表单，不直接操作数据库
    """
    username = forms.CharField(
        max_length=11,  # 最大长度
        label='请输入您的手机号',  # 字段标签
        widget=forms.TextInput(
            attrs={
                'class': 'layui-input',  # LayUI输入框样式
                'placeholder': '请输入您的手机号',  # 占位提示文本
                'lay-verity': 'required|phone',  # LayUI验证规则：必填+手机号格式
                'id': 'username'  # 输入框ID
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        label='请您输入密码',
        widget=forms.PasswordInput(
            attrs={
                'class': 'layui-input',
                'placeholder': '请您输入密码',
                'lay-verity': 'required|password',
                'id': 'password'
            }
        )
    )

    def clean_username(self):
        """
        自定义表单字段username的数据清洗函数
        只适用于username数据的清洗，函数名的格式必须clean_表单字段
        必须有return返回值
        """
        # 验证手机号是否是11位
        # 获取清洗后的数据
        username = self.cleaned_data['username']
        if len(username) == 11:
            return username
        else:
            # 验证失败就抛出异常，错误将会显示在表单上
            raise ValidationError('用户名为手机号')


class LoginModelForm(forms.ModelForm):
    """
    模型表单类，继承自ModelForm，可以直接操作数据库
    """
    class Meta:
        """
        重新定义Meta类，分别设置属性model、fields、labels、error_messages、widgets
        并且自定义表单字段username的数据清洗函数
        """
        model = User  # 关联Django内置的User模型
        fields = ('username', 'password')  # 包含的模型字段
        # 字段标签，覆盖模型中的verbose_name
        labels = {
            'username': '请输入您的手机号',
            'password': '请输入您的密码',
        }
        # 错误信息
        error_messages = {
            '__all__':{
                'required': '请输入内容',   # 必填字段错误
                'invalid': '请检查输入内容'  # 格式错误
            },
        }
        # 自定义表单控件属性
        widgets = {
            'username': forms.widgets.TextInput(
                attrs={
                    'class': 'layui-input',
                    'placeholder': '请输入您的手机号',
                    'lay-verify': 'required|phone',
                    'id': 'username'
                }
            ),
            'password': forms.widgets.PasswordInput(
                attrs={
                    'class': 'layui-input',
                    'placeholder': '请输入您的密码',
                    'lay-verify': 'required|password',
                    'id': 'password'
                }
            )
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) == 11:
            return username
        else:
            raise ValidationError('用户名为手机号')