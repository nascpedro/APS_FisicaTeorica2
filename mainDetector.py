#APS Física Teórica 2, por Pedro Eugênio Marin do Nascimento
#Primeira parte:
import cv2
import numpy as np

# Abre o video:
captura = cv2.VideoCapture('capturaPendulo.mp4')

# Verifica se o video carregou corretamente:
if not captura.isOpened():
    print("Erro ao abrir video")
    exit()

contador_frames = 0
fps = captura.get(cv2.CAP_PROP_FPS)
Tempo_por_frame = 1 / fps
continua = True 

# Criar uma pasta "data" antes!

frameAtual = 0

# Lista para armazenar todas as posições x
posicoes_x = []

while continua:
    ret, frame = captura.read()

    if ret:
        # Grava as imagens extraídas do video
        nome = './data/frame' + str(frameAtual) + '.jpg'
        print('Criando...' + nome)
        
        # Antes de salvar as imagens é necessário convertê-la para escalas de cinza e daí para uma imagem binária
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binaria = cv2.threshold(cinza, 70, 255, cv2.THRESH_BINARY_INV)

        # Para achar o pêndulo na imagem binarizada, deve-se obter o maior contorno dessa:
        contornos, _ = cv2.findContours(binaria, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        #Relação de conversão 
        diametro_real = 0.04 #(m)
        diametro_pendulo_pixels = 44 #(px)
        pixels_por_metro = diametro_pendulo_pixels / diametro_real

        if contornos:
            # Maior contorno:
            c = max(contornos, key=cv2.contourArea)
            # M funciona como um dicionário, recebendo diversos momentos, que são relações geométricas da figura da massa:
            M = cv2.moments(c)
            if M["m00"] != 0:  # m00 é sobre a área da figura, ela não pode ser nula
                # Calcular o centro do contorno
                cX = int(M["m10"] / M["m00"])  # m10 indica a soma das coordenadas x dos pontos do contorno
                cY = int(M["m01"] / M["m00"])  # m01 indica a soma das coordenadas y dos pontos do contorno
                
                posicao_x_metros = cX / pixels_por_metro
                posicoes_x.append(posicao_x_metros)  # Adicionar a posição à lista para posterior cálculo da média
                
                # Desenha um círculo no centro de massa
                raio= 1
                cv2.circle(frame, (cX, cY), raio, (255, 0, 0), 2)
                
        cv2.imwrite(nome, frame)
        frameAtual += 1
    #Mostra os frames criados em sequencia, como se fosse um video
        cv2.imshow('Video original', frame)
        cv2.imshow('Video em preto e branco', cinza)
        cv2.imshow('Video Binarizado', binaria)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            continua = False
    else:
        continua = False

# Calcular a posição média
media_posicao_x = np.mean(posicoes_x)

# Ajustar as posições subtraindo a média, para obter valores que variam de [-A, +A]
posicoes_x_ajustadas = [x - media_posicao_x for x in posicoes_x]

# Salvar os dados ajustados no arquivo
with open('dados_ajustados.txt', 'w') as file:
    file.write("Tempo(s)\tPosicao_x(m)\n")
    for i in range(len(posicoes_x_ajustadas)):
        tempo = i * Tempo_por_frame
        file.write(f"{tempo:.2f}\t{posicoes_x_ajustadas[i]:.4f}\n")

# Libera o vídeo e fecha as janelas
captura.release()
cv2.destroyAllWindows()

# Fecha o arquivo depois do loop acabar
file.close()











