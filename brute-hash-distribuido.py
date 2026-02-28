import hashlib
import time
import string
import itertools
from dask.distributed import Client, as_completed

def hasheandoMD5(senha):
    senha = senha.encode('utf-8')
    md5 = hashlib.md5(senha)
    print("Hash md5: " + md5.hexdigest())
    return md5.hexdigest()

def hasheandoSHA1(senha):
    senha = senha.encode('utf-8')
    sha1 = hashlib.sha1(senha)
    print("Hash sha1: " + sha1.hexdigest())
    return sha1.hexdigest()

def workerBruteForce (prefixo, hashAlvo, tamanhoSenha, caracteres):
    for tamanhos in range(1, tamanhoSenha + 1):
        print(f"Testando senhas com {tamanhoSenha} caractere(s)...")

        if tamanhoSenha == 0 :
            senha_testada = prefixo
            hash_testado1 = hashlib.md5(senha_testada.encode('utf-8')).hexdigest()
            hash_testado2 = hashlib.sha1(senha_testada.encode('utf-8')).hexdigest()
            if (hash_testado1 == hashAlvo) or (hash_testado2 == hashAlvo):
                return senha_testada

        # itertools.product gera todas as combinações possíveis
        for tentativa in itertools.product(caracteres, repeat=tamanhoSenha):
            senha_testada = prefixo + ''.join(tentativa)

            # Gera o hash da tentativa atual
            hash_testado1 = hashlib.md5(senha_testada.encode('utf-8')).hexdigest()
            hash_testado2 = hashlib.sha1(senha_testada.encode('utf-8')).hexdigest()

            # Compara o hash gerado com o hash alvo
            if (hash_testado1 == hashAlvo) or (hash_testado2 == hashAlvo):
                return senha_testada

    return None

def bruteForceHash(client, hashAlvo, tamanho):
    print(f"\nIniciando Força Bruta para o hash: {hashAlvo}")
    caracteres = string.ascii_lowercase + string.digits + string.ascii_uppercase #aqui considerei apenas letras maiúsculas, minúsculas e números

    trabalhos = []

    print(f"Separando o hash {len(caracteres)} tarefas")

    for c in caracteres:
        tamanhoRestante = tamanho - 1 if tamanho > 1 else 0
        #agora enviar o trabalho a função de workerBruteForce para o cluster
        trabalho = client.submit(workerBruteForce, c, hashAlvo, tamanhoRestante, caracteres)
        trabalhos.append(trabalho)

    for trabalho in as_completed(trabalhos):
        resultado = trabalho.result() #recebe alguma coisa do worker
        if resultado is not None:
            print(f"\n[+] Sucesso! Senha: {resultado}")
            client.cancel(trabalhos)
            return resultado


if __name__ == "__main__":
    enderecoMaster = 'tcp://192.168.4.234:8786'
    client = Client(enderecoMaster)
    print(f"Conectando ao cluster, nó mestre: {client}")
    #--------------------------------------

    senha = input("Digite sua senha: ")
    tamanhoSenha = len(str(senha))
    print("\nSenha digitada: " + senha)
    hashMD5 = hasheandoMD5(senha)
    hashSHA1 = hasheandoSHA1(senha)


    inicioTempo = time.time()
    hashEncontrado = bruteForceHash(client, hashMD5, tamanhoSenha)
    print(f"Tempo para achar hash MD5: " + str(time.time() - inicioTempo) + "\nSenha achada: " + str(hashEncontrado))
    hashEncontrado = bruteForceHash(client, hashSHA1, tamanhoSenha)
    print(f"Tempo para achar hash SHA1: " + str(time.time() - inicioTempo) + "\nSenha achada: " + str(hashEncontrado))

