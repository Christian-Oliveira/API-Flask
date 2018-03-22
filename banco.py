import peewee
from flask import Flask, jsonify, request

banco = peewee.SqliteDatabase('banco.db')

class Postagens(peewee.Model):
	titulo = peewee.CharField()
	conteudo = peewee.TextField()

	def to_dict(self):
		return {'id':self.id, 'titulo':self.titulo, 'conteudo':self.conteudo}

	class Meta:
		database = banco
