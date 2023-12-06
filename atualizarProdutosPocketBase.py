import cx_Oracle
import pocketbase
import timeit
from credenciais import dados

client = pocketbase.Client(dados['endereco'])
user = client.admins.auth_with_password(dados['email'], dados['senha'])

# Obtendo dados atualizados do Banco de Dados Oracle
def obterDados():
    print('OBTENDO DADOS DO BANCO - ORACLE')
    connection = cx_Oracle.connect(dados['url_conn_azul'])
    cursor = connection.cursor()
    cursor.execute("""
                SELECT p.codprod, p.descricao, p.embalagem, p.unidade, p.codfab, p.pesoliq, 
                    p.pesobruto, p.modulo, p.rua, p.numero, p.apto, p.tipoalturapalete, p.alturapal,
                    p.lastropal, p.qttotpal, p.alturam3, p.larguram3, p.comprimentom3, p.volume,
                    p.gtincodauxiliartrib, p.codauxiliartrib, p.gtincodauxiliar, p.codauxiliar,
                    p.gtincodauxiliar2, p.codauxiliar2, e.qtestger, e.qtindeniz, 
                    (NVL(e.qtbloqueada, 0) - NVL(e.qtindeniz, 0)) AS qtbloqueada, e.qtreserv,
                    (PKG_ESTOQUE.ESTOQUE_DISPONIVEL(e.CODPROD, e.CODFILIAL, 'V', NULL, 'S')) AS qtdisponivel, 
                    TO_CHAR(e.dtultent, 'DD/MM/YYYY') AS dtultent
                    FROM pcprodut p JOIN pcest e ON p.codprod = e.codprod
                    WHERE e.codfilial = 1 AND p.modulo = 1 AND p.rua < 51""")
    consulta = cursor.fetchall()
    cursor.close()
    connection.close()
    print('DADOS OBTIDOS - ORACLE')
    return consulta

# Adicionando os dados atulizados ao Banco de Dados Pocketbase
# 1 - Apagando todos os dados anteriores
# 2 - Inserindo os dados atualizados
def adicionarDadosBanco(consulta):
    print('APAGANDO DADOS ANTIGOS - POCKETBASE')
    response = client.collection('produto').get_full_list()
    for produto in response:
        client.collection('produto').delete(produto.id)
    print('DADOS APAGADOS - POCKETBASE')
    print('INSERINDO DADOS - POCKETBASE')
    for produto in consulta:
        codprod, descricao, embalagem, unidade, codfab, pesoliq, pesobruto, modulo, rua, numero, apto, \
            tipoalturapalete, alturapal, lastropal, qttotpal, alturam3, larguram3, comprimentom3, volume, \
                gtincodauxiliartrib, codauxiliartrib, gtincodauxiliar, codauxiliar, gtincodauxiliar2, codauxiliar2, qtestger, \
                    qtindeniz, qtbloqueada, qtreserv, qtdisponivel, dtultent = produto
        
        client.collection('produto').create({
            "codprod": codprod,
            "descricao" : descricao,
            "embalagem" : embalagem,
            "unidade" : unidade,
            "codfab" : codfab,
            "pesoliq" : pesoliq,
            "pesobruto" : pesobruto,
            "modulo" : modulo,
            "rua" : rua,
            "numero" : numero,
            "apto" : apto,
            "tipoalturapalete" : tipoalturapalete,
            "alturapal" : alturapal,
            "lastropal" : lastropal,
            "qttotpal" : qttotpal,
            "alturam3" : alturam3,
            "larguram3" : larguram3,
            "comprimentom3" : comprimentom3,
            "volume" : volume,
            "gtincodauxiliartrib" : gtincodauxiliartrib,
            "codauxiliartrib" : codauxiliartrib,
            "gtincodauxiliar" : gtincodauxiliar,
            "codauxiliar" : codauxiliar,
            "gtincodauxiliar2" : gtincodauxiliar2,
            "codauxiliar2" : codauxiliar2,
            "qtestger" : qtestger,
            "qtindeniz" : qtindeniz,
            "qtbloqueada" : qtbloqueada,
            "qtreservada" : qtreserv,
            "qtdisponivel" : qtdisponivel,
            "dtultent": dtultent
        })
    print('DADOS INSERIDOS - POCKETBASE')

def atualizarBanco():
    print('INICIADO')
    adicionarDadosBanco(obterDados())
    print('FINALIZADO')

tempo = timeit.timeit(atualizarBanco, number=1)
print(tempo)
