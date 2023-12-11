import pandas as pd
import openai

# Configuração inicial
openai.api_key = 'sua_api_key'
prompt_base = "Analisar o seguinte parecer financeiro e determinar se deve ser arquivado ou investigado: "
insights = []

def obter_amostra_para_resumo(dataframe, tamanho_amostra=100):
    erros = dataframe[dataframe['analiseHumano'] != dataframe['analiseIA']]
    return erros.sample(min(tamanho_amostra, len(erros)))

def categorizar_erros(row):
    if row['analiseHumano'] != row['analiseIA']:
        if row['analiseIA'] == 'investigar':
            return 'Falso Positivo'
        else:
            return 'Falso Negativo'
    return 'Correto'

def gerar_prompt_baseado_em_insights(prompt_base, insights):
    prompt_atualizado = prompt_base
    for insight in insights:
        prompt_atualizado += f"\n{insight}"
    return prompt_atualizado

def processar_nova_amostra(dataframe, prompt_base):
    amostra = obter_amostra_para_resumo(dataframe)
    amostra['tipo_erro'] = amostra.apply(categorizar_erros, axis=1)
    texto_para_resumo = "\n".join(f"{row['parecer']} - Erro: {row['tipo_erro']}" for index, row in amostra.iterrows())
    
    prompt = gerar_prompt_baseado_em_insights(prompt_base, insights)
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"{prompt}\nPor favor, identifique padrões nos seguintes erros:\n{texto_para_resumo}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def atualizar_insights(novos_insights):
    insights.extend(novos_insights)

# Carregar os dados
df = pd.read_csv('caminho_para_sua_planilha.csv')

# Processar a primeira amostra
sumario_erros = processar_nova_amostra(df, prompt_base)

# Aqui você deveria interpretar manualmente o sumário de erros para obter insights
# Por exemplo: novos_insights = ["Insight baseado no sumário de erros"]
# Atualizar insights com base na sua análise
# atualizar_insights(novos_insights)

# Continuar o processo para novas amostras...
