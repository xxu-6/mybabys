from alipay import AliPay

# 支付宝公钥，用于验证支付回调签名
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhQ7ZrhUHOchyMbyy3w7E6xCJEbmrjo+thDRwRMKuavP5RSinI2uE/56LK8yvz/zw40MdLQNSyx8xh2/eWsNpg9KC3wLzCZcTPJHrpXjfV+hnybBmd9UBw9GCycVYYZh1d0CD9AzL1s5cBgNGqXtjKwDD7VcKkidV4DsZ57wUeZiTDrEDK0BaLUp5ygTSFAuM3sAZ8jq5hkTIGSPqWn33gIKb+9mf9rKVWtZX66zFxW+dYFaq/6w/ZpeKR4cYdhSWxQjSViYl56V9sU9ETj56m554duaQzev4h4k1AUlPZiX0Tiv8q/D/Hk/K8gwDkOEjvC8uKxddQ3xnmdsol08t2wIDAQAB
-----END PUBLIC KEY-----"""
# 应用私钥，用于生成支付签名，我们需要转换私钥格式
# https://opendocs.alipay.com/common/02khjp?pathHash=e5a2e515
app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAhQ7ZrhUHOchyMbyy3w7E6xCJEbmrjo+thDRwRMKuavP5RSinI2uE/56LK8yvz/zw40MdLQNSyx8xh2/eWsNpg9KC3wLzCZcTPJHrpXjfV+hnybBmd9UBw9GCycVYYZh1d0CD9AzL1s5cBgNGqXtjKwDD7VcKkidV4DsZ57wUeZiTDrEDK0BaLUp5ygTSFAuM3sAZ8jq5hkTIGSPqWn33gIKb+9mf9rKVWtZX66zFxW+dYFaq/6w/ZpeKR4cYdhSWxQjSViYl56V9sU9ETj56m554duaQzev4h4k1AUlPZiX0Tiv8q/D/Hk/K8gwDkOEjvC8uKxddQ3xnmdsol08t2wIDAQABAoIBAFEXVNkAXc/8doQTcZv5v09XW4Ie+ww+SkypPMbbMzthh0h71ykCDSNQd5bw/zEuAY0vyOc3AE1krGXTats7/uFk+Xd6r63nkcS3VbsaKFvF+wLza++aNKIn3KKlkBCivuw3uHOTHOPEDldnxbfix/RcWgwaoQmjyXWH72jIul3EEwJ6lRax4zbjjBsvpeu5ULGIgY5AlM2U/1Wj0K/mUO0HbrPYC/ap7Pyfx0P0IWJn5+++UN6OisJ44AH4k0YbMk8avBBhZrGu8g1g3e5TwNaxubpifp535i0+XANLH9U2fBg9LG21+xh4hSFndYYmH3TdTy0HLA7pt5KLs3FvwVkCgYEA8DP5WWQeOb+TDUzYu5OMa+zwqmV4fmP67ad7aDtL9B0oroLu7dxdKs3Erw7cHWBnEeaB6hfTDYaGUYYD/GsjifHq+SE3SrxStwiTOYvfoRKalxWhaE3dWxcig2LpdWlyiHE4cgzB2Hf5HERnrm7uvitnKbD/MjsHlXfBhAVK6QUCgYEAjc7/RbsdoLi9nYeGamfdEcL0tmoQPxtUP/3El6jRsxGquhemBQe9lBf2nmxb0VQSdUNSzelIEEOVMhjz3PM64mRkm5XmD9dx9ArZ2bTa4MZoXxtrIlqSP4vKrf49X87VMNcXZEZYtgurCirVgZ+F7PjFEaIlFSTqbmM5kYOh8V8CgYB7zh4gT/UwSKjPuyMek29WFVr6SLCxXHDyW1fFIoMEgJ7+S6hA20r+C+7rV9pmHdEiLdAaS0tR9lt2239kdAhuSk2VOOSZ1bVAd+ACUjDigYdChjiaXT/Renwkgi/Yf5Az+T9hsWecXkH8qtlR1AWj6RUULRFr33cKOB57IIs6zQKBgBdHv0KsWE3VZlOhNyDq0jEjR1dXDDm/+9HRkF+xeFOkd9m7Hic/QRE56ePSODSiT7Fujv586La60Zh63jYMvEMEZjvgnPdG0E9XJLKH7VLvX50VfD4UjmPeSDTOQzciVn+BIDb3EYM5YSf3Jjv0e2EO6hNeAiZ5e/8JTR8ldAWTAoGBALo4dP0w7ycW5ZkKuxJngVg0/l1aDetXr6BDztBGboQm5HVHkr4lV6JP1wu9gblUhEzUpmFu536CdXMoDU9NgvNtwpaRhztSoiaiUlhEGpoyij4Mhc2O9J2IoUM/iY8fbO1t8TsdMcCZnrp4uOgbmz2tNNyGqj0IkdG9FvQp7nSP
-----END RSA PRIVATE KEY-----"""

def get_pay(out_trade_no, total_amount, return_url):
    """
    生成支付宝的支付链接
    :param out_trade_no: 商户订单号
    :param total_amount: 支付金额
    :param return_url: 支付成功后的回调URL地址
    :return: 支付宝支付页面URL
    """
    # 初始化支付宝SDK实例
    alipay = AliPay(
        # 自己的支付宝应用ID，沙箱环境的
        appid='9021000150626288',
        # 异步通知地址，None表示使用默认
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        # 签名算法
        sign_type='RSA2'
    )

    # 生成支付宝页面支付请求参数
    order_string = alipay.api_alipay_trade_page_pay(
        # 商户的订单号，唯一，建议使用时间戳+随机数生成
        out_trade_no=out_trade_no,
        # 支付金额，转换为字符串主要是为了避免精度问题
        total_amount=str(total_amount),
        # 订单的标题
        subject='测试',
        # 支付成功后，同步回调地址
        return_url=return_url + "?t=" + out_trade_no,
        # 支付成功后的异步通知地址
        notify_url=return_url + "?t=" + out_trade_no,
    )
    # 拼接支付宝网关URL，生成一个可以访问的支付链接
    return "https://openapi-sandbox.dl.alipaydev.com/gateway.do?" + order_string