from flask import current_app, make_response, jsonify
from flask_restful import Resource, reqparse
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
            redis_client.setex('ImageCode'+code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        except Exception as e:
            current_app.logger.error(e)
            return make_response(jsonify(errno=RET.DATAERR,errmsg='短信验证码保存失败'))
        resp = make_response(image)
        resp.headers['Content-Type'] = 'image/jpg'
        return resp

