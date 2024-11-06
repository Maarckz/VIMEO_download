import re
import subprocess

###################################################################################################
## REDUZIR TAMANHO: ffmpeg -i input_video.mp4 -vf scale=1280:720 -c:a copy output_video_720p.mp4 ##
###################################################################################################z
###############################################################################
## Abrir iFrame do vido em nova aba, Inspecionar e Buscar por "playerConfig" ##
###############################################################################
final = []

def download_video(video_url, output_name):
    try:
        #############################################
        ## Executa o FFmpeg para baixar o vídeo    ##
        #############################################
        command = ["ffmpeg", "-i", video_url, "-c", "copy", output_name]
        subprocess.run(command, check=True)
        print(f"Download concluído: {output_name}")
    except subprocess.CalledProcessError:
        print("Erro ao executar o FFmpeg.")

string = '''

'''

#########################################
## Regex para capturar URLs HLS (m3u8) ##
#########################################
urls = re.findall(r'"url":"(https?://[^"]+)"', string)

###################################################
## Exibindo apenas as URLs que terminam com "ts" ##
###################################################
for url in urls:
    if url.endswith('ts'):
        final.append(url)


#######################################################################
## Recebe o trecho de código e o nome do arquivo de saída do usuário ##
#######################################################################
name = input('Nome do Arquivo: ')
output_name = name+'.mp4'

download_video(final[0],output_name)