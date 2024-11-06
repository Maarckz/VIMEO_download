import re
import subprocess

###################################################################################################
## REDUZIR TAMANHO: ffmpeg -i input_video.mp4 -vf scale=1280:720 -c:a copy output_video_720p.mp4 ##
###################################################################################################z

###############################################################################
## Abrir iFrame do vido em nova aba, Inspecionar e Buscar por "playerConfig" ##
###############################################################################

#############################################
## Inspecionar e Buscar por "playerConfig" ##
#############################################

def extract_video_url(config_text):
    #######################################################
    ## Regex para capturar URLs HLS (m3u8) e DASH (json) ##
    #######################################################
    hls_url_pattern = r'"url":"(https://[^"]+\.m3u8[^"]*)"'
    
    #######################################
    ## Buscar as URLs no texto do código ##
    #######################################
    hls_url_match = re.search(hls_url_pattern, config_text)
    
    ###################################################
    ## Selecionar HLS se disponível, senão usar DASH ##
    ###################################################
    if hls_url_match:
        video_url = hls_url_match.group(1).replace("\\u0026", "&")
    else:
        print("Nenhuma URL de vídeo encontrada no trecho de código.")
        return None
    
    return video_url


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

#######################################################################
## Recebe o trecho de código e o nome do arquivo de saída do usuário ##
#######################################################################
name = input('Nome do arquivo: ')
output_name = name+'.mp4'
config_text = input("Insira o trecho de código com a URL do vídeo: ")
video_url = extract_video_url(config_text)


################################################
## Se a URL for encontrada, inicia o download ##
################################################
if video_url:
    print(f"URL do vídeo encontrada: {video_url}")
    download_video(video_url,output_name)
