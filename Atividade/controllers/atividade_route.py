from flask import Blueprint, request, jsonify
from models.atividade_model import Atividade, Submissao 
from database import db
import requests
import json

routes = Blueprint("routes", __name__)


def validar_aluno(id_aluno):
    try:
        resp = requests.get(f"http://localhost:5002/api/alunos/{id_aluno}")
        if resp.status_code == 200:
            dados = resp.json()
            return dados.get("nome") 
    except requests.RequestException as e:
        print(f"Erro ao conectar com o serviço de aluno para ID {id_aluno}: {e}")
        pass
    return None

def validar_professor(id_professor):
    try:
        resp = requests.get(f"http://localhost:5002/api/professores/{id_professor}")
        if resp.status_code == 200:
            dados = resp.json()
            return dados.get("nome")
    except requests.RequestException:
        pass
    return None


@routes.route("/atividades", methods=["POST"])
def criar_atividade():
    dados = request.json
    id_professor = dados.get("id_professor")
    id_disciplina = dados.get("id_disciplina")
    enunciado = dados.get("enunciado")
    respostas_recebidas = dados.get("respostas")

    if id_disciplina is None:
        return jsonify({"erro": "id_disciplina é obrigatório"}), 400
    if not enunciado:
        return jsonify({"erro": "enunciado é obrigatório"}), 400
    if respostas_recebidas is not None and not isinstance(respostas_recebidas, list):
        return jsonify({"erro": "'respostas' deve ser uma lista"}), 400
    if id_professor is None:
        return jsonify({"erro": "id_professor é obrigatório"}), 400

    alunos_validos = {}
    if respostas_recebidas:
        for resposta_data in respostas_recebidas:
            if not isinstance(resposta_data, dict):
                return jsonify({"erro": "Cada item em 'respostas' deve ser um objeto JSON"}), 400
            
            id_aluno = resposta_data.get("id_aluno")
            resposta_texto = resposta_data.get("resposta")
            nota = resposta_data.get("nota")

            if id_aluno is None:
                return jsonify({"erro": "Cada resposta deve ter um 'id_aluno'"}), 400
            if not resposta_texto:
                return jsonify({"erro": f"Resposta para o aluno {id_aluno} é obrigatória"}), 400
            if nota is None:
                return jsonify({"erro": f"Nota para o aluno {id_aluno} é obrigatória"}), 400
            if id_aluno not in alunos_validos:
                nome_aluno = validar_aluno(id_aluno)
                if not nome_aluno:
                    return jsonify({"erro": f"Aluno com ID {id_aluno} não encontrado ou serviço de aluno indisponível."}), 400
                alunos_validos[id_aluno] = nome_aluno 

    nome_professor = validar_professor(id_professor)
    if not nome_professor:
        return jsonify({"erro": "Professor não encontrado ou serviço de professores indisponível"}), 400
    
    try:
        
        atividade = Atividade(
            id_professor = id_professor,
            id_disciplina=id_disciplina,
            enunciado=enunciado
        )
        db.session.add(atividade)
        db.session.flush()

        if respostas_recebidas:
            for resposta_data in respostas_recebidas:
                submissao = Submissao(
                    id_atividade=atividade.id_atividade, 
                    id_aluno=resposta_data['id_aluno'],
                    resposta=resposta_data['resposta'],
                    nota=resposta_data['nota']
                )
                db.session.add(submissao)

        db.session.commit()

        return jsonify({"mensagem": "Atividade criada com sucesso", "id_atividade": atividade.id_atividade}), 201

    except Exception as e:
        db.session.rollback() 
        print(f"Erro ao criar atividade: {e}")
        return jsonify({"erro": "Ocorreu um erro ao criar a atividade."}), 500
    



@routes.route("/atividades", methods=["GET"])
def listar_atividades():
    try:
        
        atividades = Atividade.query.options(db.joinedload(Atividade.submissoes)).all()
        lista_atividades = []

        for atividade in atividades:
            submissoes_formatadas = []
            for submissao in atividade.submissoes:
                submissoes_formatadas.append({
                    "id_aluno": submissao.id_aluno,
                    "resposta": submissao.resposta,
                    "nota": submissao.nota,
                    "id_submissao": submissao.id_submissao 
                })

            lista_atividades.append({
                "id_professor": atividade.id_professor,
                "id_atividade": atividade.id_atividade,
                "id_disciplina": atividade.id_disciplina,
                "enunciado": atividade.enunciado,
                "respostas": submissoes_formatadas
            })
        return jsonify(lista_atividades), 200
    except Exception as e:
        print(f"Erro ao listar atividades: {e}")
        return jsonify({"erro": "Ocorreu um erro ao buscar as atividades."}), 500
    



