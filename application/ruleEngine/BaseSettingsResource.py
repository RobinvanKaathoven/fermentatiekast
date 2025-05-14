from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from util.db import db

from ruleEngine.RuleEngine import ruleEngine

class BaseSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<BaseSettings {self.name}>'

class BaseSettingsResource():
    def get(self, base_setting_id):
        base_setting = BaseSettings.query.get(base_setting_id)
        if not base_setting:
            abort(404, message="Base setting not found")
        return base_setting
    def put(self, base_setting_name, value):
        base_setting = BaseSettings.query.filter_by(name=base_setting_name).first()
        if not base_setting:
            base_setting = BaseSettings(name=base_setting_name, value=value)
            db.session.add(base_setting)
        base_setting.value = value
        db.session.commit()
        return base_setting
    def delete(self, base_setting_name):
        base_setting = BaseSettings.query.filter_by(name=base_setting_name).first()
        if not base_setting:
            abort(404, message="Base setting not found")
        db.session.delete(base_setting)
        db.session.commit()
        return '', 204

    def updateRuleEngineSettings(self):
        # Update the rule engine settings based on the base settings
        test = BaseSettings.query.filter_by(name='targetTemperature').first()
        targetTemperature = float(BaseSettings.query.filter_by(name='Target_Temperature').first().value)
        targetHumidity = float(BaseSettings.query.filter_by(name='Target_Humidity').first().value)
        ruleEngine.setTargetTemperature(targetTemperature)
        ruleEngine.setTargetHumidity(targetHumidity)
        temperatureThreshold = float(BaseSettings.query.filter_by(name='Temperature_Threshold').first().value)
        ruleEngine.setTemperatureThreshold(temperatureThreshold)
        humidityThreshold = float(BaseSettings.query.filter_by(name='Humidity_Threshold').first().value)
        ruleEngine.setHumidityThreshold(humidityThreshold)
