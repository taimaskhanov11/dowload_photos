from tortoise import models, fields


class Users(models.Model):
    old_id = fields.TextField()
    name = fields.TextField()
    country = fields.TextField()
    birthday = fields.TextField()
    img_src = fields.TextField()
    qr_code = fields.TextField()
    user_status = fields.TextField()
