#-*-coding:utf-8-*-
import peewee
from flask import Flask, jsonify, request

#Criação do modelo de BD
banco = peewee.SqliteDatabase('banco.db')

class Postagem(peewee.Model):
	titulo = peewee.CharField()
	conteudo = peewee.TextField()

	class Meta:
		database = banco

#Criação de tabela de postagem
try:
	banco.create_tables(Postagem)
except Exception as e:
	pass
#instância do Flask
app = Flask(__name__)

#função para conectar ao BD
@app.before_request
def before_request():
	banco.connect()

#função para desconectar do BD
@app.after_request
def after_request(response):
	banco.close()
	return response

#GET /postagens/
@app.route('/postagens/')
def postagens():
	return jsonify(list(Postagem.select()))

#GET /postagens/1
@app.route('/postagens/<int:id_postagem>')
def postagem(id_postagem):
	try:
		postagem = Postagem.get(id_postagem)
		return jsonify(postagem)
	except Postagem.DoesNotExist:
		return jsonify({'status': 404, 'mensagem': 'Postagem não encontrada'})

#POST /postagens/
@app.route('/postagens/', methods = ['POST'])
def nova_postagem():
	dados = request.json
	postagem = Postagem(titulo=dados['titulo'], conteudo=dados['conteudo'])
	postagem.save()
	return jsonify({'status':200, 'mensagem':'Postagem salva com sucesso!'})

#PUT/PATCH/postagens/1
@app.route('/postagens/<int:id_postagem>', methods=['PUT', 'PATCH'])
def editar_postagem(id_postagem):
	dados = request.json
	#verifica se a postagem existe no BD
	try:
		postagem = Postagem.get(id_postagem)
	except Postagem.DoesNotExist as e:
		return jsonify({'status':404, 'mensagem': 'Postagem não encontrada'})
	#pegando postagem do banco e atualizando
	postagem.titulo = dados['titulo']
	postagem.conteudo = dados['conteudo']
	postagem.save()
	#mensagem de sucesso
	return jsonify({'status':200, 'mensagem': 'Postagem salva com sucesso'})

#DELETE /postagens/1
@app.route('/postagens/<int:id_postagem>', methods=['DELETE'])
def apagar_postagem(id_postagem):
	#recupera a postagem
	try:
		postagem = Postagem.get(id_postagem)
		postagem.delete()
		return jsonify({'status':200, 'mensagem':'Postagem excluída com sucesso'})
	except Postagem.DoesNotExist:
		return jsonify({'status':404, 'mensagem':'Postagem não encontrada'})

if __name__=='__main__':
	app.run(debug=True)