from querys.dao_generic import Generic_DAO
import sys
from objetos.usuario import Usuario
import ctypes

class Dao:

    @staticmethod
    def verifica_versao():
        try:
            dao = Generic_DAO()

            sql = "SELECT id_versao, maior, media, menor FROM distribuicao.tb_versao " \
                  "where id_versao = (SELECT MAX(id_versao) FROM distribuicao.tb_versao) ;"

            resultado = dao.abre_result_set(sql)
            maior = str(resultado[0][1])
            media = str(resultado[0][2])
            menor = str(resultado[0][3])
            versao = maior + "." + media + "." + menor
            return versao
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - verifica_versao", 0)


    @staticmethod
    def inserir_dados_gerais(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.originacao_ubs (id, versionamento, tipo_ativo, lei_12431, conv_acoes, esg,
                     nome_emissor, cnpj_emissor, tipo_emissor, nome_coordenador, cnpj_coordenador, coordenador_lider,
                     demais_coordenadores, legislacao_cvm, rito_registro, documento_oferta, valor_emissao, 
                     part_regime_garantia_firme, regime_colocacao, lote_adicional, lote_ad_maximo, series, 
                     destinacao_recursos, rating_emissora, rating_min_oferta, prob_colocacao, justificativa, 
                     esforcos_distrib, ha_garantia, garantia, covenants, permite_resgate_antecip, premio_resgate_antecip, 
                     market_flex_mac_clause, fees_total, fees_canal, fee_canal_forma_cal, outras_fees, balanco_auditado, 
                     empresa_auditoria, balanco_divulgado, rfp,previsao_liquidacao, data_limite_prop, 
                     observacoes, funcionario, data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '""" + Usuario.chave + """' , Now());"""
            print(sql)


            args = []
            args.append(int(item[0]['ID']))
            args.append(int(item[0]['versionamento']))
            args.append(int(item[0]['Tipo de Ativo *']))
            args.append(int(item[0]['Lei 12.431 *']))
            args.append(int(item[0]['Conversível em Ações *']))
            args.append(int(item[0]['ESG *']))
            args.append(str(item[0]['Nome Emissor/ Originador/ Cedente / Devedor *']))
            args.append(int(item[0]['CNPJ Emissor/ Originador/ Cedente / Devedor *']))
            args.append(int(item[0]['Tipo de Emissor *']))
            args.append(str(item[0]['Nome Coordenador *']))
            args.append(int(item[0]['CNPJ Coordenador *']))
            args.append(str(item[0]['Coordenador Líder']))
            args.append(str(item[0]['Demais Coordenadores']))
            args.append(int(item[0]['Legislação CVM *']))
            args.append(int(item[0]['Rito de Registro *']))
            args.append(int(item[0]['Documentos da Oferta *']))
            args.append(round(float(item[0]['Valor da emissão *']), 2))
            args.append(round(float(item[0]['Participação em regime de garantia firme *']), 2))
            args.append(int(item[0]['Regime de Colocação *']))
            args.append(int(item[0]['Lote Adicional? *']))
            args.append(round(float(item[0]['Lote Adicional máximo *']), 2))
            args.append(int(item[0]['Séries *']))
            args.append(str(item[0]['Destinação dos Recursos *']))
            args.append(int(item[0]['Rating da Emissora *']))
            args.append(int(item[0]['Rating Mínimo da Oferta *']))
            args.append(int(item[0]['Probabilidade de colocação *']))
            args.append(str(item[0]['Justificativa *']))
            args.append(int(item[0]['Haverá esforço de distribuição junto ao investidor PF no BB? *']))
            args.append(int(item[0]['Terá garantia? *']))
            args.append(str(item[0]['Garantia *']))
            args.append(str(item[0]['Cláusulas de Vencimento Antecipado/Covenants *']))
            args.append(int(item[0]['Permite resgate antecipado? *']))
            args.append(round(float(item[0]['Prêmio de Resgate antecipado - BFF *']), 2))
            args.append(int(item[0]['Market Flex e Mac Clause *']))
            args.append(round(float(item[0]['Fee total *']), 2))
            args.append(round(float(item[0]['Fee canal *']), 2))
            args.append(int(item[0]['Fee Canal - Forma de Cálculo *']))
            args.append(str(item[0]['Outras fees']))
            args.append(int(item[0]['Balanço Auditado *']))
            args.append(str(item[0]['Empresa de Auditoria *']))
            args.append(int(item[0]['Balanço Divulgado *']))
            args.append(int(item[0]['RFP (Request for Proposal)? *']))
            args.append(str(item[0]['Previsão de liquidação *'])[:10])
            args.append(str(item[0]['Data limite para envio da proposta *'])[:10])
            args.append(str(item[0]['Observações']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_gerais", 0)

    @staticmethod
    def inserir_dados_lastro(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.lastros (id, versionamento, lastro, resolvencia, subordinacao, seguro, 
            lastro_vol_medio, lastro_tic_medio, lastro_conc_carteira, lastro_10_maiores_dev, lastro_vol_total_carteira,
            lastro_prz_medio_carteira, lastro_vol_disp_cessao, lastro_inad_media, lastro_idc_media_pag_atraso, 
            lastro_prz_medio_pag_atraso, lastro_idc_distrato_devol, funcionario, data_log) values (%s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  '""" + Usuario.chave + """' , Now());"""
            print(sql)
            args = []
            args.append(int(item[0]['ID']))
            args.append(int(item[0]['versionamento']))
            if 'Lastro *' in item[0]:
                args.append(str(item[0]['Lastro *']))
            elif 'Lastro' in item[0]:
                args.append(str(item[0]['Lastro']))
            args.append(int(item[0]['Revolvência']))
            if 'Subordinação *' in item[0]:
                args.append(int(item[0]['Subordinação *']))
            elif 'Subordinação' in item[0]:
                args.append(int(item[0]['Subordinação']))
            args.append(int(item[0]['Seguro']))
            args.append(round(float(item[0]['Lastro volume médio']), 2))
            args.append(round(float(item[0]['Lastro ticket médio']), 2))
            args.append(str(item[0]['Lastro nível de concentração da carteira']))
            args.append(str(item[0]['Lastro 10 maiores devedores']))
            if 'Lastro volume total da carteira *' in item[0]:
                args.append(round(float(item[0]['Lastro volume total da carteira *']), 2))
            elif 'Lastro volume total da carteira' in item[0]:
                args.append(round(float(item[0]['Lastro volume total da carteira']), 2))
            args.append(str(item[0]['Lastro prazo médio da carteira']))
            if 'Lastro volume disponível para cessão *' in item[0]:
                args.append(round(float(item[0]['Lastro volume disponível para cessão *']), 2))
            elif 'Lastro volume disponível para cessão' in item[0]:
                args.append(round(float(item[0]['Lastro volume disponível para cessão']), 2))
            args.append(round(float(item[0]['Lastro inadimplência média']), 2))
            args.append(str(item[0]['Lastro índice média de pagamentos em atraso']))
            args.append(str(item[0]['Lastro prazo médio de pagamentos em atraso']))
            args.append(str(item[0]['Lastro índice de distrato ou devoluções']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)
            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_lastro", 0)

    @staticmethod
    def inserir_dados_series(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.series (id, versionamento, serie, tipo, prazo, carencia, pag_principal,
                    ini_pag_principal, carencia_juros, pag_juros, indexador, ref_ntnb, taxa, pub_merc_primario, 
                    pub_merc_secundario, funcionario, data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, '""" + Usuario.chave + """' , Now());"""
            print(sql)

            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(int(item['serie']))
            args.append(int(item['tipo']))
            args.append(round(float(item['prazo']), 2))
            args.append(round(float(item['carencia']), 2))
            args.append(int(item['pag_principal']))
            args.append(int(item['ini_pag_principal']))
            args.append(round(float(item['carencia_juros']), 2))
            args.append(int(item['pag_juros']))
            args.append(int(item['indexador']))
            args.append(str(item['ref_ntnb']))
            args.append(round(float(item['taxa']), 2))
            args.append(int(item['pub_merc_primario']))
            args.append(int(item['pub_merc_secundario']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)
            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_series", 0)

    @staticmethod
    def ids_existentes():
        try:
            dao = Generic_DAO()
            """Query necessária para alimentar o comboBox dos IDs """
            sql = """Select tb1.id, tb1.nome_emissor, tb1.versionamento from distribuicao.originacao_ubs as tb1
                     left join  distribuicao.originacao_ubs as tb2
                     on tb1.id= tb2.id and tb1.versionamento < tb2.versionamento
                     where tb2.versionamento is null;"""
            resultado = dao.abre_result_set(sql)
            #print(resultado)
            #print(len(resultado))
            lista_ID = ['']
            for linha in range(0, len(resultado)):
                ID = str(resultado[linha][0]) + " - " + str(resultado[linha][1])
                print(ID)
                lista_ID.append(ID)
            return lista_ID
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - ids_existentes", 0)

    @staticmethod
    def operacoes_existentes():
        try:
            dao = Generic_DAO()
            """Query necessária para alimentar a lista de operações existentes """
            sql = """select o.id,
                            Coalesce(o.nome_emissor, ''),
                            Coalesce(o.cnpj_emissor, 0),
                            Coalesce(a.nome_ativo, ''),
                            Coalesce(o.valor_emissao, 0.0),
                            Coalesce(r.nome_status, '')
                        from distribuicao.originacao_ubs as o
                        left join distribuicao.status_operacao as s on s.id = o.id
                        left join distribuicao.status as r on r.id_status = s.status
                        left join distribuicao.ativos as a on a.id_ativo = o.tipo_ativo
                        where o.versionamento = (select max(versionamento) from distribuicao.originacao_ubs as x where x.id = o.id)
                        order by o.nome_emissor;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - ids_operacoes", 0)

    @staticmethod
    def funcis_bbbi():
        try:
            dao = Generic_DAO()
            """Query necessária para alimentar o comboBox dos funcis """
            sql = "select nome from funcionalismo.funci_bbbi"
            resultado = dao.abre_result_set(sql)
            #print(resultado)
            #print(len(resultado))
            lista_funci = ['']
            for linha in range(0, len(resultado)):
                funci = str(resultado[linha][0])
                print(funci)
                lista_funci.append(funci)
            return lista_funci
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcis_bbbi", 0)

    @staticmethod
    def consultar_versionamento(id):
        try:
            dao = Generic_DAO()
            """Query necessária para verificar o versionamemto do ID selecionado """
            sql = "select max(versionamento) from distribuicao.originacao_ubs where id = " + id + ";"
            resultado = dao.abre_result_set(sql)
            #print(resultado)
            versionamento = int(resultado[0][0])
            return versionamento
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - consultar_versionamento", 0)

    @staticmethod
    def informacoes_id(id):
        try:
            dao = Generic_DAO()
            sql = """select a.nome_ativo tipo_ativo,
                            o.nome_emissor,
                            o.cnpj_emissor,
                            c.nome_coordenador,
                            o.cnpj_coordenador,
                            o.coordenador_lider,
                            o.demais_coordenadores,
                            o.lei_12431,
                            o.conv_acoes,
                            o.lote_adicional,
                            o.esforcos_distrib,
                            o.ha_garantia,
                            o.permite_resgate_antecip,
                            o.market_flex_mac_clause,
                            o.balanco_auditado,
                            o.balanco_divulgado,
                            o.rfp,
                            t.tipo_legislacao,
                            r.tipo_registro,
                            d.tipo_oferta,
                            b.tipo_regime,
                            f.classificacao as rating_emissao,
                            g.classificacao as rating_min_oferta,
                            p.classificacao as prob_colocacao,
                            e.tipo_emissor,
                            o.valor_emissao,
                            o.destinacao_recursos, 
                            o.part_regime_garantia_firme, 
                            o.lote_ad_maximo, 
                            o.premio_resgate_antecip, 
                            o.garantia, 
                            o.fees_total, 
                            o.fees_canal, 
                            o.outras_fees, 
                            o.series, 
                            o.previsao_liquidacao, 
                            o.data_limite_prop, 
                            o.empresa_auditoria, 
                            o.justificativa,
                            o.covenants, 
                            o.observacoes,
                            o.versionamento,
                            o.esg,
                            h.nome_fee                        
                    from distribuicao.originacao_ubs as o
                    inner join distribuicao.ativos as a on o.tipo_ativo = a.id_ativo 
                    inner join distribuicao.coordenador as c on o.nome_coordenador = c.id_coordenador
                    inner join distribuicao.legislacao_cvm as t on o.legislacao_cvm = t.id_legislacao
                    inner join distribuicao.rito_registro as r on o.rito_registro = r.id_registro
                    inner join distribuicao.doc_oferta as d on o.documento_oferta = d.id_oferta
                    inner join distribuicao.regime_colocacao as b on o.regime_colocacao = b.id_regime
                    inner join distribuicao.rating as f on o.rating_emissora = f.id_rating
                    inner join distribuicao.rating as g on o.rating_min_oferta = g.id_rating
                    inner join distribuicao.prob_colocacao as p on o.prob_colocacao = p.id_colocacao
                    inner join distribuicao.emissor as e on o.tipo_emissor = e.id_emissor
                    inner join distribuicao.fee_canal_form_cob as h on o.fee_canal_forma_cal = h.id_fee
                    where o.versionamento = (select max(versionamento) from distribuicao.originacao_ubs where id = """ + id + """) 
                    and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_id", 0)

    @staticmethod
    def inserir_dados_gerais_versionamento(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.originacao_ubs (id, versionamento, tipo_ativo, lei_12431, conv_acoes, esg,
                     nome_emissor, cnpj_emissor, tipo_emissor, nome_coordenador, cnpj_coordenador, coordenador_lider,
                     demais_coordenadores, legislacao_cvm, rito_registro, documento_oferta, valor_emissao, 
                     part_regime_garantia_firme, regime_colocacao, lote_adicional, lote_ad_maximo, series, 
                     destinacao_recursos, rating_emissora, rating_min_oferta, prob_colocacao, justificativa, 
                     esforcos_distrib, ha_garantia, garantia, covenants, permite_resgate_antecip, premio_resgate_antecip, 
                     market_flex_mac_clause, fees_total, fees_canal, fee_canal_forma_cal, outras_fees, balanco_auditado, 
                     empresa_auditoria, balanco_divulgado, rfp,previsao_liquidacao, data_limite_prop, 
                     observacoes, funcionario, data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '""" + Usuario.chave + """' , Now());"""
            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(int(item['tipo_ativo']))
            args.append(int(item['lei_12431']))
            args.append(int(item['conv_acoes']))
            args.append(int(item['esg']))
            args.append(str(item['nome_emissor']))
            args.append(int(item['cnpj_emissor']))
            args.append(int(item['tipo_emissor']))
            args.append(str(item['nome_coordenador']))
            args.append(int(item['cnpj_coordenador']))
            args.append(str(item['coordenador_lider']))
            args.append(str(item['demais_coordenadores']))
            args.append(int(item['legislacao_cvm']))
            args.append(int(item['rito_registro']))
            args.append(int(item['documento_oferta']))
            args.append(round(float(item['valor_emissao']), 2))
            args.append(round(float(item['part_regime_garantia_firme']), 2))
            args.append(int(item['regime_colocacao']))
            args.append(int(item['lote_adicional']))
            args.append(round(float(item['lote_ad_maximo']), 2))
            args.append(int(item['series']))
            args.append(str(item['destinacao_recursos']))
            args.append(int(item['rating_emissora']))
            args.append(int(item['rating_min_oferta']))
            args.append(int(item['prob_colocacao']))
            args.append(str(item['justificativa']))
            args.append(int(item['esforcos_distrib']))
            args.append(int(item['ha_garantia']))
            args.append(str(item['garantia']))
            args.append(str(item['covenants']))
            args.append(int(item['permite_resgate_antecip']))
            args.append(round(float(item['premio_resgate_antecip']), 2))
            args.append(int(item['market_flex_mac_clause']))
            args.append((round(float(item['fees_total']), 2)))
            args.append((round(float(item['fees_canal']), 2)))
            args.append(int(item['fee_canal_forma_cal']))
            args.append(str(item['outras_fees']))
            args.append(int(item['balanco_auditado']))
            args.append(str(item['empresa_auditoria']))
            args.append(int(item['balanco_divulgado']))
            args.append(int(item['rfp']))
            args.append(str(item['previsao_liquidacao'])[:10])
            args.append(str(item['data_limite_prop'])[:10])
            args.append(str(item['observacoes']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_gerais_versionamento", 0)

    @staticmethod
    def inserir_dados_lastro_versionamento(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.lastros (id, versionamento, resolvencia, subordinacao, seguro, lastro,
                    lastro_vol_medio, lastro_tic_medio, lastro_conc_carteira, lastro_10_maiores_dev, lastro_vol_total_carteira,
                    lastro_prz_medio_carteira, lastro_vol_disp_cessao, lastro_inad_media, lastro_idc_media_pag_atraso,
                    lastro_prz_medio_pag_atraso, lastro_idc_distrato_devol, funcionario, data_log) values 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(int(item['resolvencia']))
            args.append(int(item['subordinacao']))
            args.append(int(item['seguro']))
            args.append(int(item['lastro']))
            args.append(float(item['lastro_vol_medio']))
            args.append(float(item['lastro_tic_medio']))
            args.append(str(item['lastro_conc_carteira']))
            args.append(str(item['lastro_10_maiores_dev']))
            args.append(float(item['lastro_vol_total_carteira']))
            args.append(str(item['lastro_prz_medio_carteira']))
            args.append(float(item['lastro_vol_disp_cessao']))
            args.append(float(item['lastro_inad_media']))
            args.append(str(item['lastro_idc_media_pag_atraso']))
            args.append(str(item['lastro_prz_medio_pag_atraso']))
            args.append(str(item['lastro_idc_distrato_devol']))
            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_lastro_versionamento", 0)

    @staticmethod
    def inserir_dados_series_versionamento(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.series (id, versionamento, serie, tipo, prazo, carencia, pag_principal, ini_pag_principal,
                    carencia_juros, pag_juros, indexador, ref_ntnb, taxa, pub_merc_primario, pub_merc_secundario , funcionario, 
                    data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(int(item['serie']))
            args.append(int(item['tipo']))
            args.append(float(item['prazo']))
            args.append(float(item['carencia']))
            args.append(int(item['pag_principal']))
            args.append(float(item['ini_pag_principal']))
            args.append(float(item['carencia_juros']))
            args.append(int(item['pag_juros']))
            args.append(int(item['indexador']))
            args.append(str(item['ref_ntnb']))
            args.append(float(item['taxa']))
            args.append(int(item['pub_merc_primario']))
            args.append(int(item['pub_merc_secundario']))
            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_series_versionamento", 0)

    @staticmethod
    def inserir_dados_status(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.status_operacao (id, status, motivo, versao, funci, dt_log)
                    values (%s, %s, %s, %s, '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['status']))
            args.append(str(item['motivo']))
            args.append(int(item['versao']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_estudo", 0)

    @staticmethod
    def inserir_dados_estudo(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.estudo (id, versionamento, assessor_bbbi, estrategia_distribuicao,
                     consulta_viabilidade_tvm, consulta_upb, pz_estmd_vnd_secun_upb, impacto_prob, limite_global_rc, 
                     limite_especifico_rc, dt_consulta_viab_tvm, dt_consulta_upb, dt_proposta_negocios, 
                     te_retorno_consulta_viabilidade_tvm, te_retorno_consulta_upb, te_resultado_proposta_negocios, 
                     funcionario, data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(str(item['assessor_bbbi']))
            args.append(str(item['estrategia_distribuicao']))
            args.append(str(item['consulta_viabilidade_tvm']))
            args.append(str(item['consulta_upb']))
            args.append(float(item['pz_estmd_vnd_secun_upb']))
            args.append(float(item['impacto_prob']))
            args.append(float(item['limite_global_rc']))
            args.append(float(item['limite_especifico_rc']))
            args.append(str(item['dt_consulta_viab_tvm'])[:10])
            args.append(str(item['dt_consulta_upb'])[:10])
            args.append(str(item['dt_proposta_negocios'])[:10])
            args.append(str(item['te_retorno_consulta_viabilidade_tvm']))
            args.append(str(item['te_retorno_consulta_upb']))
            args.append(str(item['te_resultado_proposta_negocios']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_estudo", 0)

    @staticmethod
    def inserir_dados_aprovacao(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.aprovacao (id, versionamento, nr_estudo_tecnico, dt_apvcao_estd_tcnco,
                    valor_gf_apvda_estdo_tcnco, funcionario, data_log) 
                    values (%s, %s, %s, %s, %s, '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(int(item['nr_estudo_tecnico']))
            args.append(str(item['dt_apvcao_estd_tcnco'])[:10])
            args.append(float(item['valor_gf_apvda_estdo_tcnco']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_aprovacao", 0)

    @staticmethod
    def inserir_dados_estruturacao(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.estruturacao (id, versionamento, nm_sec_adm, cnpj_sec_adm, nm_agente_fid,
                    cnpj_agente_fid, especie, indexador, percent_spread, nr_emissao, classe, series, taxa_op, pu_emissao,
                    fee_estruturacao, fee_sucesso, fee_garant_firme, fees_outras, fee_distrib_canal, dt_emissao, 
                    dt_venc_emissao, dt_inicial_juros, dt_final_juros, dt_inicial_amort, dt_final_amort, dt_bookbuilding,
                    dt_liquidacao, funcionario, data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  '""" + Usuario.chave + """' , Now());"""

            print(sql)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))

            args.append(str(item['nm_sec_adm']))
            args.append(str(item['cnpj_sec_adm']))
            args.append(str(item['nm_agente_fid']))
            args.append(str(item['cnpj_agente_fid']))

            args.append(int(item['especie']))
            args.append(int(item['indexador']))
            args.append(int(item['percent_spread']))
            args.append(int(item['nr_emissao']))
            args.append(int(item['classe']))
            args.append(int(item['series']))

            args.append(float(item['taxa_op']))
            args.append(float(item['pu_emissao']))
            args.append(float(item['fee_estruturacao']))
            args.append(float(item['fee_sucesso']))
            args.append(float(item['fee_garant_firme']))
            args.append(float(item['fees_outras']))

            args.append(str(item['fee_distrib_canal']))

            args.append(str(item['dt_emissao'])[:10])
            args.append(str(item['dt_venc_emissao'])[:10])
            args.append(str(item['dt_inicial_juros'])[:10])
            args.append(str(item['dt_final_juros'])[:10])
            args.append(str(item['dt_inicial_amort'])[:10])
            args.append(str(item['dt_final_amort'])[:10])
            args.append(str(item['dt_bookbuilding'])[:10])
            args.append(str(item['dt_liquidacao'])[:10])

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_estruturacao", 0)


    @staticmethod
    def inserir_dados_liquidacao(item):
        dao = Generic_DAO()

        try:
            sql = """INSERT INTO distribuicao.liquidacao (id, versionamento, codigo_ativo, insi, pu_liquidacao, 
                    grtia_frm_exercida, vol_adquirido, qtd_vlrs_mob_adq,
                    porcent_sobras, prob_col_realizada, demanda_upb_merc_pri, aloc_upb_merc_pri, fee_upb_merc_pri,
                    fee_retida_dist_merc_sec, fee_recebida_bbbi, carteira_rm, grupo_rm, livro_rm, categoria_contabil,
                    camara_registro, codigo_grupo, grupo, codigo_livro, livro, cod_sub_livro, sub_livro, funcionario, 
                    data_log) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  '""" + Usuario.chave + """' , Now());"""

            print(sql)
            print(item)
            args = []
            args.append(int(item['id']))
            args.append(int(item['versionamento']))
            args.append(str(item['codigo_ativo']))
            args.append(str(item['insi']))
            args.append(float(item['pu_liquidacao']))
            args.append(int(item['grtia_frm_exercida']))
            args.append(float(item['vol_adquirido']))
            args.append(float(item['qtd_vlrs_mob_adq']))
            args.append(float((item['porcent_sobras']).replace("%", "")))
            args.append(str(item['prob_col_realizada']))
            args.append(float(item['demanda_upb_merc_pri']))
            args.append(float(item['aloc_upb_merc_pri']))
            args.append(float(item['fee_upb_merc_pri']))
            args.append(float(item['fee_retida_dist_merc_sec']))
            args.append(float(item['fee_recebida_bbbi']))
            args.append(str(item['carteira_rm']))
            args.append(str(item['grupo_rm']))
            args.append(str(item['livro_rm']))
            args.append(str(item['categoria_contabil']))
            args.append(str(item['camara_registro']))
            args.append(int(item['codigo_grupo']))
            args.append(str(item['grupo']))
            args.append(int(item['codigo_livro']))
            args.append(str(item['livro']))
            args.append(str(item['cod_sub_livro']))
            args.append(str(item['sub_livro']))

            print(sql)
            resultado = dao.executa_sql(sql, args)

            print(resultado)

            return resultado

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - inserir_dados_liquidacao", 0)


    @staticmethod
    def verificar_dados_originacao(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.originacao_ubs where versionamento = 
                   (select max(versionamento) from distribuicao.originacao_ubs where id = """ + id + """) 
                   and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - verificar_dados_originacao", 0)


    @staticmethod
    def informacoes_status(id):
        try:
            dao = Generic_DAO()
            sql = """select s.nome_status, o.motivo 
                    from distribuicao.status_operacao as o
                    inner join distribuicao.status as s on s.id_status = o.status 
                    where dt_log = (select max(dt_log) from distribuicao.status_operacao where id = """ + id + """) 
                    and versao = (select max(versao) from distribuicao.status_operacao where id = """ + id + """)
                    and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_status", 0)

    @staticmethod
    def informacoes_cliente(cnpj):
        try:
            dao = Generic_DAO()
            sql = """select c.*,
                    s.aprovado as aprovado_tvm,
                    s.disponivel as disponivel_tvm,
                    r.aprovado as aprovado_distribuicao,
                    r.disponivel as disponivel_distribuicao
                    from dados_externos.clientes as c
                    left join dados_externos.sublimites as s on c.mci = s.mci and s.sublimite = 213
                    left join dados_externos.sublimites as r on c.mci = r.mci and r.sublimite = 231
                    where c.cnpj = """ + cnpj + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_cliente", 0)

    @staticmethod
    def informacoes_lastro(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.lastros where versionamento = 
                   (select max(versionamento) from distribuicao.lastros where id = """ + id + """) 
                   and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_lastro", 0)

    @staticmethod
    def informacoes_series(id):
        try:
            dao = Generic_DAO()
            sql = """select a.nome_ativo,
                            s.prazo,
                            s.carencia,
                            f.frequencia as pag_principal,
                            s.ini_pag_principal,
                            s.carencia_juros,
                            g.frequencia as pag_juros,
                            d.tipo_indice as indexador,
                            s.ref_ntnb,
                            s.taxa,
                            i.tipo_investidor as pub_merc_primario,
                            j.tipo_investidor as pub_merc_secundario
                        from distribuicao.series as s
                        inner join distribuicao.frequencia as f on f.id_freq = s.pag_principal
                        inner join distribuicao.frequencia as g on g.id_freq = s.pag_juros
                        inner join distribuicao.investidor as i on i.id_investidor = s.pub_merc_primario
                        inner join distribuicao.investidor as j on j.id_investidor = s.pub_merc_secundario
                        inner join distribuicao.indices as d on d.id_indice = s.indexador
                        inner join distribuicao.ativos as a on a.id_ativo = s.tipo
                        where versionamento = (select max(versionamento) from distribuicao.series where id = """ + id + """)
                        and id = """ + id + """ order by s.serie;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_series", 0)

    @staticmethod
    def informacoes_estudo(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.estudo where versionamento = 
                   (select max(versionamento) from distribuicao.estudo where id = """ + id + """) 
                   and data_log = (select max(data_log) from distribuicao.estudo where id = """ + id + """)
                   and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_estudo", 0)

    @staticmethod
    def informacoes_aprovacao(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.aprovacao where versionamento = 
                   (select max(versionamento) from distribuicao.aprovacao where id = """ + id + """) 
                   and data_log = (select max(data_log) from distribuicao.aprovacao where id = """ + id + """)
                   and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_aprovacao", 0)

    @staticmethod
    def informacoes_estruturacao(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.estruturacao where versionamento = 
                      (select max(versionamento) from distribuicao.estruturacao where id = """ + id + """) 
                      and data_log = (select max(data_log) from distribuicao.estruturacao where id = """ + id + """)
                      and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_estruturacao", 0)

    @staticmethod
    def informacoes_liquidacao(id):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.liquidacao where versionamento = 
                      (select max(versionamento) from distribuicao.liquidacao where id = """ + id + """) 
                      and data_log = (select max(data_log) from distribuicao.liquidacao where id = """ + id + """)
                      and id = """ + id + """;"""
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_liquidacao", 0)

    @staticmethod
    def consultar_dados_base(cnpj, valor):
        try:
            dao = Generic_DAO()
            sql = """select * from distribuicao.originacao_ubs where cnpj_emissor =  """ + cnpj + """ 
            and valor_emissao = """ + valor + """;"""
            print(sql)
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_liquidacao", 0)

    @staticmethod
    def verificar_ultimo_cnpj_por_id(id):
        try:
            dao = Generic_DAO()
            sql = """select cnpj_emissor from distribuicao.originacao_ubs where id = """ + id + """ and
            data_log = (select max(data_log) from distribuicao.originacao_ubs where id = """ + id + """);"""
            print(sql)
            resultado = dao.abre_result_set(sql)
            print(resultado)
            return resultado[0][0]
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - informacoes_liquidacao", 0)
