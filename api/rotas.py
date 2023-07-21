from flask import json, jsonify, request,g

def health():
    """
    Status da API
    """
    responseBody = {
        "status": "Service Running"
    }
    return jsonify(responseBody)

def listagem_despesas():
    try:
        query = """SELECT * FROM despesas"""
        g.cursor.execute(query)
        rows = g.cursor.fetchall()
        data = []
        for row in rows:
            data.append(row)

    
        resposta= {
            'data': data,
            "success": True
        }
        return jsonify(resposta)
    
    except Exception as error:
        resposta = {
            "data": str(error),
            "success": False
        }
        
        return jsonify(resposta)
    
def cadastro_despesas():
    try:
        valor = request.form['valor']
        data_compra = request.form['data_compra']
        descricao = request.form['descricao']
        tipo_pagamento_id = request.form['tipo_pagamento_id']
        categoria_id = request.form['categoria_id']
        query = 'INSERT INTO despesas(valor, data_compra, descricao, tipo_pagamento_id, categoria_id) VALUES (?,?,?,?,?)'
        g.cursor.execute(query, [valor, data_compra, descricao, tipo_pagamento_id, categoria_id])
        g.conexao_com_banco.commit()
        # pegando último id 
        ultimo_id = g.cursor.lastrowid
        resposta = {
                'data':ultimo_id,
                "success": True,
            }
        return resposta
    
    except Exception as error:
        resposta = {
           'data': str(error),
            "success": False
        }
        
        return jsonify(resposta)
