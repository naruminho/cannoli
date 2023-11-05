from cannoli import Cannoli 

fake_data = Cannoli()
prompt = ("Generate a list of sentences about a restaurant's quality. "
          "There should be an equal number of positive and negative sentences. "
          "Prepend each sentence with a '1' for positive and a '0' for negative. "
          "Format: sentence|number")


def generate_reviews(prompt, n):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50*n,
            n=n,
            stop=["\n"],
            temperature=0.7
        )
        # Checar se a resposta contém algum erro.
        if response.get('error'):
            print(f"Erro na API: {response['error']['message']}")
            return None

        # Supondo que a resposta foi um sucesso e contém o campo 'choices'.
        generated_text = response.choices[0].text.strip()
        return generated_text

    except Exception as e:
        # Tratar qualquer exceção que ocorra durante a chamada da API ou processamento da resposta.
        print(f"Ocorreu um erro: {str(e)}")
        return None

# Exemplo de uso:


generated_reviews = generate_reviews(prompt, 5)

if generated_reviews:
    print(generated_reviews)
else:
    print("Não foi possível gerar as revisões.")

####################################################

def get_restaurant_review_phrases(num_phrases=100):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Generate a list of {num_phrases} sentences about a restaurant's quality. 
               There should be an equal number of positive and negative sentences. 
               Add a '1' for positive and a '0' for negative at the end of the each sentence.
               Format: sentence|number""",
        temperature=0.7,
        max_tokens=1000,
        n=1
    )
    # A resposta gerada será um texto único, então precisamos dividi-lo em frases.
    generated_text = response.choices[0].text.strip()
    phrases = generated_text.split('\n')

    # Agora, vamos garantir que temos o número exato de frases solicitadas.
    positive_phrases = [phrase for phrase in phrases if phrase.endswith('|1')]
    negative_phrases = [phrase for phrase in phrases if phrase.endswith('|0')]

    # Pode ser que a API não retorne o número exato de frases solicitadas, então isso é um ajuste.
    min_phrases = min(len(positive_phrases), len(negative_phrases), num_phrases // 2)
    final_phrases = positive_phrases[:min_phrases] + negative_phrases[:min_phrases]

    # Imprimir as frases na tela.
    for i, phrase in enumerate(final_phrases):
        print(i, phrase)

# Chamando a função
get_restaurant_review_phrases(10)

