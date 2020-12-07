# coding:utf-8
from info.libs.yuntongxun.CCPRestSDK import REST

accountSid='8a216da874af5fff0174fd9a97321935'
accountToken='1dbb7dca028144cba0d42ff5e4177990'
appId='8a216da874af5fff0174fd9a983a193c'
serverIP='sandboxapp.cloopen.com'
serverPort='8883'
softVersion='2013-12-26'  #说明：REST API版本号保持不变。

class CCP(object):
    """发送短信的辅助类"""

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "instance"):
            cls.instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls.instance.rest = REST(serverIP, serverPort, softVersion)
            cls.instance.rest.setAccount(accountSid, accountToken)
            cls.instance.rest.setAppId(appId)
        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        """发送模板短信"""
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # 如果云通讯发送短信成功，返回的字典数据result中statuCode字段的值为"000000"
        if result.get("statusCode") == "000000":
            # 返回0 表示发送短信成功
            return 0
        else:
            # 返回-1 表示发送失败
            return -1

if __name__ == '__main__':
    ccp = CCP()
    print(ccp.send_template_sms('18355896696',['123456',5],1))