@routes.route("/atividades/<int:id_atividade>", methods=["GET"])
def buscar_atividade_por_id(id_atividade):
    try:
    
        atividade = Atividade.query.options(db.joinedload(Atividade.submissoes)).get(id_atividade)
        
        if not atividade:
            return jsonify({"erro": "Atividade não encontrada."}), 404

        submissoes_formatadas = []
        for submissao in atividade.submissoes:
            submissoes_formatadas.append({
                "id_aluno": submissao.id_aluno,
                "resposta": submissao.resposta,
                "nota": submissao.nota,
                "id_submissao": submissao.id_submissao
            })

        atividade_data = {
            "id_professor": atividade.id_professor,
            "id_atividade": atividade.id_atividade,
            "id_disciplina": atividade.id_disciplina,
            "enunciado": atividade.enunciado,
            "respostas": submissoes_formatadas
        }
        return jsonify(atividade_data), 200
    except Exception as e:
        print(f"Erro ao buscar atividade por ID: {e}")
        return jsonify({"erro": "Ocorreu um erro ao buscar a atividade."}), 500
    


@routes.route("/atividades/<int:id_atividade>", methods=["PATCH"])
def atualizar_atividade(id_atividade):
    dados = request.json
    try:
        atividade = Atividade.query.get(id_atividade)
        if not atividade:
            return jsonify({"erro": "Atividade não encontrada."}), 404
        if "id_disciplina" in dados:
            atividade.id_disciplina = dados["id_disciplina"]
        if "enunciado" in dados:
            atividade.enunciado = dados["enunciado"]
        if "respostas" in dados:
            respostas_recebidas = dados["respostas"]
            if not isinstance(respostas_recebidas, list):
                return jsonify({"erro": "'respostas' deve ser uma lista"}), 400
            
            
            submissoes_existentes = {sub.id_submissao: sub for sub in atividade.submissoes}
            submissoes_a_manter_ids = set()

            for resposta_data in respostas_recebidas:
                id_submissao = resposta_data.get("id_submissao")
                id_aluno = resposta_data.get("id_aluno")
                resposta_texto = resposta_data.get("resposta")
                nota = resposta_data.get("nota")

              
                if id_aluno is None or not resposta_texto or nota is None:
                    return jsonify({"erro": "Cada resposta deve ter id_aluno, resposta e nota"}), 400
                nome_aluno = validar_aluno(id_aluno)
                if not nome_aluno:
                    return jsonify({"erro": f"Aluno com ID {id_aluno} não encontrado ou serviço de aluno indisponível."}), 400
                if id_submissao and id_submissao in submissoes_existentes:
                 
                    submissao = submissoes_existentes[id_submissao]
                    submissao.id_aluno = id_aluno
                    submissao.resposta = resposta_texto
                    submissao.nota = nota
                    submissoes_a_manter_ids.add(id_submissao)
                else:
                  
                    nova_submissao = Submissao(
                        id_atividade=atividade.id_atividade,
                        id_aluno=id_aluno,
                        resposta=resposta_texto,
                        nota=nota
                    )
                    db.session.add(nova_submissao)
                   

            for submissao_existente in list(atividade.submissoes): 
                if submissao_existente.id_submissao not in submissoes_a_manter_ids and \
                   submissao_existente.id_submissao not in [s.get("id_submissao") for s in respostas_recebidas if s.get("id_submissao")]:
                   
                    db.session.delete(submissao_existente)


        db.session.commit()
        return jsonify({"mensagem": "Atividade atualizada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar atividade: {e}")
        return jsonify({"erro": "Ocorreu um erro ao atualizar a atividade."}), 500
    



@routes.route("/atividades/<int:id_atividade>", methods=["DELETE"])
def deletar_atividade(id_atividade):
    try:
        atividade = Atividade.query.get(id_atividade)
        if not atividade:
            return jsonify({"erro": "Atividade não encontrada."}), 404

        db.session.delete(atividade)
        db.session.commit()
        return jsonify({"mensagem": "Atividade excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar atividade: {e}")
        return jsonify({"erro": "Ocorreu um erro ao deletar a atividade."}), 500    