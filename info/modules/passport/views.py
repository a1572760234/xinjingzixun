import re
import random

from flask import current_app, make_response, jsonify
from flask_restful import Resource, reqparse

from info.models import User
from info.utils.captcha.captcha import captcha
from info import constants
from info import redis_client
from info.utils.response_code import RET


class ImageCodeResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code_id', location='args', required=True)
        args = parser.parse_args()
        # 获取当前验证码编号
        code_id = args.get('code_id')
        # 生成验证码
        text, image = captcha.generate_captcha()
        # 保存验证码生成的内容
        try:
            redis_client.setex('ImageCode' + code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        except Exception as e:
            current_app.logger.error(e)
            return make_response(jsonify(errno=RET.DATAERR, errmsg='短信验证码保存失败'))
        resp = make_response(image)
        resp.headers['Content-Type'] = 'image/jpg'
        return resp


class SMSCodeResource(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('mobile', location='json', required=True)
        parser.add_argument('image_code', location='json', required=True)
        parser.add_argument('image_code_id', location='json', required=True)
        args = parser.parse_args()
        mobile = args.get('mobile')
        image_code = args.get('image_code')
        image_code_id = args.get('image_code_id')
        # 校验参数
        if not all([mobile, image_code, image_code_id]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不全')
        # 判断手机号格式是否正确
        if not re.match("^1[3578][0-9]{9}$", mobile):
            return jsonify(errno=RET.DATAERR, errmsg='格式错误')
        # 判断图片验证码内容
        try:
            redis_image_code = redis_client.get('ImageCode' + image_code_id)
            if redis_image_code:
                # 解码图片验证码
                redis_image_code = redis_image_code.decode()
                redis_client.delete('ImageCode' + image_code_id)
            else:
                return jsonify(errno=RET.NODATA, errmsg='验证码已过期')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='获取验证码失败')
        # 验证码比对
        if redis_image_code.lower() != image_code.lower():
            return jsonify(errno=RET.DATAERR, errmsg='验证码输入错误')
        # 判断手机号是否已注册
        try:
            user = User.query.filter(User.mobile==mobile).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='查询错误')
        if user:
            return jsonify(errno=RET.DATAEXIST, errmsg='手机号已被注册')
        # 生成短信验证码并且发送
        sms_code ='%06d' % random.randint(0, 999999)
        key = f'info:code:{mobile}'
        try:
            redis_client.set(key, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存短信验证码失败')
        print(sms_code)
        return jsonify(errno=RET.OK, errmsg='发送成功')

