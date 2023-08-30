from django.db import models

class UserMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey('Users', models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey('Users', models.DO_NOTHING, related_name='received_messages')
    replyto = models.IntegerField(db_column='replyTo')  # Field name made lowercase.
    message = models.TextField(blank=True, null=True)
    isseen = models.IntegerField(db_column='isSeen')  # Field name made lowercase.
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self)->str:
        return str(self.sender)
    class Meta:
        managed = False
        db_table = 'user_messages'
        
class SdSampler(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sd_sampler'

    def __str__(self) -> str:
        return str(self.name)


class SdUpscaler(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sd_upscaler'

    def __str__(self) -> str:
        return str(self.name)


class SdCheckpoint(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sd_checkpoint'

    def __str__(self) -> str:
        return str(self.filename)



class SdConfig(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    checkpoint_id = models.ForeignKey('SdCheckpoint', on_delete=models.CASCADE,db_column='checkpoint_id') #models.IntegerField(blank=True, null=True)
    sampler_id = models.ForeignKey('SdSampler', on_delete=models.CASCADE, db_column='sampler_id')#models.IntegerField(blank=True, null=True)
    cfg_scale = models.IntegerField(blank=True, null=True)
    upscaler_id = models.ForeignKey('SdUpscaler', on_delete=models.CASCADE, db_column='upscaler_id') #models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sd_config'
    def __str__(self) -> str:
        return str(self.name)
    
class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=191)
    display_name = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
    def __str__(self) -> str:
        return str(self.name)
    
class UserGenders(models.Model):
    id = models.BigAutoField(primary_key=True)
    gender_name = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_genders'
    def __str__(self):
        return str(self.gender_name)

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey('Roles', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=191)
    username = models.CharField(unique=True, max_length=191)
    campaign = models.CharField(max_length=191, blank=True, null=True)
    referral_code = models.CharField(unique=True, max_length=191, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=191, blank=True, null=True)
    website = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    cover = models.CharField(max_length=191, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    identity_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=191)
    gender = models.ForeignKey('UserGenders', models.DO_NOTHING, blank=True, null=True)
    gender_pronoun = models.CharField(max_length=191, blank=True, null=True)
    public_profile = models.IntegerField()
    paid_profile = models.IntegerField()
    profile_access_price = models.FloatField()
    profile_access_price_6_months = models.FloatField(blank=True, null=True)
    profile_access_price_3_months = models.FloatField(blank=True, null=True)
    profile_access_price_12_months = models.FloatField(blank=True, null=True)
    billing_address = models.CharField(max_length=191, blank=True, null=True)
    first_name = models.CharField(max_length=191, blank=True, null=True)
    last_name = models.CharField(max_length=191, blank=True, null=True)
    city = models.CharField(max_length=191, blank=True, null=True)
    country = models.CharField(max_length=191, blank=True, null=True)
    state = models.CharField(max_length=191, blank=True, null=True)
    postcode = models.CharField(max_length=191, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    auth_provider = models.CharField(max_length=191, blank=True, null=True)
    auth_provider_id = models.CharField(max_length=191, blank=True, null=True)
    enable_2fa = models.IntegerField(blank=True, null=True)
    enable_geoblocking = models.IntegerField(blank=True, null=True)
    open_profile = models.IntegerField(blank=True, null=True)
    settings = models.TextField(blank=True, null=True, db_column='settings')
    demo_user_settings = models.ForeignKey('SdConfig', to_field="id", on_delete=models.CASCADE, null=True, db_column='demo_user_settings')
    # settings = models.ForeignKey('SdConfig', to_field="id", on_delete=models.CASCADE, null=True, db_column='settings')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    mature_content = models.IntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=60, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    linked_userid = models.IntegerField(blank=True, null=True)
    type_of_body = models.CharField(max_length=255, blank=True, null=True)
    relationship_status = models.CharField(max_length=255, blank=True, null=True)
    personality = models.CharField(db_column='Personality', max_length=255, blank=True, null=True)  # Field name made lowercase.
    interests = models.CharField(db_column='Interests', max_length=255, blank=True, null=True)  # Field name made lowercase.
    personality_style = models.CharField(max_length=255, blank=True, null=True)
    speech_style = models.CharField(max_length=255, blank=True, null=True)
    favourite_color_and_pattern = models.CharField(max_length=255, blank=True, null=True)
    current_partner = models.CharField(max_length=48, blank=True, null=True)
    breast_size = models.CharField(max_length=48, blank=True, null=True)
    hips_width = models.CharField(max_length=48, blank=True, null=True)
    time_period_fashion = models.CharField(max_length=255, blank=True, null=True)
    looking_for_relationship = models.CharField(max_length=255, blank=True, null=True)
    current_home = models.CharField(max_length=255, blank=True, null=True)
    piercings = models.CharField(max_length=48, blank=True, null=True)
    religion = models.CharField(max_length=48, blank=True, null=True)
    hair_color = models.CharField(max_length=48, blank=True, null=True)
    eye_color = models.CharField(max_length=48, blank=True, null=True)
    height = models.CharField(max_length=48, blank=True, null=True)
    weight = models.CharField(max_length=48, blank=True, null=True)
    cultural_background = models.CharField(max_length=48, blank=True, null=True)
    sd_prompt = models.TextField(blank=True, null=True)
    sd_negative_prompt = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    planning = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
    class Meta: 
        managed = False
        db_table = 'users'
